import React from 'react';
import { Search, Loader2 } from 'lucide-react';

interface Props {
    onSearch: (query: string) => void;
    isLoading: boolean;
}

export const SearchBar = ({ onSearch, isLoading }: Props) => {
    const [query, setQuery] = React.useState('');

    return (
        <div className = "relative mb-12">
            <input
                type="text"
                value={query}
                placeholder='Digite sua pesquisa...'
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && onSearch(query)}
                className="w-96 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button onClick={() => onSearch(query)} className="absolute right-2 top-1/2 transform -translate-y-1/2 text-blue-500 hover:text-blue-700 focus:outline-none" disabled={isLoading}>
            {isLoading ? <Loader2 className="animate-spin" /> : <Search />}
        </button>
        </div>
    );
};