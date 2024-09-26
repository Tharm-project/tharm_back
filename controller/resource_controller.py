import io
import re
from datetime import datetime, timezone
from kiwipiepy import Kiwi
import pdfplumber
from pydantic import ValidationError
from firebase_set import db
from models.resource import ResourceModel
from schemas.schemas import ResourceSchema
from fastapi import HTTPException
import pdfplumber 

class ResourceController:
    def __init__(self):
        self.model = ResourceModel()
        self.kiwi = Kiwi()

    def process_file(self, user_id: str, study_id: str, file_content: bytes, file_name: str) -> ResourceSchema:
        try:
            # PDF 파일에서 텍스트 추출
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                #텍스트가 없거나 페이지가 비어있으면 에러 출력
                if len(pdf.pages) == 0:
                    raise HTTPException(status_code=400, detail="pdf에 페이지가 없음")
                
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            
            # 텍스트가 비어있는지 확인
            if not text.strip():
                raise HTTPException(status_code=400, detail="null임둥~")

            # 텍스트를 문장 단위로 나누기
            sentences = [sent.text for sent in self.kiwi.split_into_sents(text)]
            # sentences = kiwi.split_into_sents(text, return_tokens=False)
            # 문장이 추출되지 않은 경우 확인
            if not sentences:
                raise HTTPException(status_code=400, detail="추출된 문장이 없음! 오류확인 ㄱㄱ")

            # 한글 깨짐 유무 체크 (예: 한글 문장 포함 여부)
            if any([not re.search(r'[\uac00-\ud7af]', sentence) for sentence in sentences]):
                raise HTTPException(status_code=400, detail="한국어 인코딩 문제 확인")
            
            # Resource 문서 생성
            doc_ref = db.collection('resource').document()

            # Resource 데이터를 저장
            resource_id = doc_ref.id
            resource = ResourceSchema(
                id=resource_id,
                user_id=user_id,
                study_id=study_id,
                url=file_name,
                sentence={"data": sentences},
                total=len(sentences),
                last_idx=len(sentences) - 1,
                created_at=datetime.now(timezone.utc)
            )
            self.model.add_resource(resource)
            return resource
        
        # except pdfplumber.PDFSyntaxError:
        #     raise HTTPException(status_code=400, detail="pdf 파일 구문 에러")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str("예외 처리된 에러 확인: ",e))
