-- Initial table creation
-- depends: 
CREATE TABLE "users" (
  "id" varchar PRIMARY KEY,
  "name" varchar,
  "password_hash" varchar,
  "created_dt" timestamptz,
  "updated_dt" timestamptz
);
