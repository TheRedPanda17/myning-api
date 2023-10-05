-- Add scores
-- depends: myning_20231002_01_1ui56-add-seasons


CREATE TABLE "scores" (
  "id" SERIAL PRIMARY KEY,
  "user_season_id" int,
  "score" float,
  "date" timestamptz
);


ALTER TABLE "scores" ADD FOREIGN KEY ("user_season_id") REFERENCES "users_seasons" ("id");
ALTER TABLE "scores" ADD CONSTRAINT "unique_scores_key" UNIQUE ("user_season_id", "date");
