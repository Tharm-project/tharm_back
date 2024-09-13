from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from firebase_set import db
from controller import resource_controller
from uuid import uuid4

router = APIRouter()
resourceController = resource_controller.ResourceController()

#파일 업로드
#pdf 파일 업로드 기능 구현 -> 문장 추출 -> 오차율 확인 및 저장 구현하기
@router.post("/resources/")
async def create_resource(user_id: uuid4, study_id: uuid4, file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="파일 타입이 안맞당")
    
    file_content = await file.read()
    resource = resourceController.process_file(user_id, study_id, file_content, file.filename)
    
    return resource, {"message":"업로드 완료"}