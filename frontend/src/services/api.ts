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

export type LearnerState = {
  id: number;
  user_id: number;
  concept_id: number;
  mastery: number;
  confidence: number;
  attempts_count: number;
  correct_count: number;
  last_attempt_at: string | null;
  updated_at: string;
};

export type Recommendation = {
  concept_id: number | null;
  reason: string | null;
};

export type Attempt = {
  id: number;
  user_id: number;
  question_id: number;
  answer: string;
  is_correct: boolean;
  time_taken: number | null;
  confidence: number | null;
  created_at: string;
};

export type AdaptiveResult = {
  action: string;
  concept_id: number | null;
  priority: number;
  reason: string;
  mastery: number;
  confidence: number;
  revision_need: number;
  misconception_severity: number;
  prerequisites_ready: boolean;
  next_question_id: number | null;
};

export type AttemptResponse = {
  attempt_id: number;
  user_id: number;
  question_id: number;
  is_correct: boolean;
  created_at: string;

  action: string;
  concept_id: number | null;
  priority: number;
  reason: string;

  mastery: number;
  confidence: number;
  revision_need: number;
  misconception_severity: number;
  prerequisites_ready: boolean;

  next_question_id: number | null;
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


/* =========================================================
   Questions
   ========================================================= */

export async function getQuestion(
  questionId: number
): Promise<Question> {
  return request<Question>(`/questions/${questionId}`);
}

export async function getQuestions(): Promise<Question[]> {
  return request<Question[]>("/questions/");
}


/* =========================================================
   Attempts
   ========================================================= */

export async function submitAttempt(
  payload: AttemptPayload
): Promise<AttemptResponse> {
  return request<AttemptResponse>("/attempts/", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getUserAttempts(
  userId: number
): Promise<Attempt[]> {
  return request<Attempt[]>(`/attempts/user/${userId}`);
}

export async function getAttempt(
  attemptId: number
): Promise<Attempt> {
  return request<Attempt>(`/attempts/${attemptId}`);
}


/* =========================================================
   Learner State
   ========================================================= */

export async function getLearnerStates(
  userId: number
): Promise<LearnerState[]> {
  return request<LearnerState[]>(
    `/learner-states/user/${userId}`
  );
}

export async function getLearnerState(
  userId: number,
  conceptId: number
): Promise<LearnerState> {
  return request<LearnerState>(
    `/learner-states/user/${userId}/concept/${conceptId}`
  );
}


/* =========================================================
   Recommendations
   ========================================================= */

export async function getNextRecommendation(
  userId: number
): Promise<Recommendation> {
  return request<Recommendation>(
    `/recommendations/next/${userId}`
  );
}export type Concept = {
  id: number
  topic_id: number
  name: string
  description?: string | null
  difficulty: number
}

export async function getConcept(
  conceptId: number
): Promise<Concept> {
  const response = await fetch(
    `${API_BASE_URL}/concepts/${conceptId}`
  )

  if (!response.ok) {
    throw new Error(
      `Failed to load concept (${response.status})`
    )
  }

  return response.json()
}