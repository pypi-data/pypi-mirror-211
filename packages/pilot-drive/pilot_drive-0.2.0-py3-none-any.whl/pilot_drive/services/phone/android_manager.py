"""
Module for interfacing with ADB to pull in Android notifications
"""
import subprocess
import itertools
import re
import json
import os
import typing

from pilot_drive.master_logging.master_logger import MasterLogger
from .abstract_manager import AbstractManager
from .constants import (
    SETTINGS_PATH,
    ADB_PACKAGE_NAMES,
    AdbCommands,
    AdbNotificationAttributes,
    AdbState,
    PhoneStates,
    Notification,
)


class AdbDependenciesMissingException(Exception):
    """
    Raised when dependencies are missing (ie. ADB or AAPT2)
    """

    def __init__(self, missing_dep: str, return_str: str) -> None:
        message = (
            "Missing dependency: "
            + missing_dep
            + ", bash output returned: "
            + return_str
        )
        super().__init__(message)


class AdbCommandFailedException(Exception):
    """
    Raised when an ADB command failed to execute
    """


class AdbFailedToFindPackageException(Exception):
    """
    Raised when a package was not found
    """


class AdbFailedToGetDeviceNameException(Exception):
    """
    Raised when the device name could not be retrieved
    """


class AndroidManager(AbstractManager):
    """
    The ADB notification manager
    """

    def __init__(self, logger: MasterLogger) -> None:
        """
        Initialize the Android Manager

        :param logger: An instantiated MasterLogger instance for logging
        """
        self.logger = logger
        self.__validate_dependencies()  # Confirm all dependencies are there

        try:
            with open(
                SETTINGS_PATH + ADB_PACKAGE_NAMES, "r", encoding="utf8"
            ) as package_file:
                self.__saved_package_names = json.load(fp=package_file)
        except FileNotFoundError:
            self.logger.info(
                msg="""Package names file does not exist,
                 it will be created when notifications are detected."""
            )
            self.__saved_package_names = {}
        except json.JSONDecodeError:
            self.logger.error(msg="Failed to decode ADB package names path!")
            self.__saved_package_names = {}

    def __validate_dependencies(self) -> None:
        """
        Validate the required dependencies for ADB exist on the system
        """
        adb_status_code, adb_return_str = subprocess.getstatusoutput(AdbCommands.ADB)
        aapt_status_code, aapt_return_str = subprocess.getstatusoutput(
            AdbCommands.AAPT_HELP
        )

        sucess_codes = [0, 1]

        if adb_status_code not in sucess_codes:
            raise AdbDependenciesMissingException(
                missing_dep="ADB", return_str=adb_return_str
            )

        if aapt_status_code not in sucess_codes:
            raise AdbDependenciesMissingException(
                missing_dep="AAPT2", return_str=aapt_return_str
            )

    def __add_package_name(self, package_id: str, package_name: str) -> None:
        """
        Append package name to the package names file
        """
        self.__saved_package_names[package_id] = package_name
        with open(
            SETTINGS_PATH + ADB_PACKAGE_NAMES, "w", encoding="utf8"
        ) as package_file:
            json.dump(fp=package_file, obj=self.__saved_package_names)

    def __get_package_name(self, package_id: str) -> str:
        """
        Get the package name based on the app ID utilizing AAPT2
        """
        try:
            package_label = self.__saved_package_names[package_id]
            if package_label is None:
                raise AdbFailedToFindPackageException(
                    f'Specified package "{package_id}" has previously failed, ignoring query.'
                )

            return package_label
        except KeyError as exc:
            package_path = self.__execute_adb_command(
                f"{AdbCommands.ADB_GET_PACKAGE_PATH}{package_id}"
            )
            if package_path == "" or not package_path:
                # self.__add_package_name(package_id=package_id, package_name=None)
                raise AdbFailedToFindPackageException(
                    f'Specified package ID "{package_id}" was not found!'
                ) from exc

            if len(package_path.split("\n")) > 1:
                for path in package_path.split("\n"):
                    if package_id in path and "base.apk" in path:
                        package_path = path

            package_path = package_path.replace("package:", "").replace(
                "=" + package_id, ""
            )
            package_name = package_path.split("/")[-1]

            self.__execute_adb_command(
                AdbCommands.ADB_PULL_PACKAGE + package_path + " /tmp/"
            )
            aapt_out = self.__execute_adb_command(
                f"{AdbCommands.AAPT_DUMP_BADGING}/tmp/{package_name}"
            )
            try:
                package_label = (
                    re.compile("application-label:'(.*)'").search(aapt_out).group(1)
                )
            except AttributeError as err:  # Failed to find the regex string
                self.__add_package_name(package_id=package_id, package_name=None)
                raise AdbFailedToFindPackageException(
                    f'Failed to parse aapt package return on package ID "{package_id}"!'
                ) from err

            self.__add_package_name(package_id=package_id, package_name=package_label)

            os.remove("/tmp/" + package_name)

            return package_label

    def __map_adb_attrs(self, adb_attr: AdbNotificationAttributes) -> str:
        """
        Convert the inpuit ADB attribute into the PILOT Drive format

        :param adb_attr: the AdbNotificationAttributes item to be mapped
        :return: the mapped attribute string
        """
        if not isinstance(
            adb_attr, AdbNotificationAttributes
        ):  # If an attribute like 'device' or 'app_name', leave it.
            return adb_attr

        adb_map = {
            AdbNotificationAttributes.UID: "id",
            AdbNotificationAttributes.TEXT: "body",
            AdbNotificationAttributes.OP_PACKAGE: "app_id",
            AdbNotificationAttributes.TITLE: "title",
            AdbNotificationAttributes.TIME: "time",
        }

        return adb_map[adb_attr]

    @property
    def state(self) -> PhoneStates:
        """
        The state of the ADB device. Maps ADB to PILOT Drive phone states

        :return: PHONE_STATE object
        """
        state = self.__execute_adb_command(AdbCommands.ADB_GET_STATE).split("\n")[0]
        match state:
            case AdbState.ADB_DEVICE:
                return PhoneStates.CONNECTED
            case AdbState.ADB_NOT_CONNECTED:
                return PhoneStates.DISCONNECTED
            case AdbState.ADB_NO_PERMISSIONS:
                return PhoneStates.LOCKED
            case AdbState.ADB_NOT_TRUSTED:
                return PhoneStates.UNTRUSTED
            case _:
                self.logger.error(
                    msg='Failed to detect ADB state, falling back to "Not Connected"!'
                )
                return PhoneStates.DISCONNECTED

    @property
    def notifications(self) -> list:
        """
        Get the list of notifications that have been aggregated via ADB

        :return: the list of notifications pulled from ADB
        """
        if self.state == PhoneStates.CONNECTED:
            notif_dump = self.__execute_adb_command(AdbCommands.ADB_DUMP_NOTIFICATIONS)
            return self.__parse_notifications(notif_dump)
        self.logger.error(msg=f"Invalid state: {self.state.value}")
        return []

    @property
    def device_name(self) -> str:
        """
        Get the name of the connected ADB device

        :return: the name of the connected ADB device
        """
        re_string = "name: (.*)"
        adb_name = self.__execute_adb_command(AdbCommands.ADB_DEVICE_NAME)
        try:
            return re.compile(re_string).search(adb_name).group(1)
        except AttributeError as exc:
            raise AdbFailedToGetDeviceNameException(exc) from exc

    def __get_notification_attr_type(self, attr: str):
        """
        Get the notification attribute type

        :param attr: the attribute to get
        """
        result_type = Notification.__annotations__[self.__map_adb_attrs(attr)]
        if (
            typing.get_origin(result_type) == typing.Union
        ):  # this ensures it pulls the correct type out of typing.Optional type
            return typing.get_args(result_type)[0]

        return result_type

    def __parse_notifications(self, notifications: str) -> list:
        """
        Parse an ADB notification dump into a clean, serializable notification

        :param notifications: an ADB notification dump string
        """
        parsed_notifs = []

        notifs_list = notifications.split("NotificationRecord")
        for notif in notifs_list:
            formatted_notif = {}
            notif_lines = notif.split("\n")
            for line, notif_attr in itertools.product(
                notif_lines, AdbNotificationAttributes
            ):
                if re.match(notif_attr.value, line):
                    re_string = notif_attr.value

                    try:
                        result = (
                            re.compile(re_string).search(line).group(1)
                        )  # Pull the result based on the regex string
                        result_type = self.__get_notification_attr_type(notif_attr)
                        result = result_type(
                            result
                        )  # Ensure that the result is of the proper type (str, int, etc)
                        formatted_notif[
                            self.__map_adb_attrs(adb_attr=notif_attr)
                        ] = result
                    except AttributeError:  # Failed to find the regex string
                        self.logger.error(
                            msg=f'Failed to find regex string "{re_string}" in "{line}"'
                        )
                        continue

            if len(formatted_notif.keys()) > 0:
                try:
                    # Add the package name
                    name = self.__get_package_name(package_id=formatted_notif["app_id"])
                    formatted_notif["app_name"] = name

                    # Add the device
                    try:
                        formatted_notif["device"] = self.device_name
                    except (
                        AdbFailedToGetDeviceNameException
                    ):  # Normally occurs when the device is disconnected.
                        self.logger.error(msg="Failed to get device name!")
                        formatted_notif["device"] = None

                except (KeyError, AdbFailedToFindPackageException) as exc:
                    self.logger.error(
                        msg=f'Failed to find package on notification "{formatted_notif}": {exc}'
                    )
                    continue

                try:
                    notif_obj = Notification(**formatted_notif)
                    parsed_notifs.append(notif_obj)
                except (
                    TypeError
                ) as exc:  # If the needed values didn't exist, don't create the notification object
                    self.logger.debug(
                        msg=f'Failed to create notification from: "{formatted_notif}": {exc}'
                    )
                    continue

        return parsed_notifs

    def __execute_adb_command(self, command: str):
        """
        Execute a command via suprocess

        :param command: the full command to be executed
        """
        try:
            return subprocess.getoutput(command)
        except Exception as exc:
            raise AdbCommandFailedException(
                f'Failed to execute ADB command "{command}": {exc}'
            ) from exc
