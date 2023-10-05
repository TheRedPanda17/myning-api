from aiohttp import web

from myning.handlers import (
    monitoring,
    permissions,
    seasons,
    users,
    users_permissions,
    users_seasons,
    stats,
    scores,
)


def get_routes():
    return [
        web.get("/ping", monitoring.ping),
        # Users
        web.post("/users", users.create_user),
        web.get("/users", users.get_users),
        web.put("/users/{user_id:\d+}", users.update_user),
        # Permissions
        web.get("/permissions", permissions.get_permissions),
        # User Permissions
        web.get(
            "/users/{user_id:\d+}/permissions", users_permissions.get_user_permissions
        ),
        web.post(
            "/users/{user_id:\d+}/permissions", users_permissions.grant_user_permissions
        ),
        web.delete(
            "/users/{user_id:\d+}/permissions/{permission_id:\d+}",
            users_permissions.revoke_user_permissions,
        ),
        # Seasons
        web.get("/seasons", seasons.get_seasons),
        web.post("/seasons", seasons.create_season),
        # User Seasons
        web.post("/users/{user_id:\d+}/seasons", users_seasons.create_user_season),
        # Stats
        web.get("/users/{user_id:\d+}/seasons/{season_id:\d}/stats", stats.get_stats),
        web.post(
            "/users/{user_id:\d+}/seasons/{season_id:\d}/stats/sync", stats.sync_stats
        ),
        web.put("/users/{user_id:\d+}/seasons/{season_id:\d}/stats", stats.update_stat),
        web.post(
            "/users/{user_id:\d+}/seasons/{season_id:\d}/stats/{key}/increment",
            stats.increment_stat,
        ),
        # Scores
        web.post(
            "/users/{user_id:\d+}/seasons/{season_id:\d}/scores", scores.create_score
        ),
        web.get(
            "/users/{user_id:\d+}/seasons/{season_id:\d}/scores/recent",
            scores.get_score,
        ),
        web.get(
            "/users/{user_id:\d+}/seasons/{season_id:\d}/scores", scores.get_scores
        ),
    ]
