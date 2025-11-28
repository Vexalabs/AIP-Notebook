from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path

router = APIRouter(prefix="/api/models", tags=["models"])

class SampleModel(BaseModel):
    id: str
    name: str
    description: str

@router.get("/list-samples", response_model=List[SampleModel])
async def list_sample_models():
    """
    Lists available sample models by scanning the filesystem.
    """
    try:
        # Establish project root from the current file's location.
        # .../backend/routes/models.py -> .../
        project_root = Path(__file__).parent.parent.parent
        sample_models_dir = project_root / "sample_models"

        if not sample_models_dir.exists():
            return []

        models = []
        for model_dir in sample_models_dir.iterdir():
            if model_dir.is_dir():
                model_id = model_dir.name
                if model_id == "crypto":
                    description = "Predict cryptocurrency prices."
                elif model_id == "soccer":
                    description = "Predict soccer match outcomes."
                else:
                    description = f"A sample model for {model_id}."
                
                models.append(SampleModel(
                    id=model_id,
                    name=model_id.replace("_", " ").title(),
                    description=description
                ))
        return models
    except Exception as e:
        print(f"CRITICAL: An unexpected error occurred while listing sample models: {e}")
        return []
