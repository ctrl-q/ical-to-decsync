import logging
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from dataclasses import dataclass
from datetime import timedelta
from os import getenv
from pathlib import Path

from icalendar import Alarm, Calendar, Event
from libdecsync import Decsync

logging.basicConfig(
    level=getenv("LOGLEVEL", "INFO"),
    format="{asctime} [{levelname}] {name}: {message}",
    style="{",
)
logger = logging.getLogger(__name__)


@dataclass
class Args:
    calendar: Calendar
    decsync_cc_dir: Path
    decsync_collection: str
    decsync_cc_app_id: str
    default_alarm_minutes: int


def parse_args() -> Args:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("ics_file")
    parser.add_argument("--decsync-cc-dir", required=True, dest="decsync_cc_dir")
    parser.add_argument(
        "--decsync-collection", dest="decsync_collection", required=True
    )
    parser.add_argument("--decsync-cc-app-id", dest="decsync_cc_app_id", required=True)
    parser.add_argument(
        "--default-alarm-minutes", dest="default_alarm_minutes", type=int, default=15
    )
    args = parser.parse_args()
    args = Args(
        calendar=Calendar.from_ical(Path(args.ics_file).read_text()),
        decsync_cc_dir=Path(args.decsync_cc_dir),
        decsync_collection=args.decsync_collection,
        decsync_cc_app_id=args.decsync_cc_app_id,
        default_alarm_minutes=args.default_alarm_minutes,
    )
    return args


def main():
    args = parse_args()
    decsync = Decsync(
        decsync_dir=str(args.decsync_cc_dir),
        sync_type="calendars",
        collection=args.decsync_collection,
        own_app_id=args.decsync_cc_app_id,
    )
    for event in args.calendar.walk("vevent"):
        cal = Calendar()
        cal.add("prodid", args.decsync_cc_app_id)
        cal.add("version", "2.0")
        event: Event

        if not event.walk(Alarm.name):
            alarm = Alarm()
            alarm.add("ACTION", "DISPLAY")
            alarm.add("DESCRIPTION", "Reminder")
            alarm.add("TRIGGER", -timedelta(minutes=args.default_alarm_minutes))
            event.add_component(alarm)

        cal.add_component(event)
        decsync.set_entry(
            ["resources", str(event.decoded("uid"), "utf-8")],
            None,
            str(cal.to_ical(), "utf-8"),
        )


if __name__ == "__main__":
    main()
