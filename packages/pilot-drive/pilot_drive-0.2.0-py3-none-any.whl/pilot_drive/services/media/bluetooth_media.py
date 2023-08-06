"""
The Bluetooth media manager
"""
from types import NoneType
from typing import Any, Callable, Dict, List, Union
from dasbus.loop import EventLoop  # type: ignore # missing
from dasbus.typing import ObjPath, Variant, Str
from dasbus.error import DBusError

from pilot_drive.master_logging import MasterLogger

from .abstract_media_source import BaseMediaSource, TrackProps
from .constants import TrackStatus
from ..bluetooth import Bluetooth, BluetoothDevice
from ..shared.bluez_api import BluezDevice, BluezMediaPlayer, BluezAdapter


class BluetoothMedia(BaseMediaSource):
    """
    The Bluetooth media manager for Media. Utilizes the bluetooth service to relay metadata on
        currently playing media.
    """

    def __init__(
        self,
        push_to_queue_callback: Callable,
        bluetooth: Bluetooth,
        logger: MasterLogger,
    ) -> None:
        """
        Initialize the Bluetooth media manager

        :param push_to_queue_callback: method that pushes new events to the queue
        :param bluetooth: an instance of the Bluetooth service
        :param logger: an instance of the MasterLogger
        """
        super().__init__(push_to_queue_callback, logger)
        self.bluetooth = bluetooth
        self.adapter = self.bluetooth.bluez_adapter
        self.media_player: Union[BluezMediaPlayer, NoneType] = None
        self.__devices: List[BluetoothDevice] = []

        # on iOS sometimes only a duration comes in for an associated track.
        # It's important to store track info in this case
        self.__current_track = {}

    def __get_track_property_failed(
        self, prop: str, exc: DBusError, default: Any
    ) -> None:
        """
        Used to log when the getting of a property (position, track, playing) fails, most likely
            due to a state change.

        :param property: the property that failed
        :param exec: the DBus exception that was thrown
        :param default: the default value to be returned
        """
        self.logger.warning(
            msg=f'Failed to get property "{prop}" raised: "{exc}", defaulting to "{default}"!'
        )

    @property
    def position(self) -> int:
        """
        Get the track position

        :return: track position in milliseconds
        """
        try:
            return self.bluetooth.bluez_media_player.Position
        except DBusError as exc:
            default = 0
            self.__get_track_property_failed(
                prop="position", exc=exc, default=default)
            return default

    @property
    def track(self) -> Union[TrackProps, Dict[str, NoneType]]:
        """
        Get the track metadata

        :return: a dict of Title, Artist, Album, and Duration with corresponding values.
        """
        try:
            track = self.bluetooth.bluez_media_player.Track
            print(track)
        except DBusError as exc:
            print("GETTING TRACK FAILED")
            default = {"Title": None, "Artist": None,
                       "Album": None, "Duration": None}
            self.__get_track_property_failed(
                prop="track", exc=exc, default=default)
            return default

        is_empty_track = not bool(
            track.get("Title") or track.get("Album") or track.get("Artist")
        )
        if is_empty_track and (track.get("Duration") and self.__current_track):
            media_dict = {
                **self.__current_track,
                "Duration": track.get("Duration"),
            }
        else:
            # Convert the dasbus variant types to normal types (probably better ways to do this)
            media_dict = {
                "Title": track.get("Title"),
                "Artist": track.get("Artist"),
                "Album": track.get("Album"),
                "Duration": track.get("Duration"),
            }

            self.__current_track = media_dict

        # Convert dasbus Variants to native objects
        converted_dict = {}
        for key, value in media_dict.items():
            if value is not None:
                converted_dict[key] = value.unpack()
            else:
                converted_dict[key] = value

        return converted_dict

    @property
    def playing(self) -> bool:
        """
        Get whether the current track is playing

        :return: a boolean of True if playing and False if not playing
        """
        try:
            return self.bluetooth.bluez_media_player.Status == TrackStatus.PLAYING
        except DBusError as exc:
            default = False
            self.__get_track_property_failed(
                prop="playing", exc=exc, default=default)
            return default

    @property
    def active_av_devices(self) -> List[BluetoothDevice]:
        """
        Get a list of connected devices that have media capabilities

        :return: A list of connected & media capable BluetoothDevice instances
        """
        av_list = []
        for device in self.__devices:
            if device.connected and device.media:
                av_list.append(device)

        return av_list

    def __metadata_changed(self) -> None:
        """
        Metadata (BlueZ MediaPlayer1) callback when properties change
        """
        if len(self.active_av_devices) > 0:
            self.push_media_to_queue()

    def __interfaces_added(
        self, path: ObjPath, interface: str
    ) -> None:  # pylint: disable=unused-argument
        """
        Callback utilized when a new interface is added

        :param path: DBus path to the new interface
        :param interface: name of the interface that was added
        """

        if BluezMediaPlayer.interface in interface:
            self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)
            self.push_media_to_queue()
            self.bluetooth.bluez_media_player.PropertiesChanged.connect(
                self.__properties_changed
            )
        elif BluezDevice.interface in interface:
            bt_device = self.bluetooth.get_bluez_device(
                path=path, props_changed_callback=self.__properties_changed
            )
            self.__devices.append(bt_device)
            bt_device.bluez_device.PropertiesChanged.connect(
                bt_device.prop_changed)

    def __interfaces_removed(
        self, path: ObjPath, interfaces: List[Str]
    ) -> None:  # pylint: disable=unused-argument
        """
        Callback utilized when an interface is removed

        :param path: DBus path to the new interface
        :param interface: list of names of interfaces that were removed
        """
        if BluezDevice.interface in interfaces:
            for count, device in enumerate(self.__devices):
                if device.path == path:
                    self.__devices.pop(count)
                    break

        self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)

    def __properties_changed(
        self,
        interface: str,
        changes: Dict[str, Variant],  # pylint: disable=unused-argument
        invalidated_properties: List[str],  # pylint: disable=unused-argument
    ) -> None:
        """
        Callback utilized when an interface's properties change

        :param interface: names of interface that had a property change
        :param changes: a dict of changes on the properties of the interface
        :param invalidated_properties: a list of properties that were invalidated
        """
        match interface:
            case BluezAdapter.interface:
                self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)
            case BluezDevice.interface:
                self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)
            case BluezMediaPlayer.interface:
                self.__metadata_changed()

    def __initialize_observers(self) -> None:
        for path, services in self.bluetooth.bluez_root.GetManagedObjects().items():
            self.__interfaces_added(path, services)

        self.bluetooth.bluez_root.InterfacesAdded.connect(
            self.__interfaces_added)
        self.bluetooth.bluez_root.InterfacesRemoved.connect(
            self.__interfaces_removed)
        self.adapter.PropertiesChanged.connect(self.__properties_changed)

    def main(self) -> None:
        """
        Main loop of the bluetooth media manager. Creates a dasbus event loop and sets up initial
            callbacks, along with initial queue pushes.
        """
        loop = EventLoop()

        self.__initialize_observers()

        self.bluetooth.push_bluetooth_to_queue(devices=self.__devices)

        if len(self.active_av_devices) > 0:
            self.bluetooth.bluez_media_player.PropertiesChanged.connect(
                self.__properties_changed
            )
            self.push_media_to_queue()

        loop.run()
