import React, { useState } from 'react';
import { Card } from './Card';

export function Column({ id, title, cards, onAddCard, onDeleteCard, onUpdateCardContent }) {
    const [isAddingCard, setIsAddingCard] = useState(false);
    const [newCardContent, setNewCardContent] = useState('');
  
    const handleAddCardSubmit = (e) => {
      e.preventDefault();
      onAddCard(id, newCardContent);
      setNewCardContent('');
      setIsAddingCard(false);
    };
  
    return (
      <div className="flex-none w-[280px] bg-gray-50 rounded-lg p-3 mx-2 border border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-semibold text-gray-700">{title}</h2>
          {/* <button className="text-gray-400 hover:text-gray-600">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10 6a2 2 0 110-4 2 2 0 010 4zM10 12a2 2 0 110-4 2 2 0 010 4zM10 18a2 2 0 110-4 2 2 0 010 4z" />
            </svg>
          </button> */}
        </div>
  
          <div className="flex flex-col gap-2 min-h-[200px] overflow-y-auto max-h-[calc(100vh-200px)]">
            {cards.map(card => (
              <Card
                key={card.id}
                id={card.id}
                columnId={id}
                content={card.content}
                onDeleteCard={() => onDeleteCard(card.id)}
                onUpdateCardContent={onUpdateCardContent}
              />
            ))}
          </div>
  
        {isAddingCard ? (
          <div className="mt-2">
            <textarea
              value={newCardContent}
              onChange={(e) => setNewCardContent(e.target.value)}
              className="w-full p-2 border rounded-md text-sm resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter a title for this card..."
              rows="3"
              autoFocus
            />
            <div className="flex gap-2 mt-2">
              <button
                onClick={handleAddCardSubmit}
                className="bg-blue-600 text-white px-3 py-1.5 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
              >
                Add card
              </button>
              <button
                onClick={() => {
                  setIsAddingCard(false);
                  setNewCardContent('');
                }}
                className="text-gray-600 hover:bg-gray-100 px-2 py-1.5 rounded-md text-sm transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setIsAddingCard(true)}
            className="mt-2 text-gray-600 hover:bg-gray-100 w-full text-left px-3 py-2 rounded-md text-sm transition-colors"
          >
            <span className="flex items-center">
              <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
              Add a card
            </span>
          </button>
        )}
      </div>
    );
  }