# Running
## Install Dependencies
`pip install -r requirements.txt`

## Create Database Table with Seed Data
Prerequisite: DynamoDB Local should be running (from the Dockerfile)
```commandline
cd ../
docker compose up -d
```

`python scripts/init_db.py`

## Create/Update .env file
`cp .env.example .env`

Update env vars inside the .env file as needed

## Run
`python -m uvicorn src.main:app --reload --port 8080`