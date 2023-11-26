from mongoengine import connect
import configparser
from pathlib import Path


# config parcer
config = configparser.ConfigParser()
path_to_config = Path(__file__).parent.joinpath("config_db.ini")
config.read(path_to_config)

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
address = config.get("DB", "address")
db_name = config.get("DB", "db_name")

# connection
connect(
    host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{address}/{db_name}?retryWrites=true&w=majority""",
    ssl=True,
)
