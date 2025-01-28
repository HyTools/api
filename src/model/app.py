from __future__ import annotations

import enum
from pydantic import field_validator
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Column, Enum, Field, Relationship, String, Integer

class AccountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    BANNED = "BANNED"
    DELETED = "DELETED"

class Locale(str, enum.Enum):
    EN_US = "en_US"
    FR_FR = "fr_FR"

class Permissions(enum.IntFlag):
    ADMINISTRATOR      = 1 << 0
    MANAGE_PERMISSIONS = 1 << 1
    MANAGE_ROLES       = 1 << 2
    MANAGE_SERVERS     = 1 << 3
    MANAGE_USERS       = 1 << 4
    SUSPEND_USER       = 1 << 5
    BAN_USER           = 1 << 6
    VIEW_LOGS          = 1 << 7
    MANAGE_EVENTS      = 1 << 8
    CREATE_EVENT       = 1 << 9

    def add(self, permission: "Permissions") -> "Permissions":
        """Add a permission to the current set of permissions."""
        return self | permission

    def remove(self, permission: "Permissions") -> "Permissions":
        """Remove a permission from the current set of permissions."""
        return self & ~permission

    def has(self, permission: "Permissions") -> bool:
        """Check if the current set of permissions includes the given permission."""
        return (self & permission) == permission
    
    def has_any(self, *permissions: "Permissions") -> bool:
        """Check if any of the given permissions are present"""
        return any(self.has(perm) for perm in permissions)
    
    def has_all(self, *permissions: "Permissions") -> bool:
        """Check if all given permissions are present"""
        return all(self.has(perm) for perm in permissions)

    def __str__(self):
        if not self.value:
            return "No permissions"
        return " | ".join([perm.name for perm in type(self) if self & perm])
    
class Benefits(enum.IntFlag):
    SOMETHING = 1 << 0

    def add(self, benefit: "Benefits") -> "Benefits":
        return self | benefit

    def remove(self, benefit: "Benefits") -> "Benefits":
        return self & ~benefit

    def has(self, benefit: "Benefits") -> bool:
        return (self & benefit) == benefit
    
    def has_any(self, *benefits: "Benefits") -> bool:
        return any(self.has(b) for b in benefits)
    
    def has_all(self, *benefits: "Benefits") -> bool:
        return all(self.has(b) for b in benefits)

    def __str__(self):
        if not self.value:
            return "No benefits"
        return " | ".join([b.name for b in type(self) if self & b])

class Premium(SQLModel, table=True):
    __tablename__="app_premium"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    users: list["User"] = Relationship(back_populates="premium")


class Role(SQLModel, table=True):
    __tablename__="app_role"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    permissions: Permissions = Field(
        default=Permissions(0),
        sa_column=Column(Integer())
    )
    priority: int

    users: list["User"] = Relationship(back_populates="role")

    @field_validator('permissions', pre=True)
    def validate_permissions(cls, v):
        if isinstance(v, int):
            return Permissions(v)
        elif isinstance(v, Permissions):
            return v
        raise ValueError("Permissions must be an integer or Permissions instance")

class User(SQLModel, table=True):
    __tablename__="app_users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    alt_id: Optional[UUID] = Field(
        foreign_key="app_users.id",
        sa_column=Column("alt", String, default=None)
    )
    alt: Optional["User"] = Relationship(back_populates="alts")
    alts: list["User"] = Relationship(back_populates="alt")

    premium_id: int = Field(
        foreign_key="app_premium.id",
        sa_column=Column("premium", Integer, default=0, nullable=False)
    )
    premium: Optional["Premium"] = Relationship(back_populates="users")

    role_id: int = Field(
        foreign_key="app_role.id",
        sa_column=Column("role", Integer, default=0, nullable=False)
    )
    role: Optional["Role"] = Relationship(back_populates="users")

    locale: Locale = Field(default=Locale.EN_US, sa_column=Column(Enum(Locale)))
    status: AccountStatus = Field(default=AccountStatus.ACTIVE, sa_column=Column(Enum(AccountStatus)))

