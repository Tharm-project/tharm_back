from fastapi import APIRouter, HTTPException
from firebase_set import db

router = APIRouter()

@router.get("/{user_id}")
def get_study_progress(user_id: str):
    try:
        study_ref = db.collection('study').filter('user_id', '==', user_id)
        study_docs = study_ref.stream()

        study_list = []
        for doc in study_docs:
            study_data = doc.to_dict()
            study_data['id'] = doc.id
            study_list.append(study_data)

        return {"studies": study_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching study data: {str(e)}")

@router.delete("/delete")
def delete_study(study_ids: list[str]):
    try:
        study_ref = db.collection('study')
        for study_id in study_ids:
            study_ref.document(study_id).delete()

        return {"message": f"Deleted {len(study_ids)} studies successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting studies: {str(e)}")
