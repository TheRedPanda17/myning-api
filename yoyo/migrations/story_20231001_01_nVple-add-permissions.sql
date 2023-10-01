-- Add permissions
-- depends: story_20230929_01_uSfDZ-initial-table-creation


CREATE TABLE "permissions" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "created_dt" timestamptz,
  "updated_dt" timestamptz
);


CREATE TABLE "users_permissions" (
  "permission_id" int,
  "user_id" int,
  "created_dt" timestamptz,
  PRIMARY KEY(permission_id, user_id)
);

ALTER TABLE "users_permissions" ADD FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id");
ALTER TABLE "users_permissions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "permissions" ADD CONSTRAINT "permissions_unique_names" UNIQUE ("name");

INSERT INTO "permissions" VALUES(1, 'create_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(2, 'edit_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(3, 'delete_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(4, 'view_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(5, 'grant_users_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(6, 'view_users_permissions', NOW(), NOW());

INSERT INTO "users" VALUES(1, 'Admin', 'change_this', NOW(), NOW());

INSERT INTO "users_permissions" VALUES(1, 1, NOW());
INSERT INTO "users_permissions" VALUES(2, 1, NOW());
INSERT INTO "users_permissions" VALUES(3, 1, NOW());
INSERT INTO "users_permissions" VALUES(4, 1, NOW());
INSERT INTO "users_permissions" VALUES(5, 1, NOW());
INSERT INTO "users_permissions" VALUES(6, 1, NOW());
