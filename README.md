# My Mini Trello
A simple page for a Kanban Board with columns that contain cards.

Uses:
- Python / Graphene and FastAPI in the backend
- DynamoDB Local
- React / Hooks + Tailwind CSS / Apollo Client GraphQL in the frontend

# Running
Bring up the docker container with DynamoDB Local
`docker-compose up -d`

## Backend
`cd backend`
### Install Dependencies
`pip install -r requirements.txt`

### Create Database Table with Seed Data
Prerequisite: DynamoDB Local should be running (from the Dockerfile)

`python scripts/init_db.py`

### Create/Update .env file
`cp .env.example .env`

Update env vars inside the .env file as needed

### Run FastAPI server
`python -m uvicorn src.main:app --reload --port 8080`

## Frontend
`cd frontend`

### Install Dependencies
`npm i`

### Create/Update .env file
`cp .env.example .env`

Update env vars inside the .env file as needed

### Run Frontend
`npm run start`

in your web browser, navigate to http://localhost:3000 to view the application


## Resetting Data:
```commandline
# Stop containers
docker-compose down
# Remove data
rm -rf docker/dynamodb/*
# Restart
docker-compose up -d
# Reinitialize
python backend/scripts/init_db.py
```

## Helpful Links
- View DynamoDB Tables: http://localhost:8001/
    - Kanban Table: http://localhost:8001/tables/KanbanBoard
- Swagger Docs: http://localhost:8080/docs
- Health Check: http://localhost:8080/health


