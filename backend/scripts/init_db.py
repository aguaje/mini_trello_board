import boto3
import time
from datetime import datetime
import uuid


def create_table():
    """
    creates the KanbanBoard table in the local dynamodb if it doesn't already exist and adds some seed data:
    3 columns (To Do, In Progress, and Done) with some cards in each column
    :return:
    """
    # Create the DynamoDB client
    dynamodb = boto3.client(
        'dynamodb',
        endpoint_url='http://localhost:8000',
        region_name='local',
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy'
    )

    try:
        # Delete the table if it exists
        try:
            dynamodb.delete_table(TableName='KanbanBoard')
            print("Waiting for table to be deleted...")
            time.sleep(5)
        except:
            pass

        # Create the table with GSI
        response = dynamodb.create_table(
            TableName='KanbanBoard',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI1PK', 'AttributeType': 'S'},
                {'AttributeName': 'GSI1SK', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'GSI1',
                    'KeySchema': [
                        {'AttributeName': 'GSI1PK', 'KeyType': 'HASH'},
                        {'AttributeName': 'GSI1SK', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print("Table created successfully")
        print("Waiting for table to be created...")
        time.sleep(5)

        # Add sample data
        table = boto3.resource(
            'dynamodb',
            endpoint_url='http://localhost:8000',
            region_name='local',
            aws_access_key_id='dummy',
            aws_secret_access_key='dummy'
        ).Table('KanbanBoard')

        # Create board metadata
        table.put_item(Item={
            'PK': 'BOARD#default',
            'SK': 'METADATA',
            'title': 'Erin\'s Kanban Board',
            'createdAt': datetime.utcnow().isoformat()
        })

        # Create sample columns with UUIDs
        columns = [
            {'id': str(uuid.uuid4()), 'title': 'To Do', 'position': 0},
            {'id': str(uuid.uuid4()), 'title': 'In Progress', 'position': 1},
            {'id': str(uuid.uuid4()), 'title': 'Done', 'position': 2}
        ]

        # Store column IDs for creating cards
        column_ids = [col['id'] for col in columns]

        for column in columns:
            table.put_item(Item={
                'PK': 'BOARD#default',
                'SK': f"COLUMN#{column['id']}",
                'id': column['id'],
                'title': column['title'],
                'position': column['position'],
                'createdAt': datetime.utcnow().isoformat()
            })

        # Create sample cards using the actual column UUIDs
        cards = [
            {
                'id': str(uuid.uuid4()),
                'content': 'First task',
                'columnId': column_ids[0],  # To Do column
                'rank': '0|bbbbb'
            },
            {
                'id': str(uuid.uuid4()),
                'content': 'Second task',
                'columnId': column_ids[0],  # To Do column
                'rank': '0|ccccc'
            },
            {
                'id': str(uuid.uuid4()),
                'content': 'In progress task',
                'columnId': column_ids[1],  # In Progress column
                'rank': '0|bbbbb'
            },
            {
                'id': str(uuid.uuid4()),
                'content': 'Completed task',
                'columnId': column_ids[2],  # Done column
                'rank': '0|bbbbb'
            }
        ]

        for card in cards:
            table.put_item(Item={
                'PK': 'BOARD#default',
                'SK': f"CARD#{card['id']}",
                'id': card['id'],
                'content': card['content'],
                'columnId': card['columnId'],
                'rank': card['rank'],
                'GSI1PK': f"BOARD#default#COLUMN#{card['columnId']}",
                'GSI1SK': f"CARD#{card['id']}",
                'createdAt': datetime.utcnow().isoformat()
            })

        print("Sample data inserted successfully")

        # Print the column IDs for reference
        print("\nCreated columns:")
        for col in columns:
            print(f"{col['title']}: {col['id']}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_table()