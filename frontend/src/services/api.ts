const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export type Question = {
  id: number;
  concept_id: number;
  question_text: string;
  question_type: string;
  difficulty: number;
  options?: Record<string, string> | null;
  correct_answer?: string | null;
  explanation?: string | null;
};

export type AttemptPayload = {
  user_id: number;
  question_id: number;
  answer: string;
  is_correct: boolean;
  time_taken: number;
  confidence?: number | null;
};

export type AdaptiveResult = {
  action?: string;
  reason?: string;
  priority?: number;
  next_question_id?: number | null;
  mastery?: number;
  confidence?: number;
  revision_need?: number;
  [key: string]: unknown;
};

export type AttemptResponse = {
  id?: number;
  user_id?: number;
  question_id?: number;
  answer?: string;
  is_correct?: boolean;
  time_taken?: number;
  confidence?: number | null;

  adaptive_result?: AdaptiveResult | null;

  [key: string]: unknown;
};

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();

    throw new Error(
      text || `API request failed with status ${response.status}`
    );
  }

  return response.json();
}

export async function getQuestion(
  questionId: number
): Promise<Question> {
  return request<Question>(`/questions/${questionId}`);
}

export async function getQuestions(): Promise<Question[]> {
  return request<Question[]>("/questions/");
}

export async function submitAttempt(
  payload: AttemptPayload
): Promise<AttemptResponse> {
  return request<AttemptResponse>("/attempts/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}