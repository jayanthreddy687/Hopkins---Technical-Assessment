/**
 * Summary card component for displaying category-level statistics
 */

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, AlertTriangle, FileText, DollarSign, Scale, Briefcase, Settings } from 'lucide-react';
import { formatCount } from '@/utils';
import type { CategoryAggregate, DocumentCategory } from '@/types/vdr';

interface SummaryCardProps {
  category: DocumentCategory;
  data: CategoryAggregate;
}

const categoryConfig = {
  financial: {
    icon: DollarSign,
    label: 'Financial',
    color: 'text-primary',
  },
  legal: {
    icon: Scale,
    label: 'Legal',
    color: 'text-accent',
  },
  commercial: {
    icon: Briefcase,
    label: 'Commercial',
    color: 'text-success',
  },
  operations: {
    icon: Settings,
    label: 'Operations',
    color: 'text-muted-foreground',
  }
};

/**
 * Card component showing facts and red flags for a specific category
 */
export const SummaryCard = ({ category, data }: SummaryCardProps) => {
  const config = categoryConfig[category];
  const Icon = config.icon;

  return (
    <Card className="hover:shadow-lg transition-shadow bg-gradient-card">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {config.label}
        </CardTitle>
        <Icon className={`w-4 h-4 ${config.color}`} />
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          {/* Facts Count */}
          <div 
            className="flex items-center gap-2"
            title={formatCount(data.facts, 'fact', 'facts')}
          >
            <TrendingUp className="w-4 h-4 text-success" />
            <span className="text-2xl font-bold text-foreground">{data.facts}</span>
            <span className="text-sm text-muted-foreground">facts</span>
          </div>
          
          {/* Red Flags Count */}
          <div 
            className="flex items-center gap-2"
            title={formatCount(data.red_flags, 'red flag', 'red flags')}
          >
            <AlertTriangle className="w-4 h-4 text-destructive" />
            <span className="text-2xl font-bold text-foreground">{data.red_flags}</span>
            <span className="text-sm text-muted-foreground">flags</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
