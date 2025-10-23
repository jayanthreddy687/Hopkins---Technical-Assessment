/**
 * Formatting utility functions
 */

import { CATEGORY_CONFIG } from '@/constants';
import type { DocumentCategory } from '@/types/vdr';

/**
 * Get category display configuration
 * @param category - Document category
 * @returns Category configuration with label, color, and icon
 */
export function getCategoryConfig(category: DocumentCategory) {
  return CATEGORY_CONFIG[category] || CATEGORY_CONFIG.other;
}

/**
 * Format count with label
 * @param count - Number to format
 * @param singular - Singular label
 * @param plural - Plural label
 * @returns Formatted count string
 */
export function formatCount(
  count: number,
  singular: string,
  plural: string
): string {
  return `${count} ${count === 1 ? singular : plural}`;
}

/**
 * Truncate text to specified length
 * @param text - Text to truncate
 * @param maxLength - Maximum length
 * @returns Truncated text with ellipsis if needed
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

/**
 * Format timestamp to readable date string
 * @param timestamp - Date timestamp
 * @returns Formatted date string
 */
export function formatDate(timestamp: number | Date): string {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

