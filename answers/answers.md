# Answers

## Problem 1 - Data Modeling

Model:

[WeatherData](../august/model.py)

## Problem 2 - Ingestion

Ingest code:

[WeatherDataImporter](../august/libs/importer.py)

## Problem 3 - Data Analysis

Model:

[WeatherDataSummary](../august/model.py)

Stats code:

[calculate_summary_data](../august/libs/stats.py)

## Problem 4 - REST API

Docs: http://localhost:5000/docs

Code: this repo

## Extra Credit - Deployment

I would deploy the app to Elastic Beanstalk. I would use the cron config of
Elastic Beanstalk to run the data ingestion code (which would be updated to
read files from S3 instead of the local filesystem). I would deploy the
database to RDS.
