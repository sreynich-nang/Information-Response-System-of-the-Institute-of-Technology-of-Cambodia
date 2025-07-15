export interface UploadedFile {
  name: string;
  size: number;
  type: string;
  status: 'uploading' | 'done' | 'error';
}