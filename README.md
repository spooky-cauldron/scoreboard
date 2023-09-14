# Scoreboard

Scoreboard Flask application which uses Redis for data storage.

## Endpoints

| Endpoint                                   | Description                   |
| ------------------------------------------ | ----------------------------- |
| `POST /scoreboard`                         | Create a new scoreboard.      |
| `GET /scoreboard/<board_id>/data/<team>`   | Get a team's score.           |
| `PATCH /scoreboard/<board_id>/data/<team>` | Add to a team's score.        |
| `GET /scoreboard/<board_id>`               | Get a scoreboard's info.      |
| `GET /scoreboard/<board_id>/data`          | Get all scores in scoreboard. |

## Run Locally

```
pip install -r requirements.txt
python app.py
```

## Run Docker

```
docker-compose up
```

## Run Tests

```
cd tests
pip install -r requirements.txt
pytest -v
```
