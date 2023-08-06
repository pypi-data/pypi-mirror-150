from typing import TypedDict

from testlodge._types import DateTimeStr


class UserDetails(TypedDict):

    id: int
    firstname: str
    lastname: str
    email: str
    created_at: DateTimeStr
    updated_at: DateTimeStr
