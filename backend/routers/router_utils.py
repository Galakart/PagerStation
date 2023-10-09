"""Роутер - вспомогательное"""
from fastapi import APIRouter, Path

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
)


@router.get("/capcode_to_frame/{capcode}")
def capcode_to_frame(capcode: int = Path(ge=1, le=9999999)):
    """Расчёт фрейма для капкода"""
    return {"frame_number": capcode % 8}
