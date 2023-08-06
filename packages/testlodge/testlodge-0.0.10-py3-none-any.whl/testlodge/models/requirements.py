from typing import TypedDict

from testlodge._types import DateTimeStr


class RequirementDocumentJSON(TypedDict):

    id: int
    title: str
    should_version: bool
    project_id: int
    created_at: DateTimeStr
    updated_at: DateTimeStr
