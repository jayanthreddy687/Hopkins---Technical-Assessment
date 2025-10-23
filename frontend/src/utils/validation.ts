/**
 * Validation utility functions
 */

import { UPLOAD_CONFIG, ERROR_MESSAGES } from '@/constants';

/**
 * Validate uploaded file
 * @param file - File to validate
 * @returns Validation result with error message if invalid
 */
export function validateFile(file: File): { valid: boolean; error?: string } {
  // Check file type
  const isValidType = UPLOAD_CONFIG.ALLOWED_TYPES.includes(file.type);
  const hasValidExtension = UPLOAD_CONFIG.ALLOWED_EXTENSIONS.some(ext =>
    file.name.toLowerCase().endsWith(ext)
  );

  if (!isValidType && !hasValidExtension) {
    return {
      valid: false,
      error: ERROR_MESSAGES.INVALID_FILE_TYPE,
    };
  }

  // Check file size
  if (file.size > UPLOAD_CONFIG.MAX_FILE_SIZE) {
    return {
      valid: false,
      error: ERROR_MESSAGES.FILE_TOO_LARGE,
    };
  }

  return { valid: true };
}

/**
 * Format file size to human-readable string
 * @param bytes - File size in bytes
 * @returns Formatted file size string
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

