/**
 * Custom hook for exporting analysis results
 */

import { useState, useCallback } from 'react';
import { apiService, ApiError } from '@/services';
import { ERROR_MESSAGES, SUCCESS_MESSAGES } from '@/constants';
import type { AnalysisResult } from '@/types/vdr';

interface UseExportReturn {
  isExporting: boolean;
  error: string | null;
  exportReport: (data: AnalysisResult) => Promise<void>;
}

/**
 * Hook for managing report export functionality
 * @returns Export state and functions
 */
export function useExport(): UseExportReturn {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  /**
   * Export analysis results as Markdown
   */
  const exportReport = useCallback(async (data: AnalysisResult) => {
    setIsExporting(true);
    setError(null);

    try {
      await apiService.exportReport(data);
      console.log(SUCCESS_MESSAGES.EXPORT_COMPLETE);
    } catch (err) {
      console.error('Export error:', err);

      const errorMessage =
        err instanceof ApiError
          ? err.message
          : ERROR_MESSAGES.EXPORT_FAILED;

      setError(errorMessage);
      throw err; // Re-throw so caller can handle (e.g., show toast)
    } finally {
      setIsExporting(false);
    }
  }, []);

  return {
    isExporting,
    error,
    exportReport,
  };
}

