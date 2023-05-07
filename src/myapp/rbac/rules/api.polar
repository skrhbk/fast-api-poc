allow(actor, action, resource) if
  has_permission(actor, action, resource);

actor ActorClass {}

resource Request {
  permissions = ["read", "write"];
  roles = ["admin"];

  "read" if "admin";
  "write" if "admin";
}

# admin is grated with all permissions
has_permission(_actor: ActorClass, _: String, _: Request) if
  role in _actor.roles and
  "admin" = role.role_name and
  "api" = role.resource;