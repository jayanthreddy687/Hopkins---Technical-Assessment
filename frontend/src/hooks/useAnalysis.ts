/**
 * Custom hook for document analysis functionality
 */

import { useState, useCallback } from 'react';
import { apiService, ApiError } from '@/services';
import { validateFile } from '@/utils';
import { ANALYSIS_STAGES, SUCCESS_MESSAGES, ERROR_MESSAGES } from '@/constants';
import type { AnalysisResult, UploadProgress } from '@/types/vdr';

interface UseAnalysisReturn {
  isAnalyzing: boolean;
  progress: UploadProgress;
  result: AnalysisResult | null;
  error: string | null;
  analyzeFile: (file: File) => Promise<void>;
  reset: () => void;
}

/**
 * Hook for managing document analysis workflow
 * @returns Analysis state and functions
 */
export function useAnalysis(): UseAnalysisReturn {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [progress, setProgress] = useState<UploadProgress>({
    current: 0,
    total: 100,
    status: 'uploading',
  });
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  /**
   * Analyze uploaded file
   */
  const analyzeFile = useCallback(async (file: File) => {
    // Reset state
    setIsAnalyzing(true);
    setResult(null);
    setError(null);

    try {
      // Validate file
      const validation = validateFile(file);
      if (!validation.valid) {
        throw new ApiError(validation.error || ERROR_MESSAGES.INVALID_FILE_TYPE);
      }

      // Stage 1: Uploading
      setProgress({
        current: ANALYSIS_STAGES.UPLOADING.progress,
        total: 100,
        status: 'uploading',
        message: ANALYSIS_STAGES.UPLOADING.message,
      });
      await delay(500);

      // Stage 2: Extracting
      setProgress({
        current: ANALYSIS_STAGES.EXTRACTING.progress,
        total: 100,
        status: 'extracting',
        message: ANALYSIS_STAGES.EXTRACTING.message,
      });
      await delay(300);

      // Stage 3: Analyzing (actual API call)
      setProgress({
        current: ANALYSIS_STAGES.ANALYZING.progress,
        total: 100,
        status: 'analyzing',
        message: ANALYSIS_STAGES.ANALYZING.message,
      });

      const analysisResult = await apiService.analyzeDocuments(file, (message) => {
        console.log('Progress:', message);
      });

      // Stage 4: Complete
      setProgress({
        current: ANALYSIS_STAGES.COMPLETE.progress,
        total: 100,
        status: 'complete',
        message: `${ANALYSIS_STAGES.COMPLETE.message} Processed ${analysisResult.docs.length} documents`,
      });
      await delay(500);

      setResult(analysisResult);
    } catch (err) {
      console.error('Analysis error:', err);

      setProgress({
        current: 0,
        total: 0,
        status: 'error',
        message: ERROR_MESSAGES.ANALYSIS_FAILED,
      });

      const errorMessage =
        err instanceof ApiError
          ? err.message
          : ERROR_MESSAGES.ANALYSIS_FAILED;

      setError(errorMessage);
    } finally {
      setIsAnalyzing(false);
    }
  }, []);

  /**
   * Reset analysis state
   */
  const reset = useCallback(() => {
    setIsAnalyzing(false);
    setProgress({
      current: 0,
      total: 100,
      status: 'uploading',
    });
    setResult(null);
    setError(null);
  }, []);

  return {
    isAnalyzing,
    progress,
    result,
    error,
    analyzeFile,
    reset,
  };
}

/**
 * Utility function for delays
 */
function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

