'use client';

import { Message } from './types';

export default function MessageItem({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-lg p-4 rounded-lg ${
          isUser ? 'bg-blue-500 text-white' : 'bg-white text-black shadow'
        }`}
      >
        {message.role === 'assistant' ? (
          <div
            dangerouslySetInnerHTML={{
              __html: message.content.replace(/\n/g, '<br />'),
            }}
          />
        ) : (
          message.content
        )}
      </div>
    </div>
  );
}