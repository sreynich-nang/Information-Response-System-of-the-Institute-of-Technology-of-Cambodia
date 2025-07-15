'use client';

import { FiSend } from 'react-icons/fi';
import { Message } from './types';
import { useState } from 'react';

interface Props {
  loading: boolean;
  input: string;
  setInput: (val: string) => void;
  onSubmit: (message: string) => void;
}

export default function ChatInput({ loading, input, setInput, onSubmit }: Props) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) onSubmit(input);
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type your message..."
        className="flex-1 p-2 border border-gray-300 rounded-lg text-black placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        disabled={loading}
      />
      <button
        type="submit"
        className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
        disabled={loading || !input.trim()}
      >
        <FiSend className="w-5 h-5" />
      </button>
    </form>
  );
}