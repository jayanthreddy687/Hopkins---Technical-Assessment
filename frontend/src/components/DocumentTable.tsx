import { useState } from 'react';
import { ChevronDown, ChevronRight, CheckCircle, AlertCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import type { DocumentResult } from '@/types/vdr';

interface DocumentTableProps {
  documents: DocumentResult[];
}

export const DocumentTable = ({ documents }: DocumentTableProps) => {
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const toggleRow = (docName: string) => {
    setExpandedRows((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(docName)) {
        newSet.delete(docName);
      } else {
        newSet.add(docName);
      }
      return newSet;
    });
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      financial: 'bg-primary/10 text-primary',
      legal: 'bg-accent/10 text-accent',
      commercial: 'bg-success/10 text-success',
      operations: 'bg-muted text-muted-foreground',
      other: 'bg-muted text-muted-foreground',
    };
    return colors[category as keyof typeof colors] || colors.other;
  };

  return (
    <div className="rounded-lg border border-border overflow-hidden bg-card shadow-card">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-muted/50 border-b border-border">
            <tr>
              <th className="px-4 py-3 text-left text-sm font-semibold text-foreground w-12"></th>
              <th className="px-4 py-3 text-left text-sm font-semibold text-foreground">Document</th>
              <th className="px-4 py-3 text-left text-sm font-semibold text-foreground">Category</th>
              <th className="px-4 py-3 text-center text-sm font-semibold text-foreground">Facts</th>
              <th className="px-4 py-3 text-center text-sm font-semibold text-foreground">Red Flags</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => {
              const isExpanded = expandedRows.has(doc.doc);
              return (
                <>
                  <tr
                    key={doc.doc}
                    className="border-b border-border hover:bg-muted/20 cursor-pointer transition-colors"
                    onClick={() => toggleRow(doc.doc)}
                  >
                    <td className="px-4 py-3">
                      {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-muted-foreground" />
                      ) : (
                        <ChevronRight className="w-4 h-4 text-muted-foreground" />
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm text-foreground font-medium">{doc.doc}</td>
                    <td className="px-4 py-3">
                      <Badge variant="outline" className={getCategoryColor(doc.category)}>
                        {doc.category}
                      </Badge>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="inline-flex items-center gap-1 text-success font-semibold">
                        <CheckCircle className="w-4 h-4" />
                        {doc.facts.length}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className="inline-flex items-center gap-1 text-destructive font-semibold">
                        <AlertCircle className="w-4 h-4" />
                        {doc.red_flags.length}
                      </span>
                    </td>
                  </tr>
                  {isExpanded && (
                    <tr className="border-b border-border bg-muted/10">
                      <td colSpan={5} className="px-4 py-4">
                        <div className="grid md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="font-semibold text-sm text-success mb-2 flex items-center gap-2">
                              <CheckCircle className="w-4 h-4" />
                              Key Facts
                            </h4>
                            <ul className="space-y-1 text-sm text-foreground">
                              {doc.facts.length > 0 ? (
                                doc.facts.map((fact, idx) => (
                                  <li key={idx} className="flex items-start gap-2">
                                    <span className="text-muted-foreground">•</span>
                                    <span>{fact}</span>
                                  </li>
                                ))
                              ) : (
                                <li className="text-muted-foreground italic">No facts extracted</li>
                              )}
                            </ul>
                          </div>
                          <div>
                            <h4 className="font-semibold text-sm text-destructive mb-2 flex items-center gap-2">
                              <AlertCircle className="w-4 h-4" />
                              Red Flags
                            </h4>
                            <ul className="space-y-1 text-sm text-foreground">
                              {doc.red_flags.length > 0 ? (
                                doc.red_flags.map((flag, idx) => (
                                  <li key={idx} className="flex items-start gap-2">
                                    <span className="text-destructive">•</span>
                                    <span>{flag}</span>
                                  </li>
                                ))
                              ) : (
                                <li className="text-muted-foreground italic">No red flags identified</li>
                              )}
                            </ul>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
