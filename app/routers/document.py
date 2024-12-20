from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Document
from app.services.file_upload import save_file

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/")
async def upload_document(
    customer_id: int = Form(...),
    document_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = await save_file(file)
    if not file_path:
        raise HTTPException(status_code=500, detail="File upload failed")

    db_document = Document(customer_id=customer_id, document_type=document_type, document_path=file_path)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return {"message": "Document uploaded successfully", "document": db_document}