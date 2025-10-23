"""API route definitions."""

import os
import tempfile
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse

from core.logging import get_logger
from core.exceptions import FileValidationError, VDRException
from models.schemas import AnalysisResponse
from services import AnalysisService, ExportService
from utils.file_utils import extract_zip_file
from api.dependencies import get_analysis_service, get_export_service

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["analysis"])


@router.get("/")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status message
    """
    return {"message": "VDR Lite + LLM API is running", "status": "healthy"}


@router.post("/analyse", response_model=AnalysisResponse)
async def analyse_documents(
    file: UploadFile = File(...),
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    """
    Upload and analyze documents from a ZIP file.
    
    Args:
        file: Uploaded ZIP file containing documents
        analysis_service: Injected analysis service
        
    Returns:
        Complete analysis response with document details and summary
        
    Raises:
        HTTPException: If file validation or processing fails
    """
    logger.info(f"Received file upload: {file.filename}")
    
    # Validate file type
    if not file.filename or not file.filename.endswith('.zip'):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(
            status_code=400,
            detail="Only ZIP files are allowed"
        )
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        logger.info("Created temporary directory for extraction")
        
        try:
            # Save uploaded file
            zip_path = os.path.join(temp_dir, file.filename)
            with open(zip_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            logger.info(f"Saved uploaded file ({len(content)} bytes)")
            
            # Extract ZIP file
            extract_dir = os.path.join(temp_dir, "extracted")
            extracted_files = extract_zip_file(zip_path, extract_dir)
            
            logger.info(f"Extracted {len(extracted_files)} files")
            
            # Analyze documents
            result = await analysis_service.analyze_directory(extract_dir)
            
            logger.info(
                f"Analysis complete: {len(result.docs)} documents, "
                f"{len(result.errors)} errors"
            )
            
            return result
            
        except FileValidationError as e:
            logger.error(f"File validation error: {e.message}")
            raise HTTPException(status_code=400, detail=e.message)
            
        except VDRException as e:
            logger.error(f"VDR processing error: {e.message}")
            raise HTTPException(
                status_code=500,
                detail=f"Processing error: {e.message}"
            )
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred during processing"
            )


@router.post("/export")
async def export_summary(
    analysis_data: AnalysisResponse,
    export_service: ExportService = Depends(get_export_service)
):
    """
    Export analysis results as a Markdown file.
    
    Args:
        analysis_data: Complete analysis response data
        export_service: Injected export service
        
    Returns:
        FileResponse containing the Markdown report
    """
    logger.info("Generating export report")
    
    try:
        # Generate markdown content
        markdown_content = export_service.generate_markdown_report(analysis_data)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.md',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(markdown_content)
            temp_file = f.name
        
        logger.info(f"Export report saved to {temp_file}")
        
        return FileResponse(
            temp_file,
            media_type='text/markdown',
            filename='vdr_summary.md',
            headers={
                "Content-Disposition": "attachment; filename=vdr_summary.md"
            }
        )
        
    except Exception as e:
        logger.error(f"Export error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate export report"
        )

