from typing import TypedDict

from testlodge._types import DateTimeStr


class SuiteSectionJSON(TypedDict):

    id: int
    title: str
    suite_id: int
    created_at: DateTimeStr
    updated_at: DateTimeStr
