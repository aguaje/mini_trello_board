import React, { useState } from 'react';

export function Card({ id, content: initialContent, onDeleteCard, onUpdateCardContent }) {
    const [isEditingCard, setIsEditingCard] = useState(false);
    const [editedContent, setEditedContent] = useState(initialContent);

    const handleSave = () => {
        onUpdateCardContent(id, editedContent);
        setIsEditingCard(false);
      };
    
      return (
        <div
          className={`
            bg-white
            border border-gray-200
            rounded-lg
            p-3
            shadow-sm
            hover:shadow-md
            transition-all
            cursor-pointer
            group
          `}
        >
        <div className="flex justify-between">
        {isEditingCard ? (
            <div className="flex flex-col w-full gap-2">
            <textarea
                className="w-full p-2 text-sm border rounded"
                value={editedContent}
                onChange={(e) => setEditedContent(e.target.value)}
            />
            <div className="flex gap-2">
                <button 
                    className="px-2 py-1 text-sm text-white bg-blue-500 rounded hover:bg-blue-600"
                    onClick={handleSave}
                >
                Save
                </button>
                <button 
                    className="px-2 py-1 text-sm text-gray-700 bg-gray-100 rounded hover:bg-gray-200"
                    onClick={() => {
                        setIsEditingCard(false);
                        setEditedContent(initialContent); // Reset to original content on cancel
                    }}
                >
                Cancel
                </button>
            </div>
            </div>
        ) : (
            <>
            <span className="text-gray-700 text-sm">{initialContent}</span>
            <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button 
                    className="p-1 hover:bg-gray-100 rounded"
                    aria-label="Edit card"
                    title="Edit card"
                    onClick={() => setIsEditingCard(true)}
                >
                <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                </svg>
                </button>
                <button 
                    className="p-1 hover:bg-gray-100 rounded"
                    onClick={onDeleteCard}
                    aria-label="Delete card"
                    title="Delete card"
                >
                <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                </button>
            </div>
            </>
        )}
        </div>
    </div>
    );
  }