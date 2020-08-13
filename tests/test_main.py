import pytest
from . import (
    ProjectCreaterMock,
    Project,
)


def test_main():
    project_creater = ProjectCreaterMock(Project)
    assert project_creater is not None
