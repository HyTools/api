from __future__ import annotations

import enum
from typing import Optional
from sqlmodel import SQLModel, Column, Enum, Field, Relationship, Integer
from uuid import UUID

class Rank(str, enum.Enum):
    NONE = "NONE"
    VIP = "VIP"
    VIP_PLUS = "VIP+"
    MVP = "MVP"
    MVP_PLUS = "MVP+"
    MVP_PP = "MVP++"

class Guild(SQLModel, table=True):
    __tablename__="hypixel_guilds"
    id: Optional[int] = Field(default=None, primary_key=True)
    api_id: str
    name: str
    tag: str

    roles: list["GuildRole"] = Relationship(back_populates="guild")
    members: list["Player"] = Relationship(back_populates="guild")

class GuildRole(SQLModel, table=True):
    __tablename__="hypixel_guild_roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tag: str
    is_default: bool = Field(default=False)
    priority: int

    guild_id: int = Field(
        foreign_key="hypixel_guilds.id",
        sa_column=Column("guild", Integer, nullable=False)
    )
    guild: "Guild" = Relationship(back_populates="roles")

    members: list["Player"] = Relationship(back_populates="role")

class Player(SQLModel, table=True):
    __tablename__="minecraft_accounts"
    uuid: UUID = Field(primary_key=True)
    username: str
    restricted: bool = Field(default=False)
    rank: Rank = Field(default=Rank.NONE, sa_column=Column(Enum(Rank)))

    guild_id: Optional[int] = Field(
        foreign_key="hypixel_guilds.id",
        sa_column=Column("guild", Integer, nullable=True)
    )
    guild: Optional["Guild"] = Relationship(back_populates="members")

    role_id: Optional[int] = Field(
        foreign_key="hypixel_guild_roles.id",
        sa_column=Column("role", Integer, nullable=True)
    )
    role: Optional["GuildRole"] = Relationship(back_populates="members")

class MarketItem(SQLModel, table=True):
    __tablename__="app_market_items"