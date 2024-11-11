import { gql } from '@apollo/client';

export const GET_BOARD = gql`
    query GetBoard($boardName: String) {
        board(boardName: $boardName) {
            id
            title
            columns {
                id
                title
                position
                cards {
                    id
                    content
                    rank
                }
            }
        }
    }
`;
