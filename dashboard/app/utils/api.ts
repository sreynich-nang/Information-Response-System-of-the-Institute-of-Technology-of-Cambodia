// utils/api.ts

export interface UploadResponse {
  filename: string;
  // extend with more fields if backend sends
}

export interface ChatResponse {
  answer: string;
  // extend with more fields if needed
}

/**
 * Uploads files to the server.
 * @param files List of files to upload.
 * @returns The server response JSON on success.
 */
export async function uploadFiles(files: File[]): Promise<UploadResponse> {
  if (files.length === 0) throw new Error('No files to upload.');

  const formData = new FormData();
  // Assuming backend expects only the first file, adjust if multiple supported
  formData.append('file', files[0]);

  const response = await fetch('http://127.0.0.1:8000/api/upload', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Upload failed');
  }

  return response.json();
}

/**
 * Sends a chat message query to the server.
 * @param query The chat input string.
 * @param conversationId Optional conversation ID, defaults to 'default-conversation'.
 * @returns The chat server response JSON.
 */
export async function sendChatMessage(
  query: string,
  conversationId = 'default-conversation'
): Promise<ChatResponse> {
  const response = await fetch('http://127.0.0.1:8000/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify({ query, conversation_id: conversationId }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}