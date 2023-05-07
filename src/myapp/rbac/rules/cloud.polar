allow(actor, action, resource) if
  has_permission(actor, action, resource);

actor ActorClass {}

resource Cloud {
  permissions = ["use"];
  roles = ["user", "admin"];

  "use" if "user";

  "user" if "admin";
}

# This rule tells Oso how to fetch roles
has_role(_actor: ActorClass, role_name: String, cloud: Cloud) if
  role in _actor.roles and
  role_name = role.role_name and
  cloud.key = role.resource;

# The cloud is open for all projects.
has_permission(_actor: ActorClass, "use", cloud: Cloud) if
  cloud.is_public;