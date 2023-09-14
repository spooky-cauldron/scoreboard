from http import HTTPStatus
from unittest.mock import MagicMock, PropertyMock, patch

from app import (
    get_board_data,
    get_board_info,
    get_board_team_score,
    patch_board_team_score,
)
from schema import PatchTeamScoreBody
from standard_responses import not_found


@patch('app.redis_client.hgetall', return_value={'name': 'test board'})
def test_get_board_info(mock):
    response, code = get_board_info(board_id='0')
    assert response == {'name': 'test board'}
    assert code == HTTPStatus.OK
    mock.assert_called_once()


@patch('app.redis_client.hgetall', return_value={})
def test_get_board_info_not_found(mock):
    response = get_board_info(board_id='0')
    assert response == not_found()
    mock.assert_called_once()


@patch('app.redis_client.hgetall', return_value={'team 0': '0'})
def test_get_board_data(mock):
    response, code = get_board_data(board_id='0')
    assert response == {'team 0': 0}
    assert code == HTTPStatus.OK
    mock.assert_called_once()


@patch('app.redis_client.hgetall', return_value={})
def test_get_board_data_not_found(mock):
    response = get_board_data(board_id='0')
    assert response == not_found()
    mock.assert_called_once()


@patch('app.redis_client.hget', return_value='0')
def test_get_board_team_score(mock):
    response, code = get_board_team_score(board_id='0', team='0')
    assert response == {'score': 0}
    assert code == HTTPStatus.OK
    mock.assert_called_once()


@patch('app.redis_client.hget', return_value=None)
def test_get_board_team_score_not_found(mock):
    response = get_board_team_score(board_id='0', team='0')
    assert response == not_found()
    mock.assert_called_once()
