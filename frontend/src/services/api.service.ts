/**
 * API service for backend communication
 * Handles all HTTP requests to the backend API
 */

import { API_CONFIG, ERROR_MESSAGES } from '@/constants';
import type { AnalysisResult } from '@/types/vdr';

/**
 * Custom API error class
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public details?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * API service class for making HTTP requests
 */
class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL;
  }

  /**
   * Handle API response and errors
   * @param response - Fetch response
   * @returns Parsed response data
   * @throws ApiError on failure
   */
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: ERROR_MESSAGES.NETWORK_ERROR }));

      throw new ApiError(
        errorData.detail || ERROR_MESSAGES.NETWORK_ERROR,
        response.status,
        errorData.detail
      );
    }

    return response.json();
  }

  /**
   * Analyze documents from uploaded ZIP file
   * @param file - ZIP file to analyze
   * @param onProgress - Optional progress callback
   * @returns Analysis result
   */
  async analyzeDocuments(
    file: File,
    onProgress?: (message: string) => void
  ): Promise<AnalysisResult> {
    try {
      onProgress?.('Preparing upload...');

      const formData = new FormData();
      formData.append('file', file);

      onProgress?.('Uploading file to server...');

      const response = await fetch(`${this.baseUrl}${API_CONFIG.ENDPOINTS.ANALYSE}`, {
        method: 'POST',
        body: formData,
      });

      onProgress?.('Processing response...');

      return this.handleResponse<AnalysisResult>(response);
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }

      // Network or other errors
      throw new ApiError(
        ERROR_MESSAGES.NETWORK_ERROR,
        undefined,
        error instanceof Error ? error.message : String(error)
      );
    }
  }

  /**
   * Export analysis results as Markdown
   * @param data - Analysis result data
   */
  async exportReport(data: AnalysisResult): Promise<void> {
    try {
      const response = await fetch(`${this.baseUrl}${API_CONFIG.ENDPOINTS.EXPORT}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new ApiError(ERROR_MESSAGES.EXPORT_FAILED, response.status);
      }

      // Create blob and download
      const blob = await response.blob();
      this.downloadBlob(blob, 'vdr_summary.md');
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }

      throw new ApiError(
        ERROR_MESSAGES.EXPORT_FAILED,
        undefined,
        error instanceof Error ? error.message : String(error)
      );
    }
  }

  /**
   * Download blob as file
   * @param blob - Blob data
   * @param filename - Name for downloaded file
   */
  private downloadBlob(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }

  /**
   * Health check endpoint
   * @returns Health status
   */
  async healthCheck(): Promise<{ message: string; status: string }> {
    try {
      const response = await fetch(`${this.baseUrl}/`);
      return this.handleResponse(response);
    } catch (error) {
      throw new ApiError(
        'API health check failed',
        undefined,
        error instanceof Error ? error.message : String(error)
      );
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export for use in hooks
export { ApiService };

