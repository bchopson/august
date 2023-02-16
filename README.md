# August

API and ingest code for weather data

## Quickstart

1. Spin up database: `docker compose up`
2. Create tables: `flask --app august.app create-db`
3. Import data: `flask --app august.app import-weather-data wx_data`
4. Calculate stats: `flask --app august.app calculate-summary-data`
5. Run app: `flask --app august.app run`

API endpoints at https://localhost:5000/api/weather and https://localhost:5000/api/weather/stats
Docs at https://localhost:5000/docs
OpenAPI Spec at https://localhost:5000/openapi.yaml


## Answers

See [answers/answers.md](answers/answers.md)
