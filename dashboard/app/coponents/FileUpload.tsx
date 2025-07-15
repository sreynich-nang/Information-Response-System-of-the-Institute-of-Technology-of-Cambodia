'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { FiUploadCloud, FiFile, FiX } from 'react-icons/fi';

export default function FileUpload() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt']
    },
    multiple: false
  });

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const uploadFiles = async () => {
    if (files.length === 0) return;

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', files[0]); // backend expects single file

      const response = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const result = await response.json();
      alert(`Successfully uploaded: ${result.filename}`);
      setFiles([]);
    } catch (error: any) {
      console.error('Upload error:', error);
      alert(error?.message || 'File upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-4 bg-gray-800 rounded-lg">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer
          ${isDragActive ? 'border-blue-500 bg-gray-700' : 'border-gray-600'}`}
      >
        <input {...getInputProps()} />
        <FiUploadCloud className="w-12 h-12 mx-auto text-gray-400 mb-2" />
        <p className="text-gray-300">
          {isDragActive ? 'Drop files here' : 'Drag files here or click to select'}
        </p>
        <p className="text-sm text-gray-400 mt-1">Supported formats: PDF, TXT</p>
      </div>

      {files.length > 0 && (
        <div className="mt-4">
          <h3 className="text-gray-300 mb-2">Selected File:</h3>
          {files.map((file, index) => (
            <div key={file.name} className="flex items-center justify-between bg-gray-700 rounded p-2 mb-2">
              <div className="flex items-center">
                <FiFile className="text-gray-400 mr-2" />
                <span className="text-gray-300">{file.name}</span>
              </div>
              <button
                onClick={() => removeFile(index)}
                className="text-red-400 hover:text-red-300"
              >
                <FiX />
              </button>
            </div>
          ))}
          <button
            onClick={uploadFiles}
            disabled={uploading}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg border border-gray-300 disabled:opacity-50"
          >
            {uploading ? 'Uploading...' : 'Upload File'}
          </button>
        </div>
      )}
    </div>
  );
}
