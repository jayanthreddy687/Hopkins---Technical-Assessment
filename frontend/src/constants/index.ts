/**
 * Application constants and configuration
 */

export const API_CONFIG = {
  BASE_URL: '/api',
  ENDPOINTS: {
    ANALYSE: '/analyse',
    EXPORT: '/export',
  },
  TIMEOUT: 300000, // 5 minutes
} as const;

export const UPLOAD_CONFIG = {
  MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
  ALLOWED_TYPES: ['application/zip', 'application/x-zip-compressed'],
  ALLOWED_EXTENSIONS: ['.zip'],
} as const;

export const CATEGORY_CONFIG = {
  financial: {
    label: 'Financial',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
    icon: '💰',
  },
  legal: {
    label: 'Legal',
    color: 'text-purple-600',
    bgColor: 'bg-purple-50',
    icon: '⚖️',
  },
  commercial: {
    label: 'Commercial',
    color: 'text-green-600',
    bgColor: 'bg-green-50',
    icon: '📊',
  },
  operations: {
    label: 'Operations',
    color: 'text-orange-600',
    bgColor: 'bg-orange-50',
    icon: '⚙️',
  },
  other: {
    label: 'Other',
    color: 'text-gray-600',
    bgColor: 'bg-gray-50',
    icon: '📄',
  },
} as const;

export const ANALYSIS_STAGES = {
  UPLOADING: {
    label: 'Uploading',
    message: 'Uploading and extracting...',
    progress: 20,
  },
  EXTRACTING: {
    label: 'Extracting',
    message: 'Extracting documents...',
    progress: 40,
  },
  ANALYZING: {
    label: 'Analyzing',
    message: 'Analysing documents...',
    progress: 70,
  },
  COMPLETE: {
    label: 'Complete',
    message: 'Analysis complete!',
    progress: 100,
  },
} as const;

export const ERROR_MESSAGES = {
  INVALID_FILE_TYPE: 'Please upload a valid ZIP file',
  UPLOAD_FAILED: 'Failed to upload file. Please try again.',
  ANALYSIS_FAILED: 'Failed to analyze documents. Please try again.',
  EXPORT_FAILED: 'Failed to export report. Please try again.',
  NETWORK_ERROR: 'Network error. Please check your connection.',
  FILE_TOO_LARGE: 'File size exceeds the maximum limit of 100MB',
} as const;

export const SUCCESS_MESSAGES = {
  ANALYSIS_COMPLETE: 'Analysis completed successfully',
  EXPORT_COMPLETE: 'Report exported successfully',
} as const;

