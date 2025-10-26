from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.services.openai_service import openai_service
from app.services.database_service import db_service
from app.models.schemas import ExpenseCreate, UploadResponse, ExpenseSummary
from app.core.security import validate_file_upload
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=ExpenseSummary)
async def get_expenses():
    """
    Get all expenses with summary
    """
    try:
        expenses = db_service.get_all_expenses()
        summary = db_service.get_expense_summary()
        
        return ExpenseSummary(
            total_expenses=summary["total_amount"],
            expense_count=summary["expense_count"],
            recent_expenses=expenses
        )
        
    except Exception as e:
        logger.error("Get expenses error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch expenses"
        ) from e

@router.post("/upload", response_model=UploadResponse)
async def upload_receipt(file: UploadFile = File(...)):
    """
    Upload a receipt image for processing
    """
    try:
        # Validate file
        await validate_file_upload(
            file_size=file.size or 0,
            content_type=file.content_type or ""
        )
        
        # Read image data
        image_data = await file.read()
        logger.info("Processing image: %s, size: %s bytes", file.filename, len(image_data))
        
        # Extract data using OpenAI
        extracted_data = await openai_service.extract_expense_data(image_data)
        
        # Create expense object
        expense_data = ExpenseCreate(**extracted_data)
        
        # Save to database
        expense_id = db_service.create_expense(expense_data)
        
        return UploadResponse(
            success=True,
            expense_id=expense_id,
            message="Receipt processed successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Upload error: %s", str(e))
        return UploadResponse(
            success=False,
            error=str(e)
        )

@router.get("/health")
async def health_check():
    """Simple health check"""
    return {"status": "healthy", "database": "sqlite"}