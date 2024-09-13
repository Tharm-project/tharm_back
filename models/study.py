from datetime import datetime
from firebase_set import db

class StudyModel:
    #모델 인스턴트 초기화(새로운 사용자 객체 생성)
    def __init__(self, id: str, user_id:str, name:str, summary:str, status:float, created_at:datetime):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.summary = summary
        self.status = status
        self.created_at = created_at

    #Firestore에서 가져온 문서 데이터를 Python 객체로 변환
    @staticmethod
    def from_firestore(doc):
        data = doc.to_dict()
        return StudyModel(
            id = doc.id,
            user_id = doc.get('user_id'),
            name=data.get('name'),
            summary=doc.summary,
            status=doc.status,
            created_at=data.get('created_at')
        )
    #모델의 속성을 딕셔너리 형태로 변환함
    def to_dict(self):
        return {
            'name': self.name,
            'summary': self.summary,
            'status': self.status,
            'created_at': self.created_at
        }    

    def save(self):
        doc_ref = db.collection('study').document(self.id)
        doc_ref.set(self.to_dict())
    
    @staticmethod
    def get(study_id: str): 
        doc_ref = db.collection('study').document(study_id)
        ref = doc_ref.get()
        if ref.exists:
            return StudyModel.from_firestore(ref)
        else:
            raise ValueError('Study not found')