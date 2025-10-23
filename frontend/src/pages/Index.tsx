import { FileSearch } from 'lucide-react';
import { UploadZone } from '@/components/UploadZone';
import { ProgressIndicator } from '@/components/ProgressIndicator';
import { SummaryCard } from '@/components/SummaryCard';
import { DocumentTable } from '@/components/DocumentTable';
import { SummarySection } from '@/components/SummarySection';
import { ExportButton } from '@/components/ExportButton';
import { useToast } from '@/hooks';
import { useAnalysis } from '@/hooks';
import { SUCCESS_MESSAGES, ERROR_MESSAGES } from '@/constants';

/**
 * Main page component for VDR Analysis Tool
 * Orchestrates the document analysis workflow
 */
const Index = () => {
  const { toast } = useToast();
  const { isAnalyzing, progress, result, error, analyzeFile, reset } = useAnalysis();

  /**
   * Handle file selection from upload zone
   */
  const handleFileSelect = async (file: File) => {
    try {
      await analyzeFile(file);
      
      if (result) {
        toast({
          title: SUCCESS_MESSAGES.ANALYSIS_COMPLETE,
          description: `Successfully analyzed ${result.docs.length} documents`,
        });
      }
    } catch (err) {
      toast({
        title: 'Analysis failed',
        description: error || ERROR_MESSAGES.ANALYSIS_FAILED,
        variant: 'destructive',
      });
    }
  };

  /**
   * Handle reset/analyze another file
   */
  const handleReset = () => {
    reset();
    toast({
      title: 'Ready for new upload',
      description: 'You can now upload another file',
    });
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-primary">
              <FileSearch className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-foreground">VDR Analysis Tool</h1>
              <p className="text-sm text-muted-foreground">AI-powered due diligence document analysis</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Upload Section */}
        {!result && !isAnalyzing && (
          <div className="max-w-3xl mx-auto">
            <UploadZone onFileSelect={handleFileSelect} disabled={isAnalyzing} />
          </div>
        )}

        {/* Progress Section */}
        {isAnalyzing && (
          <div className="max-w-3xl mx-auto">
            <ProgressIndicator progress={progress} />
          </div>
        )}

        {/* Results Section */}
        {result && !isAnalyzing && (
          <div className="space-y-8">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <SummaryCard category="financial" data={result.aggregate.financial} />
              <SummaryCard category="legal" data={result.aggregate.legal} />
              <SummaryCard category="commercial" data={result.aggregate.commercial} />
              <SummaryCard category="operations" data={result.aggregate.operations} />
            </div>

            {/* Executive Summary */}
            <SummarySection summaryText={result.summaryText} />

            {/* Document Table */}
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-4">Document Details</h2>
              <DocumentTable documents={result.docs} />
            </div>

            {/* Export Button */}
            <div className="flex justify-center">
              <ExportButton data={result} />
            </div>

            {/* Errors */}
            {result.errors.length > 0 && (
              <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20">
                <h3 className="font-semibold text-destructive mb-2">Processing Errors</h3>
                <ul className="space-y-1 text-sm text-destructive">
                  {result.errors.map((error, idx) => (
                    <li key={idx}>• {error}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Reset Button */}
            <div className="flex justify-center">
              <button
                onClick={handleReset}
                className="text-sm text-muted-foreground hover:text-foreground transition-colors underline"
              >
                Analyze another file
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Index;
