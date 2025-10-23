/**
 * Type definitions for VDR Analysis application
 */

export type DocumentCategory = 'financial' | 'legal' | 'commercial' | 'operations' | 'other';

export type AnalysisStatus = 'uploading' | 'extracting' | 'analyzing' | 'complete' | 'error';

export interface DocumentResult {
  doc: string;
  category: DocumentCategory;
  facts: string[];
  red_flags: string[];
}

export interface CategoryAggregate {
  facts: number;
  red_flags: number;
}

export interface AggregateData {
  financial: CategoryAggregate;
  legal: CategoryAggregate;
  commercial: CategoryAggregate;
  operations: CategoryAggregate;
  other: CategoryAggregate;
}

export interface AnalysisResult {
  docs: DocumentResult[];
  aggregate: AggregateData;
  summaryText: string;
  errors: string[];
}

export interface UploadProgress {
  current: number;
  total: number;
  status: AnalysisStatus;
  message?: string;
}

/**
 * API Response types
 */
export interface ApiErrorResponse {
  error: string;
  details?: string;
  error_code?: string;
}

/**
 * Component prop types
 */
export interface CategoryCardData {
  category: DocumentCategory;
  data: CategoryAggregate;
}
