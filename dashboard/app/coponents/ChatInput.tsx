import { useState } from 'react';
import { FiSend } from 'react-icons/fi';

interface ChatInputProps {
  loading: boolean;
  setMessages: React.Dispatch<React.SetStateAction<any[]>>;
  setLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setInput: React.Dispatch<React.SetStateAction<string>>;
}

export default function ChatInput({
  loading,
  setMessages,
  setLoading,
  setInput,
}: ChatInputProps) {
  const [input, setInputState] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      setLoading(true);
      const userMessage = { content: input, role: 'user' as const };
      setMessages((prev) => [...prev, userMessage]);

      const response = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'application/json',
        },
        body: JSON.stringify({
          query: input,
          conversation_id: 'default-conversation',
        }),
      });

      if (!response.ok) throw new Error(`API error: ${response.status}`);
      const data = await response.json();

      const assistantMessage = {
        content: data.answer || 'No answer received',
        role: 'assistant' as const,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setInputState('');
    } catch (error) {
      console.error('Error:', error);
      setMessages((prev) => [
        ...prev,
        {
          content:
            `Error: ${error instanceof Error ? error.message : 'Request failed'}`,
          role: 'assistant',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="max-w-2xl mx-auto flex gap-2" onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInputState(e.target.value)}
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
