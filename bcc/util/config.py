from dotenv import load_dotenv
from decouple import config
from prodict import Prodict

load_dotenv()

gcal = Prodict.from_dict({
    "local_calendar": config("local_calendar_id"),
    "cloud_calendar": config("cloud_calendar_id"),
})
