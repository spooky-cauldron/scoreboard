import logging
import os
from http import HTTPStatus
from typing import Any
from uuid import uuid4

from flask import Flask
from redis import Redis

from middleware import body
from schema import (
    PatchTeamScoreBody,
    PatchTeamScoreResponse,
    PostScoreboardBody,
    PostScoreboardResponse,
    ScoreboardInfo,
    ScoreResponse,
)
from standard_responses import not_found

app = Flask('scoreboard')
log = logging.getLogger()
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', '6379'))
redis_client = Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True
)


@app.get('/scoreboard/<board_id>')
def get_board_info(board_id: str) -> tuple[dict[str, Any], int]:
    log.debug('Get board info event.')
    board_info = redis_client.hgetall(f'board:{board_id}:info')
    if not board_info:
        log.debug(f'Board {board_id} info not found.')
        return not_found()
    return ScoreboardInfo(**board_info).model_dump(), HTTPStatus.OK


@app.get('/scoreboard/<board_id>/data')
def get_board_data(board_id: str) -> tuple[dict[str, Any], int]:
    log.debug('Get board data event.')
    team_data = redis_client.hgetall(f'board:{board_id}:data')
    if not team_data:
        log.debug(f'Board {board_id} data not found.')
        return not_found()
    return {key: int(value) for key, value in team_data.items()}, HTTPStatus.OK


@app.get('/scoreboard/<board_id>/data/<team>')
def get_board_team_score(board_id: str, team: str) -> tuple[dict[str, Any], int]:
    log.debug('Get team score event.')
    score = redis_client.hget(f'board:{board_id}:data', team)
    if score is None:
        log.debug(f'Board {board_id} team {team} score not found.')
        return not_found()
    return ScoreResponse(score=score).model_dump(), HTTPStatus.OK


@app.patch('/scoreboard/<board_id>/data/<team>')
@body(PatchTeamScoreBody)
def patch_board_team_score(body: PatchTeamScoreBody, board_id: str, team: str) -> dict[str, Any]:
    log.debug('Patch team score event.')
    total_score = redis_client.hincrby(
        f'board:{board_id}:data',
        team,
        body.amount,
    )
    if total_score is None:
        log.debug(f'Board {board_id} team {team} not found.')
        return not_found()
    return PatchTeamScoreResponse(score=total_score).model_dump(), HTTPStatus.OK


@app.post('/scoreboard')
@body(PostScoreboardBody)
def post_board(body: PostScoreboardBody) -> tuple[dict[str, Any], int]:
    log.debug('Post scoreboard event.')
    board_id = str(uuid4())
    log.debug(f'Creating scoreboard {board_id}')
    board_info = {'name': body.name}
    board_data = {team: 0 for team in body.teams}
    redis_client.hset(f'board:{board_id}:info', mapping=board_info)
    redis_client.hset(f'board:{board_id}:data', mapping=board_data)
    response = PostScoreboardResponse(id=board_id, **body.model_dump())
    log.debug(f'Created scoreboard {board_id}')
    return response.model_dump(), HTTPStatus.CREATED


if __name__ == '__main__':
    app_host = os.getenv('APP_HOST', 'localhost')
    app_port = int(os.getenv('APP_PORT', '8080'))
    app.run(host=app_host, port=app_port)
