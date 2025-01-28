from typing import Optional
from sqlmodel import Field, SQLModel
from discord.abc import Snowflake

class Account(SQLModel, table=True):
    id: Optional[Snowflake] = Field(default=None, primary_key=True)
    restricted: bool

class Server(SQLModel, table=True):
    id: Optional[Snowflake] = Field(default=None, primary_key=True)
    verified: bool = Field(default=False)
    locale: str = Field(default="en_US", foreign_key="locale.id")

class ServerSettingsList(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    default_val: str

class ServerSettings(SQLModel, table=True):
    server: Snowflake = Field(primary_key=True, foreign_key="server.id")
    setting: int = Field(primary_key=True, foreign_key="server_settings_list.id")
    val: str
