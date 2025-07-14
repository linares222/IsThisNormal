import json
from .models import Consultation
from sqlalchemy.orm import Session
from openai import OpenAI
from typing import Optional, Dict, Any
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


async def ask_question(question_text: str, chatHistory: list) -> Dict[str, Any]:
    client = OpenAI()
    system_prompt = [
        {
            "role": "system",
            "content": """És um médico pediatra altamente qualificado e experiente, com décadas de prática em ajudar pais a compreender e cuidar melhor dos seus filhos. 

A tua missão é fornecer respostas claras, precisas e empáticas a qualquer questão que os pais possam ter sobre a saúde, desenvolvimento e bem-estar dos seus filhos.

IMPORTANTE: Deves sempre responder em formato JSON com a seguinte estrutura:
{
  "answer": "tua resposta médica detalhada aqui",
  "checkPediatrician": true/false
}

- "answer": A tua resposta médica completa e empática, com um máximo de 300 tokens
- "checkPediatrician": true se a situação requer consulta médica presencial urgente ou se há sinais de alarme, false caso contrário

Critérios para checkPediatrician = true:
- Febre alta persistente
- Dificuldade respiratória
- Sinais de desidratação
- Vómitos persistentes
- Lesões graves
- Qualquer sintoma que consideres preocupante

Se receberes uma pergunta que não esteja relacionada com pediatria, pede gentilmente para reformular.""",
        }
    ]
    updated_chatHistory = (
        system_prompt + chatHistory + [{"role": "user", "content": question_text}]
    )
    
    response = client.chat.completions.create(
        model="gpt-4.1",  
        messages=updated_chatHistory,
        max_tokens=300,
        temperature=0.7,
    )
    
    try:    
        ai_response = response.choices[0].message.content
        parsed_response = json.loads(ai_response)
        
        if "answer" not in parsed_response or "checkPediatrician" not in parsed_response:
            raise ValueError("Estrutura JSON inválida")
            
        return parsed_response
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Erro ao parsear resposta da AI: {e}")
        return {
            "answer": response.choices[0].message.content,
            "checkPediatrician": False
        }


async def create_new_exchange(
    db: Session,
    consultation_id: str,
    question_text: str,
    chatHistory: Optional[list] = [],
):
    ai_response = await ask_question(question_text, chatHistory)
    
    new_exchange = Exchange(
        consultation_id=consultation_id,
        question_text=question_text,
        answer_text=ai_response["answer"],
        check_pediatrician=ai_response["checkPediatrician"],
    )
    db.add(new_exchange)
    db.commit()
    db.refresh(new_exchange)
    return new_exchange
