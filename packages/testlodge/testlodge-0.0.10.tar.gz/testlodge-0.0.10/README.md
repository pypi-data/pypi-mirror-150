[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# Description

Python client library for interacting with TestLodge.

# Installation

`pip install testlodge`

# Usage

``` python
import os

from testlodge import Client


tl = Client(
    email='my.email@email.com',
    api_key=os.environ['TESTLODGE_API_KEY'],
    account_id=os.environ['TESTLODGE_ACCOUNT_ID'],
)
```

## Users

``` python
from testlodge import UserJSON


user_json: UserJSON = dict(
    id=123456,
    firstname='First',
    lastname='Last',
    email='user@email.com',
    created_at="2022-01-01T20:30:40.123456Z",
    updated_at="2022-05-16T01:08:41.493190Z",
)
```

## Requirement Documents

``` python
from testlodge import RequirementDocumentJSON


requirement_document_json: RequirementDocumentJSON = dict(
    id=123456,
    title='title',
    should_version: True,
    project_id=234567,
    created_at="2022-01-01T20:30:40.123456Z",
    updated_at="2022-05-16T01:08:41.493190Z",
)
```

## Suite

...

## Suite Section

``` python
from testlodge import SuiteSectionJSON


suite_section_json: SuiteSectionJSON = dict(
    id=123456,
    title='title',
    suite_id=234567,
    created_at="2022-01-01T20:30:40.123456Z",
    updated_at="2022-05-16T01:08:41.493190Z",
)
```

## Case

``` python
from testlodge import CaseJSON


case_json: CaseJSON = dict(
    id=123456,
    project_id=234567,
    suite_section_id=345678,
    position=1,
    last_saved_by_id=456789,
    last_saved_by=user_json,
    created_at="2022-01-01T20:30:40.123456Z",
    updated_at="2022-05-16T01:08:41.493190Z",
    custom_fields=[],
    requirements=[],
    step_number='TC123',
    title='test case 1',
    description=None,
    test_steps=None,
    expected_result=None,
)
```

## Custom Field

``` python
from testlodge import CustomFieldJSON


custom_field_json: CustomFieldJSON = dict(
    id=123456,
    name='cf_1',
    value='my_value'),
)
```
