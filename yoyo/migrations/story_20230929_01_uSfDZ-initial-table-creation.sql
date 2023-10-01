-- Initial table creation
-- depends: 
CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "password" varchar,
  "created_dt" timestamptz,
  "updated_dt" timestamptz
);

ALTER TABLE "users" ADD CONSTRAINT unique_names UNIQUE ("name");