import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from graphene import Schema

from src.dynamodb import DynamoDBClient
from src.schema import Query, Mutation

load_dotenv()

FRONTEND_BASE_URL = os.getenv('FRONTEND_BASE_URL', 'http://localhost:3000')
DB_URL = os.getenv('DB_URL', 'http://localhost:8000')
AWS_REGION_NAME = os.getenv('AWS_REGION', 'local')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'dummy')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy')

db_client = DynamoDBClient(DB_URL, AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_BASE_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema = Schema(query=Query, mutation=Mutation)


@app.post("/graphql")
async def graphql_endpoint(request: Request):
    # Set CORS headers for the main request
    headers = {
        "Access-Control-Allow-Origin": FRONTEND_BASE_URL,
        "Access-Control-Allow-Credentials": "true",
    }

    try:
        data = await request.json()

        # Pass db_client in context
        context = {
            "request": request,
            "db_client": db_client
        }

        result = await schema.execute_async(
            data.get("query"),
            context_value=context,
            variable_values=data.get("variables"),
            operation_name=data.get("operationName"),
        )

        if result.errors:
            return JSONResponse(
                content={"errors": [str(error) for error in result.errors]},
                headers=headers
            )

        return JSONResponse(
            content={"data": result.data},
            headers=headers
        )
    except Exception as e:
        return JSONResponse(
            content={"errors": [str(e)]},
            headers=headers,
            status_code=500
        )


# Add OPTIONS handler for preflight requests
@app.options("/graphql")
async def graphql_options():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": FRONTEND_BASE_URL,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Credentials": "true",
        }
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
