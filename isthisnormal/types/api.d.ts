export interface User {
  id: string;
  email: string;
}

export interface Consultation {
  id: string;
  question_text: string;
  user_id: string;
  created_at: string;
  exchanges: Exchange[];
}

export interface Exchange {
  id: string;
  question_text: string;
  answer_text: string | null;
  created_at: string;
}

export interface ConsultationCreate {
  question_text: string;
}

export interface ExchangeCreate {
  question_text: string;
}
