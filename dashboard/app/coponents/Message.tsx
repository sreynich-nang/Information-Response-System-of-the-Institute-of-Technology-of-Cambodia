interface MessageProps {
  message: {
    content: string;
    role: 'user' | 'assistant';
  };
}

export default function ChatMessage({ message }: MessageProps) {
  return (
    <div
      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
    >
      <div
        className={`max-w-lg p-4 rounded-lg ${
          message.role === 'user'
            ? 'bg-blue-500 text-white'
            : 'bg-white text-black shadow'
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
