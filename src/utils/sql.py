import os
from dotenv import load_dotenv
from nonebot.log import logger

load_dotenv()

game_db_config = {
    "host": os.getenv("GAME_DB_HOST"),
    "port": os.getenv("GAME_DB_PORT"),
    "database": os.getenv("GAME_DB_NAME"),
    "user": os.getenv("GAME_DB_USER"),
    "password": os.getenv("GAME_DB_PASSWORD"),
}

web_db_config = {
    "host": os.getenv("WEB_DB_HOST"),
    "port": os.getenv("WEB_DB_PORT"),
    "database": os.getenv("WEB_DB_NAME"),
    "user": os.getenv("WEB_DB_USER"),
    "password": os.getenv("WEB_DB_PASSWORD"),
}

logger.info(f"[DB] PostgreSQL | env loaded\ngame_db_config | {game_db_config}\nweb_db_config  | {web_db_config}")