allow(actor, action, resource) if
  has_permission(actor, action, resource);

actor ActorClass {}

resource ProjectAuthorizable {
  permissions = ["read", "write"];
  roles = ["viewer", "user", "admin"];

  "read" if "viewer";

  "viewer" if "user";
  "write" if "user";

  "user" if "admin";
}

# have a role to act within a project ID
has_role(_actor: ActorClass, role_name: String, pa: ProjectAuthorizable) if
  role in _actor.roles and
  role_name = role.role_name and
  "project" = role.actor_type and
  pa.project_id = role.actor_id;
