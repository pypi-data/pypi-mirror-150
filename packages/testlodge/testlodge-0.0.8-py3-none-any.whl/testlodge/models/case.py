from typing import Optional
from typing import TypedDict

from testlodge._types import DateTimeStr
from testlodge._types import Pagination
from testlodge.models.custom_field import CustomField
from testlodge.models.requirements import RequirementDocumentDetails
from testlodge.models.user import UserDetails


class CaseDetails(TypedDict):

    id: int
    project_id: int
    suite_section_id: int
    position: int
    last_saved_by_id: int
    last_saved_by: UserDetails
    created_at: DateTimeStr
    updated_at: DateTimeStr
    custom_fields: list[CustomField]
    requirements: list[RequirementDocumentDetails]
    step_number: str
    title: str
    description: Optional[str]
    test_steps: Optional[str]
    expected_result: Optional[str]


class CaseListDetails(TypedDict):

    pagination: Pagination
    steps: list[CaseDetails]
