# VDR Lite + LLM

An AI-powered virtual data room document analysis tool that leverages Google's Gemini API to extract key facts and identify red flags from due diligence documents. Built as a full-stack application with FastAPI and React.

## Overview

This application streamlines the due diligence process by automatically analyzing uploaded documents and generating structured insights. It processes various document formats, categorizes them intelligently, and produces comprehensive reports highlighting critical information for investment committees.

## Demo

### Video Demo
Watch the full demo video: [View Demo Video](https://drive.google.com/file/d/1_SVWTEbiwACt9SPpqF_6Q2EIQdZ_jyEl/view?usp=sharing)

### Quick Demo
![VDR Lite Demo](demo.gif)

### Key Features

- **Multi-format Document Processing**: Supports PDF, DOCX, XLSX, CSV, and TXT files
- **AI-Powered Analysis**: Uses Google's Gemini API to extract facts and identify red flags
- **Smart Categorization**: Automatically categorizes documents into Financial, Legal, Commercial, Operations, or Other
- **Executive Summary**: Generates IC-ready summaries with grouped insights by category
- **Interactive UI**: Modern, responsive interface built with React and shadcn/ui
- **Export Functionality**: Downloads complete analysis reports in Markdown format
- **Real-time Progress**: Visual feedback during upload, extraction, and analysis stages
- **Error Handling**: Graceful degradation with detailed error reporting

## Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **LLM Provider**: Google Generative AI (Gemini 2.5 Flash Lite)
- **Document Processing**: pypdf, python-docx, openpyxl, pandas
- **Validation**: Pydantic v2 with strict schema validation
- **Architecture**: Clean service-layer architecture with dependency injection

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **UI Components**: shadcn/ui (Radix UI primitives)
- **Styling**: TailwindCSS
- **State Management**: React Query (TanStack Query)
- **Routing**: React Router v6

## Getting Started

### Prerequisites

- Python 3.13 or higher
- Node.js 18+ and npm (or Bun)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

#### 1. Clone the repository

```bash
git clone <repository-url>
cd test
```

#### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional - API key is included for demo)
export GEMINI_API_KEY="your-api-key-here"
```

#### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
# or
bun install
```

### Running the Application

You'll need two terminal windows:

#### Terminal 1: Start the Backend

```bash
cd backend
source venv/bin/activate  # If not already activated
python main.py
```

The API will start at `http://localhost:8000`

#### Terminal 2: Start the Frontend

```bash
cd frontend
npm run dev
# or
bun dev
```

The UI will be available at `http://localhost:5173`

### Verify Installation

1. Open your browser to `http://localhost:5173`
2. You should see the VDR Analysis Tool interface
3. The backend API docs are available at `http://localhost:8000/docs`

## Usage Guide

### Basic Workflow

1. **Upload Documents**: 
   - Click the upload zone or drag-and-drop a ZIP file containing your documents
   - Maximum file size: 25 MB
   - Supported document types: PDF, DOCX, XLSX, XLS, CSV, TXT

2. **Processing**:
   - The app extracts text from each document (truncated to 15,000 characters)
   - Documents are automatically categorized based on content
   - Each document is analyzed by Gemini to extract facts and identify red flags
   - An executive summary is generated from all analyses

3. **Review Results**:
   - View summary cards showing aggregate counts by category
   - Read the AI-generated executive summary
   - Expand the document table to see details for each file
   - Check key facts and red flags for individual documents

4. **Export**:
   - Click "Download Summary" to get a comprehensive Markdown report
   - The report includes the executive summary, aggregated data, and per-document details

### API Endpoints

#### `POST /api/analyse`
Upload and analyze a ZIP file containing documents.

**Request**: Multipart form-data with `file` field

**Response**:
```json
{
  "docs": [
    {
      "doc": "filename.pdf",
      "category": "financial",
      "facts": ["Revenue grew 25% YoY", "EBITDA margin is 32%"],
      "red_flags": ["Working capital deficit of $2M", "Auditor qualified opinion"]
    }
  ],
  "aggregate": {
    "financial": {"facts": 5, "red_flags": 2},
    "legal": {"facts": 3, "red_flags": 1}
  },
  "summaryText": "Executive summary...",
  "errors": []
}
```

#### `POST /api/export`
Generate and download a Markdown report.

**Request**: JSON body with analysis data (same structure as `/api/analyse` response)

**Response**: File download (`vdr_summary.md`)

## Project Structure

```
.
├── backend/
│   ├── api/
│   │   ├── routes.py          # API endpoint definitions
│   │   └── dependencies.py    # Dependency injection
│   ├── config/
│   │   └── settings.py        # Configuration management
│   ├── core/
│   │   ├── constants.py       # Enums, prompts, keywords
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── logging.py         # Logging configuration
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── analysis_service.py    # Orchestrates analysis workflow
│   │   ├── document_service.py    # Text extraction & categorization
│   │   ├── llm_service.py         # Gemini API integration
│   │   └── export_service.py      # Report generation
│   ├── utils/
│   │   ├── file_utils.py      # File handling utilities
│   │   └── text_utils.py      # Text processing utilities
│   └── main.py                # Application entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/            # shadcn/ui components
│   │   │   ├── DocumentTable.tsx
│   │   │   ├── ExportButton.tsx
│   │   │   ├── ProgressIndicator.tsx
│   │   │   ├── SummaryCard.tsx
│   │   │   ├── SummarySection.tsx
│   │   │   └── UploadZone.tsx
│   │   ├── hooks/
│   │   │   ├── useAnalysis.ts     # Analysis workflow hook
│   │   │   └── useExport.ts       # Export functionality hook
│   │   ├── services/
│   │   │   └── api.service.ts     # API client
│   │   ├── types/
│   │   │   └── vdr.ts             # TypeScript interfaces
│   │   ├── pages/
│   │   │   └── Index.tsx          # Main page
│   │   └── App.tsx
│   └── package.json
│
└── sample_pe_dataroom_pack.zip    # Sample documents for testing
```

## Architecture Highlights

### Backend Architecture

The backend follows clean architecture principles with clear separation of concerns:

- **API Layer**: FastAPI routes handle HTTP requests/responses
- **Service Layer**: Business logic separated into focused services
  - `AnalysisService`: Orchestrates the complete workflow
  - `DocumentService`: Handles text extraction and categorization
  - `LLMService`: Manages Gemini API interactions with retry logic
  - `ExportService`: Generates formatted reports
- **Models Layer**: Pydantic schemas for validation and serialization
- **Utils Layer**: Reusable utilities for file and text operations

### LLM Integration

The application uses a two-phase LLM approach:

1. **Per-Document Analysis**: Each document gets a structured analysis with temperature=0 for consistency
   - Extracts 1-5 key facts
   - Identifies 0-5 red flags
   - Enforces strict JSON schema validation
   - Automatic retry with simplified prompt on parse errors

2. **Executive Summary**: Final narrative generated from all document analyses
   - 300-400 word IC-ready summary
   - Groups insights by category
   - References specific counts and cross-document patterns

### Frontend Architecture

- **Component-Based**: Modular React components with clear responsibilities
- **Type Safety**: Full TypeScript coverage with strict mode
- **State Management**: React Query for server state, React hooks for UI state
- **Styling**: Utility-first with TailwindCSS and custom design tokens
- **Accessibility**: Built on Radix UI primitives with ARIA support

## Configuration

### Environment Variables

The backend can be configured via environment variables or `.env` file:

```bash
# LLM Configuration
GEMINI_API_KEY=your-api-key-here
```

### Customization Points

- **Category Keywords**: Modify `CATEGORY_KEYWORDS` in `backend/core/constants.py` to adjust categorization logic
- **LLM Prompts**: Update prompt templates in `backend/core/constants.py` to fine-tune analysis output
- **Document Types**: Extend `DocumentService` to support additional file formats
- **UI Theming**: Customize TailwindCSS configuration in `frontend/tailwind.config.ts`

## Error Handling

The application includes comprehensive error handling:

- **File Validation**: Size limits, format checks, ZIP extraction errors
- **LLM Failures**: Automatic retry logic, graceful degradation
- **Parse Errors**: JSON validation with fallback strategies
- **User Feedback**: Clear error messages in the UI with contextual information

## Performance Considerations

- Text truncation to 15,000 characters per document limits token usage
- Excel/CSV files limited to 200 rows for faster processing
- Concurrent document processing for improved throughput
- Temporary file cleanup after processing
- Optimized LLM token limits (700 for docs, 500 for summary)

## Testing

The application includes a sample data pack in `sample_pe_dataroom_pack.zip` for testing the complete workflow.

To test:
1. Start both backend and frontend
2. Upload the sample ZIP file
3. Verify that documents are analyzed and categorized correctly
4. Check the executive summary for coherent insights
5. Export and review the Markdown report

## Known Limitations

- Maximum ZIP file size: 25 MB
- PDF text extraction may struggle with scanned documents (no OCR)
- Complex Excel spreadsheets are flattened to text (formulas not evaluated)
- LLM analysis quality depends on document text clarity
- Processing time scales linearly with document count (~10-20 docs in 2-3 minutes)

## Troubleshooting

### Backend won't start
- Verify Python 3.13+ is installed: `python --version`
- Check virtual environment is activated
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Verify Gemini API key is valid

### Frontend won't start
- Check Node.js version: `node --version` (should be 18+)
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check for port conflicts on 5173

### Analysis fails
- Check backend logs for specific error messages
- Verify Gemini API quota hasn't been exceeded
- Ensure uploaded ZIP file is not corrupted
- Check document formats are supported

### Slow processing
- Large PDFs take longer to process
- Many documents (20+) will increase processing time
- Network latency affects LLM API calls
- Consider reducing document count or file sizes

## Future Enhancements

Potential improvements for production deployment:

- Background job processing with Celery or RQ
- Database persistence for analysis history
- User authentication and multi-tenancy
- Batch processing optimization
- OCR support for scanned PDFs
- Real-time WebSocket progress updates
- Advanced filtering and search in results
- Custom prompt templates via UI
- PDF report export option
- Comparison mode for multiple data room analyses

