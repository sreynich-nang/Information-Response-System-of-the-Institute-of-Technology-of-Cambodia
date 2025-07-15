'use client';

import { useState } from 'react';
import { FiUpload } from 'react-icons/fi';
import { UploadedFile } from './types';

export default function FileUpload() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;

    const selectedFiles = Array.from(e.target.files);
    const newFiles: UploadedFile[] = selectedFiles.map((file) => ({
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'uploading',
    }));

    setFiles((prev) => [...prev, ...newFiles]);

    setUploading(true);
    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append('files', file));

    try {
      const res = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!res.ok) throw new Error(`Upload failed: ${res.statusText}`);

      const uploaded = await res.json();

      setFiles((prev) =>
        prev.map((f) =>
          uploaded.files.some((uf: any) => uf.name === f.name)
            ? { ...f, status: 'done' }
            : f
        )
      );
    } catch (error) {
      console.error('Upload error:', error);
      setFiles((prev) =>
        prev.map((f) => ({ ...f, status: 'error' }))
      );
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 mt-4 border border-gray-300 rounded-lg bg-white shadow">
      <label className="flex items-center gap-2 cursor-pointer text-blue-600 hover:text-blue-800">
        <FiUpload className="w-5 h-5" />
        <span>Choose Files</span>
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="hidden"
          disabled={uploading}
        />
      </label>

      {files.length > 0 && (
        <ul className="mt-4 space-y-2 text-sm">
          {files.map((file, idx) => (
            <li key={idx} className="flex justify-between items-center">
              <span className="truncate">{file.name}</span>
              <span className={`ml-2 text-xs ${
                file.status === 'done' ? 'text-green-600' :
                file.status === 'error' ? 'text-red-600' :
                'text-yellow-500'
              }`}>
                {file.status}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}