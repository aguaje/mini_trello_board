export function Card({ content, onDeleteCard }) {
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
          <span className="text-gray-700 text-sm">{content}</span>
          <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button 
                className="p-1 hover:bg-gray-100 rounded"
                aria-label="Edit card"
                title="Edit card"
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
        </div>
      </div>
    );
  }