import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

# --- Schema para a criação de uma Consulta ---


class ConsultationCreate(BaseModel):
    question_text: str


# --- Schemas para a Resposta do endpoint de Consulta ---


class ExchangeForConsultationResponse(BaseModel):

    id: uuid.UUID
    question_text: str
    answer_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ConsultationResponse(BaseModel):

    id: uuid.UUID
    question_text: str
    user_id: uuid.UUID
    created_at: datetime
    exchanges: List[ExchangeForConsultationResponse] = []

    class Config:
        from_attributes = True




class ConsultationForExchangeResponse(BaseModel):

    id: uuid.UUID
    question_text: str
    user_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class ExchangeResponse(BaseModel):
    id: uuid.UUID
    consultation_id: uuid.UUID
    question_text: str
    answer_text: Optional[str]
    created_at: datetime
    consultation: ConsultationForExchangeResponse

    class Config:
        from_attributes = True

class ExchangeCreate(BaseModel):
    question_text: str