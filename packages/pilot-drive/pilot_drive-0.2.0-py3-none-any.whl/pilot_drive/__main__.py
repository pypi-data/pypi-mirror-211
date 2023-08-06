"""
The entrypoint for PILOT Drive. This initializes the PilotDrive class, which starts the program.
"""
import signal
import os
import sys
import asyncio
import argparse
from pilot_drive.installer import (  # pylint: disable=import-outside-toplevel
    Installer,
    installer_arguments,
)
from pilot_drive import __version__ as version


def start() -> None:
    """
    Entrypoint for PILOT Drive. Handle arguments and determine to run main, or install.
    """
    parser = argparse.ArgumentParser(
        prog="pilot-drive", description="An open source vehicle headunit"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help=("Get the current version of PILOT Drive"),
    )

    installer_arguments(parser=parser)

    if os.geteuid() != 0:
        sys.exit(
            """\nYou need to have root privileges to run PILOT Drive.
            \nPlease try again, this time using 'sudo'. Exiting.\n"""
        )
    args = parser.parse_args()
    if args.version is True:
        print(f"PILOT Drive {version}")
        return

    if args.setup is True:
        pilot_drive_install = Installer(use_default=args.default)
        pilot_drive_install.main(args=args)
    else:
        run()


def run() -> None:
    """
    The main entrypoint method for PILOT Drive. This initializes the PILOT Drive class in an
    asyncio event loop.
    """
    from pilot_drive.pd_manager import (  # pylint: disable=import-outside-toplevel
        PilotDrive,
    )

    pilot_drive = PilotDrive()
    signal.signal(signalnum=signal.SIGINT, handler=pilot_drive.terminate)
    signal.signal(signalnum=signal.SIGTERM, handler=pilot_drive.terminate)

    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(pilot_drive.main())
    for stop_signal in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(stop_signal, main_task.cancel)
    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()


if __name__ == "__main__":
    start()
