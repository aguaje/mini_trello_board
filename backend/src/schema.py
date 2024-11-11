import logging

import graphene

logger = logging.getLogger(__name__)


class Card(graphene.ObjectType):
    id = graphene.UUID()
    content = graphene.String()
    column_id = graphene.UUID()
    rank = graphene.String()
    created_at = graphene.String()


class Column(graphene.ObjectType):
    id = graphene.UUID()
    title = graphene.String()
    position = graphene.Int()
    cards = graphene.List(Card)


class Board(graphene.ObjectType):
    id = graphene.String()
    title = graphene.String()
    columns = graphene.List(Column)


class CreateCardInput(graphene.InputObjectType):
    content = graphene.String(required=True)
    column_id = graphene.String(required=True)


class CreateColumnInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    position = graphene.Int(required=True)


class Query(graphene.ObjectType):
    board = graphene.Field(Board, board_name=graphene.String(default_value="default"))

    def resolve_board(self, info, board_name="default"):
        try:
            db_client = info.context["db_client"]
            return db_client.get_board(board_name)
        except Exception as e:
            logger.error(f"Error fetching board: {e}")
            return []


class CreateCard(graphene.Mutation):
    class Arguments:
        input = CreateCardInput(required=True)

    Output = Card

    def mutate(self, info, input):
        try:
            db_client = info.context["db_client"]
            return db_client.create_card(input)
        except Exception as e:
            logger.error(f"Error creating card for input {input}: {e}")
            return None


class UpdateCardContent(graphene.Mutation):
    class Arguments:
        card_id = graphene.String(required=True)
        content = graphene.String(required=True)
        board_name = graphene.String(default_value="default")

    Output = Card

    def mutate(self, info, card_id, content, board_name):
        try:
            db_client = info.context["db_client"]
            return db_client.update_card_content(card_id, content, board_name)
        except Exception as e:
            logger.error(f"Error updating card content {card_id}: {e}")
            return None


class DeleteCard(graphene.Mutation):
    class Arguments:
        card_id = graphene.String(required=True)
        board_name = graphene.String(default_value="default")

    Output = Card

    def mutate(self, info, card_id, board_name):
        try:
            db_client = info.context["db_client"]
            return db_client.delete_card(card_id, board_name)
        except Exception as e:
            logger.error(f"Error deleting card {card_id}: {e}")
            return None


class CreateColumn(graphene.Mutation):
    class Arguments:
        input = CreateColumnInput(required=True)

    Output = Column

    def mutate(self, info, input):
        try:
            db_client = info.context["db_client"]
            return db_client.create_column(input)
        except Exception as e:
            logger.error(f"Error creating column for input {input}: {e}")
            return None


class Mutation(graphene.ObjectType):
    create_card = CreateCard.Field()
    create_column = CreateColumn.Field()
    update_card_content = UpdateCardContent.Field()
    delete_card = DeleteCard.Field()
