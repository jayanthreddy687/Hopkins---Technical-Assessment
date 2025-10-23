import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface SummarySectionProps {
  summaryText: string;
}

export const SummarySection = ({ summaryText }: SummarySectionProps) => {
  return (
    <Card className="shadow-lg bg-gradient-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <FileText className="w-5 h-5 text-primary" />
          Executive Summary
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="prose prose-sm max-w-none text-foreground">
          <ReactMarkdown
            components={{
              // Style the markdown elements
              h1: ({ children }) => <h1 className="text-2xl font-bold mb-4 mt-6">{children}</h1>,
              h2: ({ children }) => <h2 className="text-xl font-bold mb-3 mt-5">{children}</h2>,
              h3: ({ children }) => <h3 className="text-lg font-semibold mb-2 mt-4">{children}</h3>,
              p: ({ children }) => <p className="mb-3 leading-relaxed">{children}</p>,
              ul: ({ children }) => <ul className="list-disc pl-6 mb-3 space-y-1">{children}</ul>,
              ol: ({ children }) => <ol className="list-decimal pl-6 mb-3 space-y-1">{children}</ol>,
              li: ({ children }) => <li className="leading-relaxed">{children}</li>,
              strong: ({ children }) => <strong className="font-semibold text-foreground">{children}</strong>,
              em: ({ children }) => <em className="italic">{children}</em>,
            }}
          >
            {summaryText}
          </ReactMarkdown>
        </div>
      </CardContent>
    </Card>
  );
};
