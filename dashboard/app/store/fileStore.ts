import { create } from 'zustand';

interface FileStore {
  uploadedFiles: string[];
  addUploadedFiles: (files: string[]) => void;
}

export const useFileStore = create<FileStore>((set) => ({
  uploadedFiles: [],
  addUploadedFiles: (files) => set((state) => ({
    uploadedFiles: [...state.uploadedFiles, ...files]
  })),
}));