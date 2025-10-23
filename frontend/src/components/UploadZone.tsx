/**
 * Upload zone component for file drag-and-drop and selection
 */

import { useCallback } from 'react';
import { Upload, FileArchive } from 'lucide-react';
import { useToast } from '@/hooks';
import { validateFile } from '@/utils';

interface UploadZoneProps {
  onFileSelect: (file: File) => void;
  disabled?: boolean;
}

/**
 * Component for uploading ZIP files with drag-and-drop support
 */
export const UploadZone = ({ onFileSelect, disabled }: UploadZoneProps) => {
  const { toast } = useToast();

  /**
   * Handle file drop
   */
  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      if (disabled) return;

      const file = e.dataTransfer.files[0];
      if (!file) return;

      // Validate file
      const validation = validateFile(file);
      if (!validation.valid) {
        toast({
          title: 'Invalid file',
          description: validation.error,
          variant: 'destructive',
        });
        return;
      }

      onFileSelect(file);
    },
    [onFileSelect, disabled, toast]
  );

  /**
   * Handle file input selection
   */
  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (!file) return;

      // Validate file
      const validation = validateFile(file);
      if (!validation.valid) {
        toast({
          title: 'Invalid file',
          description: validation.error,
          variant: 'destructive',
        });
        return;
      }

      onFileSelect(file);
    },
    [onFileSelect, toast]
  );

  return (
    <div
      className="relative border-2 border-dashed border-border rounded-lg p-12 text-center hover:border-primary/50 transition-colors bg-gradient-card"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <input
        type="file"
        accept=".zip,application/zip,application/x-zip-compressed"
        onChange={handleFileInput}
        disabled={disabled}
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
      />
      <div className="flex flex-col items-center gap-4">
        <div className="p-4 rounded-full bg-primary/10">
          <FileArchive className="w-12 h-12 text-primary" />
        </div>
        <div>
          <p className="text-lg font-semibold text-foreground mb-2">
            Drop your .zip file here or click to browse
          </p>
          <p className="text-sm text-muted-foreground">
            Maximum file size: 100MB • 10-20 documents recommended
          </p>
        </div>
        <Upload className="w-5 h-5 text-muted-foreground" />
      </div>
    </div>
  );
};
