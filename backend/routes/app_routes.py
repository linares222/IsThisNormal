from fastapi import APIRouter, Request
from ..schemas import ConsultationCreate, ConsultationResponse, ExchangeResponse, ExchangeCreate
from ..database import get_db
from ..auth import get_current_user_from_cookie
from ..services import create_new_consultation, create_new_exchange
from ..models import Consultation, Exchange
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
import uuid

router = APIRouter()


@router.post("/consultations", response_model=ConsultationResponse)
async def create_consultation(
    consultation: ConsultationCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(request)
    user_id = current_user.get("sub")
    
    first_exchange = await create_new_consultation(
        db=db, user_id=user_id, question_text=consultation.question_text
    )
    return first_exchange


@router.get("/consultations", response_model=list[ConsultationResponse])
async def get_consultations(
    request: Request,
    db: Session = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(request)
    user_id = current_user.get("sub")
    
    return db.query(Consultation).filter(Consultation.user_id == user_id).all()


@router.get("/consultations/{consultation_id}", response_model=ConsultationResponse)
async def get_consultation(
    consultation_id: str,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(request)
    user_id = current_user.get("sub")
    
    consultation_id = uuid.UUID(consultation_id)
    consultation = (
        db.query(Consultation)
        .filter(Consultation.user_id == user_id)
        .filter(Consultation.id == consultation_id)
        .first()
    )

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    return consultation


@router.post("/consultations/{consultation_id}/exchanges", response_model=ExchangeResponse)
async def create_exchange(
    consultation_id: str,
    exchange: ExchangeCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user = await get_current_user_from_cookie(request)
    user_id = current_user.get("sub")
    
    consultation_id = uuid.UUID(consultation_id)
    consultation = (
        db.query(Consultation)
        .filter(
            Consultation.id == consultation_id, Consultation.user_id == user_id
        )
        .first()
    )

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    exchanges = (
        db.query(Exchange)
        .filter(Exchange.consultation_id == consultation_id)
        .order_by(Exchange.created_at)
        .all()
    )
    chatHistory = []
    for ex in exchanges:
        chatHistory.append({"role": "user", "content": ex.question_text})
        if ex.answer_text:
            chatHistory.append({"role": "assistant", "content": ex.answer_text})
    new_exchange = await create_new_exchange(
        db=db,
        consultation_id=consultation_id,
        question_text=exchange.question_text,
        chatHistory=chatHistory,
    )
    return new_exchange