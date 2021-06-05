import time

import fire
from beautiful_date import *
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.person import Person
from gcsa.recurrence import Recurrence, YEARLY

from bcc.util import base_logger
from bcc.util.config import gcal

logger = base_logger.get_logger()
YEAR_START = 1 / Jan / D.today().year
# YEAR_START = date(year=date.today().year, month=1, day=1)
YEAR_END = 31 / Dec / D.today().year


# YEAR_END = date(year=date.today().year, month=12, day=31)


def create_gcal_client(cal_id: str) -> GoogleCalendar:
    return GoogleCalendar(calendar=cal_id, credentials_path='/tmp/credentials.json', token_path='/tmp/token.pickle', save_token=True)


def clear_events(cloud):
    all_events = []
    for event in cloud.get_events(1 / Jan / 2018, 1 / Jan / 2050):
        all_events.append(event)

    for event in all_events:
        cloud.delete_event(event)


def clone_bday_events(local: GoogleCalendar, cloud: GoogleCalendar, echo=False):
    all_events = []
    # Time min and max params allow us to avoid creating duplicate birthday events by only focusing on a single year
    # e.g. Without these params if 'Josh' has a birthday today, then a calendar event would show up twice. One for today, and one for next year. So it would end up creating 2 recurring events instead of just one
    for event in local.get_events(time_min=YEAR_START,
                                  time_max=YEAR_END,
                                  single_events=True,
                                  order_by="startTime"):
        all_events.append(event)

    for event in all_events:
        bcc_user = Person(display_name="Calendar Copy Script", _is_self=True)

        bday_gadget = {
            "display": "chip",
            "type": "application/x-google-gadgets+xml",
            "iconLink": "https://calendar.google.com/googlecalendar/images/cake.gif",
            "link": "https://calendar.google.com/googlecalendar/images/cake.gif",
            "preferences": {
                "goo.contactsEventType": "BIRTHDAY",
                "goo.contactsIsMyContact": "true"
            }
        }  # For cool cake icon on event

        cloned_bday = Event(
            summary=event.summary,
            start=event.start,
            end=event.end,
            colord_id=event.color_id,
            _creator=bcc_user,
            _organizer=bcc_user,
            timezone=event.timezone,
            default_reminders=True,
            recurrence=Recurrence.rule(freq=YEARLY, count=10),
            transparency="transparent",
            status="confirmed",
            gadget=bday_gadget
        )
        if echo:
            logger.debug(event)

        cloud.add_event(cloned_bday)

    logger.info(f"Successfully cloned birthdays")


def run(local_id: str = gcal.local_calendar, cloud_id: str = gcal.cloud_calendar, verbose: bool = False):
    local_cal: GoogleCalendar = create_gcal_client(cal_id=local_id)
    cloud_cal: GoogleCalendar = create_gcal_client(cal_id=cloud_id)

    # Clear out all birthday events from the cloud calendar first before creating new ones
    logger.info(f"Deleting existing B-day events in cloud calendar: {cloud_id}")
    clear_events(cloud=cloud_cal)

    # Sleep for 1 minute to avoid rate-limiting
    logger.info("Sleeping for 1 minute")
    time.sleep(32)

    # Actually clone birthdays
    logger.info(f"Cloning birthday events from calendar {local_id} to {cloud_id}")
    clone_bday_events(local=local_cal, cloud=cloud_cal, echo=verbose)
