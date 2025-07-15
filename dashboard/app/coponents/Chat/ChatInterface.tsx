'use client';

import { useState } from 'react';
import FileUpload from '../FileUpload/FileUpload';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import { Message } from './types';
import { FiUploadCloud } from 'react-icons/fi';

export default function ChatInterface() {
  const [showUpload, setShowUpload] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (text: string) => {
    setLoading(true);
    setInput('');
    const userMessage: Message = { content: text, role: 'user' };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({
          query: text,
          conversation_id: 'default-conversation',
        }),
      });

      if (!res.ok) throw new Error(`API error: ${res.status}`);
      const data = await res.json();

      const assistantMessage: Message = {
        content: data.answer || 'No answer received',
        role: 'assistant',
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Chat error:', error);
      setMessages((prev) => [
        ...prev,
        {
          content: `Error: ${error.message || 'Request failed'}`,
          role: 'assistant',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <div className="max-w-2xl mx-auto mt-4">
        <button
          onClick={() => setShowUpload(!showUpload)}
          className="flex items-center text-blue-600 hover:text-blue-800 text-sm border border-gray-600 px-3 py-1 rounded-md"
        >
          {showUpload ? 'Hide Upload' : 'Upload Documents'}
          <FiUploadCloud className="ml-2" />
        </button>
        {showUpload && <FileUpload />}
      </div>

      <MessageList messages={messages} />
      <div className="border-t p-4 bg-white">
        <ChatInput loading={loading} input={input} setInput={setInput} onSubmit={handleSendMessage} />
      </div>
    </div>
  );
}