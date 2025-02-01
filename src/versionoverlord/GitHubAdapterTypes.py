
from typing import NewType

from datetime import date

from dataclasses import dataclass

from semantic_version import Version as SemanticVersion

ReleaseName    = NewType('ReleaseName', str)
ReleaseId      = NewType('ReleaseId',   int)
ReleaseNumber  = NewType('ReleaseNumber', int)


@dataclass
class AdapterMilestone:
    """
    Synthetic class for github.Milestone.Milestone
    """
    title:       str = ''
    state:       str = ''
    description: str = ''
    dueDate:     date | None = date.today()

    releaseNumber: ReleaseNumber = ReleaseNumber(0)


@dataclass
class AdapterRelease:
    """
    Synthetic class for GitRelease
    """
    title: str = ''
    body:  str = ''
    draft: bool = True

    tag:   SemanticVersion = SemanticVersion('0.0.0')
    id:    ReleaseId       = ReleaseId(0)
