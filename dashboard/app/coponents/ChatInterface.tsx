'use client';

import { useState, useRef, useEffect } from 'react';
import { FiUploadCloud } from 'react-icons/fi';
import FileUpload from './FileUpload';
import ChatMessage from './Message';
import ChatInput from './ChatInput';

interface Message {
  content: string;
  role: 'user' | 'assistant';
}

export default function ChatInterface() {
  const [isUploadVisible, setIsUploadVisible] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Upload Toggle Below Input */}
      <div className="max-w-2xl mx-auto mt-4">
        <button
          onClick={() => setIsUploadVisible(!isUploadVisible)}
          className="flex items-center text-blue-600 hover:text-blue-800 text-sm border border-gray-600 px-3 py-1 rounded-md"
        >
          {isUploadVisible ? 'Hide Upload' : 'Upload Documents'}
          <FiUploadCloud className="ml-2" />
        </button>
        {isUploadVisible && <FileUpload />}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-2xl mx-auto space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input and Send Message */}
      <div className="border-t p-4 bg-white">
        <ChatInput
          loading={loading}
          setMessages={setMessages}
          setLoading={setLoading}
        />

      </div>
    </div>
  );
}
