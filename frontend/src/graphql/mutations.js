import { gql } from '@apollo/client';

export const CREATE_CARD = gql`
  mutation CreateCard($input: CreateCardInput!) {
    createCard(input: $input) {
      content
      columnId
    }
  }
`;

export const UPDATE_CARD_CONTENT = gql`
    mutation UpdateCardContent($cardId: String!, $newContent: String!, $boardName: String) {
        updateCardContent(cardId: $cardId, content: $newContent, boardName: $boardName) {
            id
            content
        }
    }
`;

export const DELETE_CARD = gql`
    mutation DeleteCard($cardId: String!, $boardName: String) {
        deleteCard(cardId: $cardId, boardName: $boardName) {
            id
            content
            rank
        }
    }
`;

export const CREATE_COLUMN = gql`
  mutation CreateColumn($input: CreateColumnInput!) {
    createColumn(input: $input) {
      id
      title
      position
      cards {
        id
        content
        columnId
        rank
      }
    }
  }
`;
