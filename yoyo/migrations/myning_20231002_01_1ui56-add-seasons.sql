-- Add seasons
-- depends: myning_20231001_01_nVple-add-permissions


CREATE TABLE "seasons" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "start_dt" timestamptz,
  "end_dt" timestamptz,
  "created_dt" timestamptz,
  "updated_dt" timestamptz
);

ALTER TABLE "seasons" ADD CONSTRAINT "seasons_unique_names" UNIQUE ("name");

CREATE TABLE "users_seasons" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "season_id" int,
  "created_dt" timestamptz,
  "updated_dt" timestamptz
);


ALTER TABLE "users_seasons" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "users_seasons" ADD FOREIGN KEY ("season_id") REFERENCES "seasons" ("id");
ALTER TABLE "users_seasons" ADD CONSTRAINT "unique_user_seasons" UNIQUE ("user_id", "season_id");


CREATE TABLE "stats" (
  "id" SERIAL PRIMARY KEY,
  "user_season_id" int,
  "key" varchar,
  "value" float,
  "created_dt" timestamptz,
  "updated_dt" timestamptz
);

ALTER TABLE "stats" ADD FOREIGN KEY ("user_season_id") REFERENCES "users_seasons" ("id");