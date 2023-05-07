from myapp.database.mongo import MyMongo
from myapp.jobs.models import Job, JobStatus, ProjectAuthorizable
from myapp.rbac.exceptions import AuthorizationNotFound
from myapp.rbac.service import RoleService


if __name__ == "__main__":
    # for e in JobStatus:
    #     print(e)
    mongo = MyMongo()
    rbac_service = RoleService(mongo)

    # roles = rbac_service.list_roles({"actor_type": "project", "actor_id": "900001"})
    job = Job(id="job1", project_id="900001", job_status=JobStatus.NEW)
    rbac_service.authorize("project", "900001", "write", job)
    try:
        pa = ProjectAuthorizable(project_id="900003")
        rbac_service.authorize("project", "900003", "write", pa)
    except AuthorizationNotFound as e:
        print(e)
