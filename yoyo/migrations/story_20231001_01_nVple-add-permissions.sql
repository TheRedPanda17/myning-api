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
  "created_by" int,
  "created_dt" timestamptz,
  "revoked_by" int,
  "revoked_dt" timestamptz,
  PRIMARY KEY(permission_id, user_id)
);

ALTER TABLE "users_permissions" ADD FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id");
ALTER TABLE "users_permissions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "users_permissions" ADD FOREIGN KEY ("revoked_by") REFERENCES "users" ("id");
ALTER TABLE "users_permissions" ADD FOREIGN KEY ("created_by") REFERENCES "users" ("id");
ALTER TABLE "permissions" ADD CONSTRAINT "permissions_unique_names" UNIQUE ("name");

INSERT INTO "permissions" VALUES(DEFAULT, 'view_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(DEFAULT, 'grant_users_permissions', NOW(), NOW());
INSERT INTO "permissions" VALUES(DEFAULT, 'view_users_permissions', NOW(), NOW());

INSERT INTO "users" VALUES(DEFAULT, 'Admin', 'change_this', NOW(), NOW());

INSERT INTO "users_permissions" (permission_id, user_id, created_by, created_dt) VALUES(1, 1, 1, NOW());
INSERT INTO "users_permissions" (permission_id, user_id, created_by, created_dt) VALUES(2, 1, 1, NOW());
INSERT INTO "users_permissions" (permission_id, user_id, created_by, created_dt) VALUES(3, 1, 1, NOW());
