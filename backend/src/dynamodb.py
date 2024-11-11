import logging
import uuid
from datetime import datetime
from typing import Optional

import boto3

from src.rank import get_next_ranking
from src.schema import Column, Card, Board

logger = logging.getLogger(__name__)


class DynamoDBClient:
    def __init__(self, db_url, aws_region, aws_access_key_id, aws_secret_access_key):
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=db_url,
            region_name=aws_region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.table = self.dynamodb.Table('KanbanBoard')

    def get_board(self, board_name: str = 'default') -> Optional[Board]:
        # Get board metadata first
        board_response = self.table.get_item(
            Key={
                'PK': f'BOARD#{board_name}',
                'SK': 'METADATA'
            }
        )

        if 'Item' not in board_response:
            logger.warning(f"Board {board_name} not found")
            return None

        board_data = board_response['Item']

        # Get columns
        column_response = self.table.query(
            KeyConditionExpression='PK = :pk AND begins_with(SK, :sk)',
            ExpressionAttributeValues={
                ':pk': f'BOARD#{board_name}',
                ':sk': 'COLUMN#'
            }
        )

        if not column_response['Items']:
            logger.warning(f"No columns found for board {board_name}")
            return Board(
                id=board_name,
                title=board_data['title'],
                columns=[]
            )

        columns = {}
        for col in column_response['Items']:
            columns[col['id']] = Column(
                id=col['id'],
                title=col['title'],
                position=col['position'],
                cards=[]
            )

        # Get cards for each column
        for column_id in columns.keys():
            card_response = self.table.query(
                IndexName='GSI1',
                KeyConditionExpression='GSI1PK = :pk',
                ExpressionAttributeValues={
                    ':pk': f'BOARD#{board_name}#COLUMN#{column_id}'
                }
            )

            # Process cards for this column
            for card in card_response['Items']:
                columns[column_id].cards.append(Card(
                    id=card['id'],
                    content=card['content'],
                    rank=card['rank']
                ))

            # Sort cards in this column
            columns[column_id].cards.sort(key=lambda x: x.rank)

        # Sort columns by position and create final Board object
        sorted_columns = sorted(columns.values(), key=lambda x: x.position)

        return Board(
            id=board_name,
            title=board_data['title'],
            columns=sorted_columns
        )

    async def create_card(self, data):
        column_id = data['column_id']
        highest_rank_in_column = self.get_highest_rank_in_column(column_id)
        next_rank = get_next_ranking(highest_rank_in_column)

        card_id = str(uuid.uuid4())
        board_name = data.get('board_name', 'default')
        item = {
            'PK': f"BOARD#{board_name}",
            'SK': f"CARD#{card_id}",
            'GSI1PK': f"BOARD#{board_name}#COLUMN#{column_id}",
            'GSI1SK': f"CARD#{card_id}",
            'id': card_id,
            'content': data['content'],
            'columnId': column_id,
            'rank': f"0|{next_rank}",  # TODO: implement buckets but for now everything is in bucket 0
            'createdAt': datetime.utcnow().isoformat()
        }
        self.table.put_item(Item=item)
        return item

    async def create_column(self, data):
        board_name = data.get('board_name', 'default')

        column_id = str(uuid.uuid4())
        item = {
            'PK': f"BOARD#{board_name}",
            'SK': f"COLUMN#{column_id}",
            'id': column_id,
            'title': data['title'],
            'position': data['position'],
            'createdAt': datetime.utcnow().isoformat()
        }
        self.table.put_item(Item=item)
        return {**item, 'cards': []}

    def get_highest_rank_in_column(self, column_id: str, board_name: str = 'default') -> str:
        """
        Get the highest rank in a column.  Does not include the bucket number in the return value.  So if the ranks
        are 0|aaa, 0|bbb, and 0|ccc (where 0| means they are in bucket 0), this would return 'ccc'

        Returns:
            - rank: str (if success)
            - None (if not success)
        """
        # First validate column exists
        column_response = self.table.get_item(
            Key={
                'PK': f'BOARD#{board_name}',
                'SK': f'COLUMN#{column_id}'
            }
        )

        if 'Item' not in column_response:
            logger.error(f'Column {column_id} not found')
            return None

        # Query cards in column
        card_response = self.table.query(
            IndexName='GSI1',
            KeyConditionExpression='GSI1PK = :pk',
            ExpressionAttributeValues={
                ':pk': f'BOARD#{board_name}#COLUMN#{column_id}'
            },
            ProjectionExpression='#rank',
            ExpressionAttributeNames={
                '#rank': 'rank'
            }
        )

        if not card_response['Items']:
            return 'aaaaa'  # Default for empty column

        highest_rank = max(item['rank'] for item in card_response['Items'])
        return highest_rank[2:]  # omit the bucket prefix of the rank
