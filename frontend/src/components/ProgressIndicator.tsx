import { Progress } from '@/components/ui/progress';
import { Loader2 } from 'lucide-react';
import type { UploadProgress } from '@/types/vdr';

interface ProgressIndicatorProps {
  progress: UploadProgress;
}

const statusMessages = {
  uploading: 'Uploading and extracting...',
  extracting: 'Extracting document text...',
  analyzing: 'Analysing documents...',
  complete: 'Analysis complete!',
  error: 'An error occurred',
};

export const ProgressIndicator = ({ progress }: ProgressIndicatorProps) => {
  const percentage = progress.total > 0 ? (progress.current / progress.total) * 100 : 0;
  
  // Use custom message if provided, otherwise use default
  const message = progress.message || statusMessages[progress.status];

  return (
    <div className="w-full space-y-4 p-6 rounded-lg bg-gradient-card border border-border shadow-card">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Loader2 className="w-5 h-5 animate-spin text-primary" />
          <span className="font-medium text-foreground text-lg">
            {message}
          </span>
        </div>
        <span className="text-sm font-medium text-muted-foreground">
          {Math.round(percentage)}%
        </span>
      </div>
      <Progress value={percentage} className="h-2" />
    </div>
  );
};
