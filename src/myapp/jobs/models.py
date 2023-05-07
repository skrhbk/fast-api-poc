from enum import Enum

from pydantic import BaseModel


class JobStatus(Enum):
    NEW = "NEW"
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class ProjectAuthorizable(BaseModel):
    project_id: str


class Job(ProjectAuthorizable):
    id: str
    job_status: JobStatus
