from typing import Optional
from sqlmodel import Field, SQLModel
from discord import abc

class Account(SQLModel, table=True):
    id: Optional[abc.Snowflake] = Field(default=None, primary_key=True)
    restricted: bool