/**
 * Export button component for downloading analysis reports
 */

import { Download } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useToast, useExport } from '@/hooks';
import { SUCCESS_MESSAGES } from '@/constants';
import type { AnalysisResult } from '@/types/vdr';

interface ExportButtonProps {
  data: AnalysisResult;
  disabled?: boolean;
}

/**
 * Button component to export analysis results as Markdown
 */
export const ExportButton = ({ data, disabled }: ExportButtonProps) => {
  const { toast } = useToast();
  const { isExporting, exportReport } = useExport();

  const handleExport = async () => {
    try {
      await exportReport(data);
      toast({
        title: SUCCESS_MESSAGES.EXPORT_COMPLETE,
        description: 'Your analysis has been downloaded as vdr_summary.md',
      });
    } catch (error) {
      // Error toast already shown
      console.error('Export failed:', error);
    }
  };

  return (
    <Button
      onClick={handleExport}
      disabled={disabled || isExporting}
      size="lg"
      className="bg-gradient-primary hover:opacity-90 transition-opacity"
    >
      <Download className="w-4 h-4 mr-2" />
      {isExporting ? 'Exporting...' : 'Download Markdown Report'}
    </Button>
  );
};
