import glob
from logging import getLogger
from typing import List

import oso
from fastapi import Request
from pydantic import BaseModel
from pymongo.collection import Collection
from pymongo.results import InsertOneResult

from myapp import utils
from myapp.clouds.models import Cloud
from myapp.database.mongo import MyMongo
from myapp.jobs.models import ProjectAuthorizable
from myapp.rbac.exceptions import AuthorizationNotFound, AuthorizationForbidden
from myapp.rbac.models import RoleRepository, Role, RoleCreate

logger = getLogger("RoleService")


class ActorClass(BaseModel):
    # name: str
    roles: List[Role]


class RoleService:
    def __init__(self, db: MyMongo):
        self._db = db.db
        self._coll: Collection = db.db.roles
        
        _oso = oso.Oso()
        _oso.register_class(ProjectAuthorizable)
        _oso.register_class(Cloud)
        _oso.register_class(Request)
        _oso.register_class(ActorClass)
        _oso.load_files(glob.glob(utils.get_sibling_file_path(__file__, "rules/*.polar")))
        self._oso = _oso

    def authorize(self, actor_type: str, actor_id: str, action: str, resource):
        roles = self.list_roles({"actor_type": actor_type, "actor_id": actor_id})
        actor = ActorClass(roles=roles)
        logger.debug(f"Authorize for actor[{actor}], action[{action}], resource[{resource}]")
        try:
            self._oso.authorize(actor, action, resource)
        except oso.NotFoundError as e:
            msg = "Resource not found or you don't have any permission on it"
            logger.warning(f"{msg}")
            raise AuthorizationNotFound(msg)
        except oso.ForbiddenError as e:
            msg = "You have any permission on them"
            logger.warning(f"{msg}")
            raise AuthorizationForbidden(msg)

    def list_roles(self, cond: dict):
        repo = RoleRepository(database=self._db)
        return list(repo.find_by(cond))

    # def get_role(self, cond: dict):
    #     repo = RoleRepository(database=self._db)
    #     return list(repo.find_by(cond))

    def create_role(self, role: RoleCreate):
        repo = RoleRepository(database=self._db)
        result: InsertOneResult = repo.save(Role(**role.dict()))
        return result.acknowledged

    def delete_role(self, cond: dict):
        if not cond:
            raise Exception("Empty delete condition is given!")
        result = self._coll.delete_many(cond)
        return result.raw_result


if __name__ == "__main__":
    mongo = MyMongo()

    # rbac_service = RoleService(mongo)
    # r = rbac_service.list_roles()
    # r = rbac_service.get_role({"role_name": "user", "actor_type": "project"})
    # data = {"actor_type": 'project', "actor_id": '900002', "role_name": 'user', "resource": 'aws|jp|a1'}
    # role = RoleCreate(**data)
    # r = rbac_service.create_role(role)
    # print(r)

    # from myapp.clouds.models import CloudRepository
    # repo = CloudRepository(database=mongo.db)
    # cloud_name = "gcp"
    # cloud = list(repo.find_by({"name": cloud_name}))[0]
    #
    # pid = "900001"
    # repo = RoleRepository(database=mongo.db)
    # roles = list(repo.find_by({"actor_type": "project", "actor_id": pid}))
    #
    # actor = ActorClass(name=pid, roles=roles)
    #
    # _oso.authorize(actor, "use", cloud)

    # _oso = oso.Oso()
    # _oso.register_class(Cloud)
    # _oso.register_class(Request)
    # _oso.register_class(ActorClass)
    # _oso.load_files(glob.glob("./rules/*.polar"))
    #
    # uid = "cckea"
    # repo = RoleRepository(database=mongo.db)
    # roles = list(repo.find_by({"actor_type": "user", "actor_id": uid}))
    # print(roles)
    # actor = ActorClass(name=uid, roles=roles)
    # _oso.authorize(actor, "read", Request({"type": "http"}))
