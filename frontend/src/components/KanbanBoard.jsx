import { gql, useMutation, useQuery } from '@apollo/client';
import React, { useState } from 'react';
import { Column } from './Column';

const GET_BOARD = gql`
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

const CREATE_CARD = gql`
  mutation CreateCard($input: CreateCardInput!) {
    createCard(input: $input) {
      content
      columnId
    }
  }
`;

const CREATE_COLUMN = gql`
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

export function KanbanBoard() {
    const [isAddingColumn, setIsAddingColumn] = useState(false);
    const [newColumnTitle, setNewColumnTitle] = useState('');
    const { loading, error, data } = useQuery(GET_BOARD);
    const [createCard] = useMutation(CREATE_CARD);
    const [createColumn] = useMutation(CREATE_COLUMN);
  
  
    if (loading) return <div className="p-8">Loading...</div>;
    if (error) return <div className="p-8">Error: {error.message}</div>;
  
    const handleAddCard = async (columnId, content) => {
      const column = data.board.columns.find(col => col.id === columnId);
      if (!column) return;
  
      try {
        await createCard({
          variables: {
            input: {
              content,
              columnId
            }
          },
            refetchQueries: [{ query: GET_BOARD }]
        });
      } catch (error) {
        console.error('Error creating card:', error);
      }
    };

    const handleAddColumn = async () => {
        if (!newColumnTitle.trim()) return;

        try {
            await createColumn({
            variables: {
                input: {
                    title: newColumnTitle,
                    position: data.board.columns.length
                }
            },
            refetchQueries: [{ query: GET_BOARD }]
            });
            setNewColumnTitle('');
            setIsAddingColumn(false);
        } catch (error) {
            console.error('Error creating column:', error);
        }
    };
  
    return (
      <div className="min-h-screen bg-white p-8">
        <h1 className="text-2xl font-bold mb-8">{data.board.title}</h1>
        <div className="flex justify-between items-center mb-8">

        <button
          onClick={() => setIsAddingColumn(true)}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Add Column
        </button>
      </div>

      {isAddingColumn && (
        <div className="mb-6">
          <input
            type="text"
            value={newColumnTitle}
            onChange={(e) => setNewColumnTitle(e.target.value)}
            className="p-2 border rounded mr-2"
            placeholder="Enter column title..."
            onKeyUp={(e) => {
              if (e.key === 'Enter') {
                handleAddColumn();
              }
            }}
            autoFocus
          />
          <button
            onClick={handleAddColumn}
            className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 mr-2"
          >
            Add
          </button>
          <button
            onClick={() => {
              setIsAddingColumn(false);
              setNewColumnTitle('');
            }}
            className="text-gray-500 px-3 py-1 rounded hover:bg-gray-200"
          >
            Cancel
          </button>
        </div>
      )}
        <div className="flex flex-row gap-8 overflow-x-auto min-h-[calc(100vh-200px)]">
        {data.board.columns.map(column => (
            <Column
            key={column.id}
            id={column.id}
            title={column.title}
            cards={column.cards}
            onAddCard={handleAddCard}
            />
        ))}
        </div>
      </div>
    );
  }