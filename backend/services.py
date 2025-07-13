from .models import Consultation
from sqlalchemy.orm import Session
from openai import OpenAI
from typing import Optional
from .models import Exchange, Consultation
from uuid import UUID


async def create_new_consultation(db: Session, user_id: UUID, question_text: str):
    db_consultation = Consultation(question_text=question_text, user_id=user_id )
    db.add(db_consultation)
    db.commit()
    db.refresh(db_consultation)
    first_exchange = await create_new_exchange(db=db, consultation_id=db_consultation.id, question_text=question_text, chatHistory=[])
    db.refresh(db_consultation)
    db.refresh(first_exchange)
    return db_consultation


async def ask_question(question_text: str, chatHistory: list):
    client = OpenAI()
    system_prompt = [
        {
            "role": "system",
            "content": "És um médico pediatra altamente qualificado e experiente, com décadas de prática em ajudar pais a compreender e cuidar melhor dos seus filhos. A tua missão é fornecer respostas claras, precisas e empáticas a qualquer questão que os pais possam ter sobre a saúde, desenvolvimento e bem-estar dos seus filhos. Se receberes uma pergunta que não esteja relacionada com pediatria ou com o cuidado infantil, gentilmente pede ao utilizador para reformular a pergunta de modo a que possas oferecer a melhor assistência possível.",
        }
    ]
    updated_chatHistory = (
        system_prompt + chatHistory + [{"role": "user", "content": question_text}]
    )
    response = client.chat.completions.create(
        model="gpt-4.1", messages=updated_chatHistory,
        max_tokens=200,
    )
    return response.choices[0].message.content


async def create_new_exchange(
    db: Session,
    consultation_id: str,
    question_text: str,
    chatHistory: Optional[list] = [],
):
    answer_text = await ask_question(question_text, chatHistory)
    new_exchange = Exchange(
        consultation_id=consultation_id,
        question_text=question_text,
        answer_text=answer_text,
    )
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)
    return new_exchange
