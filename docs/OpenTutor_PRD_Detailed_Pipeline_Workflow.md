# OpenTutor --- Product Requirements & System Workflow Document

**Document Type:** Product Requirements Document (PRD) + Technical
System Workflow Specification\
**Project:** OpenTutor\
**Version:** 1.0\
**Date:** 2026-09-05\
**Status:** Engineering Foundation / Pre-API Phase\
**Primary Purpose:** Define the complete product, backend, database,
AI/RAG, recommendation, API, frontend, testing, deployment, and
operational workflow for OpenTutor.

------------------------------------------------------------------------

# 1. Executive Summary

OpenTutor is an AI-assisted personalized learning platform designed to
move beyond static question-answer tutoring toward a structured,
adaptive learning workflow.

The system maintains a representation of:

-   students and their learning state,
-   courses and learning concepts,
-   prerequisite relationships between concepts,
-   learning resources,
-   assessments and attempts,
-   student mastery/progress,
-   weak areas,
-   recommendations,
-   tutor interactions,
-   AI-generated explanations and learning actions.

The central idea is that the tutor should not treat every student
question as an isolated prompt. Instead, the system should understand
the student's current learning context, determine the relevant concept,
evaluate prerequisites and mastery, retrieve appropriate knowledge,
generate an explanation, and update the learner state after interaction.

The intended high-level loop is:

``` text
Student
   ↓
Frontend
   ↓
FastAPI API Layer
   ↓
Authentication / Validation / Request Context
   ↓
Application / Tutor Orchestration Layer
   ↓
Student State + Concept Graph + Recommendation Logic
   ↓
RAG / Retrieval Layer
   ↓
LLM / Tutor Intelligence
   ↓
Response + Learning Action
   ↓
Database / Learning State Update
   ↓
Personalized Next Recommendation
```

The system is therefore both:

1.  a conventional software platform with APIs, database,
    authentication, persistence, and frontend components; and
2.  an adaptive AI system whose outputs are influenced by structured
    learner state.

------------------------------------------------------------------------

# 2. Product Vision

## 2.1 Vision

Build a tutor that behaves like a structured learning companion rather
than a generic chatbot.

OpenTutor should be capable of answering:

-   What is the student trying to learn?
-   What does the student already know?
-   What prerequisite knowledge is missing?
-   Where is the student struggling?
-   What explanation is most appropriate?
-   Which resource or concept should be recommended next?
-   Did the latest interaction improve understanding?
-   What should the student do next?

## 2.2 Product Philosophy

The product should follow these principles:

### Context over isolated prompts

The tutor should use available learner context rather than treating
every message as independent.

### Mastery over completion

Finishing content should not automatically mean the student has mastered
it.

### Prerequisites matter

A student struggling with an advanced concept may actually be missing
foundational knowledge.

### Retrieval before generation

When the system has authoritative course material or indexed resources,
the LLM should ground its response in retrieved information.

### Explainability

Recommendation and learning decisions should have understandable
reasons.

### Safe AI behavior

The system must avoid presenting unsupported information as
authoritative course material.

### Incremental intelligence

The system should remain useful even when some advanced AI capabilities
are unavailable.

------------------------------------------------------------------------

# 3. Product Objectives

## 3.1 Primary Objectives

1.  Create a structured learning-data foundation.
2.  Provide personalized tutoring through APIs.
3.  Maintain student learning state.
4.  Represent concepts and prerequisites.
5.  Support retrieval-augmented tutoring.
6.  Generate personalized recommendations.
7.  Track learning interactions and assessment performance.
8.  Provide a coherent end-to-end learning workflow.
9.  Make the system testable and reproducible.
10. Provide an architecture that can scale from prototype to production.

## 3.2 Secondary Objectives

-   Support multiple courses.
-   Support multiple learning resources.
-   Enable future analytics.
-   Enable future adaptive assessments.
-   Enable future teacher/admin functionality.
-   Enable future model replacement without rewriting the whole
    application.
-   Keep AI logic separated from infrastructure logic.

## 3.3 Non-Goals for the Initial Version

The initial implementation does not need to provide:

-   a full enterprise LMS,
-   live human tutoring,
-   complex school administration,
-   billing/subscriptions,
-   advanced proctoring,
-   autonomous grading of every possible question type,
-   unrestricted autonomous AI actions.

These can be future extensions.

------------------------------------------------------------------------

# 4. Target Users

## 4.1 Student

Primary user.

Needs:

-   learn concepts,
-   ask questions,
-   receive explanations,
-   practice,
-   identify weak areas,
-   receive recommendations,
-   track progress.

## 4.2 Instructor / Content Author

Potential future user.

Needs:

-   manage courses,
-   manage concepts,
-   define prerequisites,
-   upload resources,
-   inspect learner progress,
-   validate AI-generated content.

## 4.3 Administrator

Potential future user.

Needs:

-   manage users,
-   monitor system health,
-   manage content,
-   manage permissions,
-   inspect operational failures.

------------------------------------------------------------------------

# 5. Core Product Concepts

## 5.1 Course

A logical learning program containing concepts, resources, and
assessments.

Example:

``` text
Course: Machine Learning
```

## 5.2 Concept

A specific unit of knowledge.

Example:

``` text
Linear Regression
```

## 5.3 Prerequisite

A concept that should be understood before another concept.

Example:

``` text
Linear Algebra → Linear Regression
```

## 5.4 Resource

Learning material associated with a concept or course.

Examples:

-   textbook chapter,
-   PDF,
-   lecture notes,
-   article,
-   video transcript,
-   generated study material.

## 5.5 Mastery

A representation of how well the student understands a concept.

A mastery value may be represented numerically, for example:

``` text
0.00 → no evidence of mastery
1.00 → strong evidence of mastery
```

The exact scoring algorithm is application-specific and should remain
replaceable.

## 5.6 Recommendation Score

A numerical ranking signal used to prioritize concepts/resources for a
learner.

It is not automatically a probability.

A conceptual score could combine:

``` text
Recommendation Score =
    Weakness Weight
  + Prerequisite Importance
  + Course Progress Relevance
  + Difficulty Fit
  + Recency / Spacing Factor
  + Assessment Evidence
  + Resource Relevance
```

The production implementation should normalize the final score.

------------------------------------------------------------------------

# 6. End-to-End Product Workflow

The complete learning pipeline is divided into several stages.

``` text
                    ┌──────────────────────┐
                    │      Student UI      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI API      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Request Validation   │
                    │ Auth + Context       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Tutor Orchestrator   │
                    └──────┬─────┬─────────┘
                           │     │
              ┌────────────┘     └──────────────┐
              ▼                                 ▼
    ┌───────────────────┐             ┌───────────────────┐
    │ Student State     │             │ Concept Graph     │
    │ Progress/Mastery  │             │ Prerequisites     │
    └─────────┬─────────┘             └─────────┬─────────┘
              │                                 │
              └──────────────┬──────────────────┘
                             ▼
                  ┌────────────────────────┐
                  │ Intent / Concept       │
                  │ Identification         │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Retrieval / RAG        │
                  │ Context Construction   │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ LLM / Tutor Engine     │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Response Validation    │
                  │ + Learning Action      │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Persist Interaction     │
                  │ + Update Learner State │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │ Recommendation Engine  │
                  └───────────┬────────────┘
                              │
                              ▼
                       Next Learning Step
```

------------------------------------------------------------------------

# 7. Pipeline Architecture

## 7.1 Layer 1 --- Presentation Layer

The frontend is responsible for:

-   login/signup UI,
-   course selection,
-   dashboard,
-   progress visualization,
-   tutor chat,
-   recommendations,
-   resource browsing,
-   assessments,
-   feedback.

The frontend must not contain core business rules.

Example:

``` text
Frontend
   ↓
HTTP Request
   ↓
Backend API
```

The frontend should receive structured responses from the backend.

------------------------------------------------------------------------

# 8. API Layer

FastAPI will provide the backend API boundary.

Responsibilities:

-   route requests,
-   validate request payloads,
-   authenticate users,
-   authorize actions,
-   create request context,
-   call application services,
-   serialize responses,
-   return appropriate HTTP errors.

The API layer should remain thin.

Bad architecture:

``` text
Route → 500 lines of business logic
```

Preferred architecture:

``` text
Route
  ↓
Schema Validation
  ↓
Service
  ↓
Domain Logic
  ↓
Repository / Database
```

------------------------------------------------------------------------

# 9. Request Lifecycle

For every API request:

``` text
1. Client creates HTTP request
2. FastAPI receives request
3. Authentication middleware/dependency executes
4. Authorization is evaluated
5. Request schema validates input
6. Request context is created
7. API route invokes service
8. Service performs business logic
9. Database/retrieval/AI operations execute
10. Result is validated
11. Database changes are committed where required
12. Response schema serializes output
13. API returns response
```

Failures at any stage should be converted into controlled errors.

------------------------------------------------------------------------

# 10. Tutor Request Workflow

When a student asks a question:

``` text
POST /tutor/chat
```

Conceptually:

``` text
Student Message
      ↓
Authenticate Student
      ↓
Load Student Context
      ↓
Identify Intent
      ↓
Identify / Infer Concept
      ↓
Load Concept Information
      ↓
Load Prerequisites
      ↓
Load Student Mastery
      ↓
Determine Missing Knowledge
      ↓
Retrieve Relevant Resources
      ↓
Build Prompt Context
      ↓
Generate Tutor Response
      ↓
Validate Response
      ↓
Persist Interaction
      ↓
Update Learning Evidence
      ↓
Recalculate Recommendations
      ↓
Return Response
```

------------------------------------------------------------------------

# 11. Intent Identification

The tutor should distinguish between different request types.

Possible intents:

-   concept explanation,
-   clarification,
-   worked example,
-   practice question,
-   answer verification,
-   hint request,
-   summary,
-   revision,
-   prerequisite help,
-   resource recommendation,
-   progress question,
-   course navigation.

Example:

``` text
"Explain gradient descent"
```

Intent:

``` text
concept_explanation
```

Example:

``` text
"Give me a hint but don't solve it"
```

Intent:

``` text
hint_request
```

The intent classifier may initially be rule-based or LLM-assisted and
can later be replaced by a dedicated model.

------------------------------------------------------------------------

# 12. Concept Identification

The tutor should map the student's request to a known learning concept
when possible.

Example:

``` text
Student:
"I don't understand why we use a learning rate."

Detected concept:
Gradient Descent

Related concepts:
Optimization
Learning Rate
Loss Function
```

Concept identification can use:

1.  explicit frontend concept ID,
2.  current lesson context,
3.  recent conversation context,
4.  semantic similarity,
5.  LLM classification,
6.  course concept graph.

The system should prefer structured identifiers when available.

------------------------------------------------------------------------

# 13. Student Context Pipeline

The tutor needs a learner context object.

Conceptual structure:

``` text
StudentContext
├── student_id
├── active_course
├── active_concept
├── recent_concepts
├── mastered_concepts
├── weak_concepts
├── prerequisite_gaps
├── recent_attempts
├── recent_interactions
├── recommended_concepts
└── relevant_resources
```

The context should be bounded.

The system must not send the entire database or entire conversation
history to the LLM unnecessarily.

------------------------------------------------------------------------

# 14. Learning State Pipeline

Student state is continuously updated.

``` text
Initial State
      ↓
Student studies
      ↓
Student asks question
      ↓
Student attempts assessment
      ↓
Evidence collected
      ↓
Mastery updated
      ↓
Weak areas recalculated
      ↓
Prerequisite gaps recalculated
      ↓
Recommendations recalculated
```

Learning state should be treated as evidence-driven rather than
permanently fixed.

------------------------------------------------------------------------

# 15. Assessment Workflow

An assessment interaction may follow:

``` text
Select concept
    ↓
Generate/select question
    ↓
Present question
    ↓
Student submits answer
    ↓
Evaluate answer
    ↓
Record attempt
    ↓
Determine correctness
    ↓
Calculate performance evidence
    ↓
Update mastery
    ↓
Update weak-area signals
    ↓
Update recommendation score
```

Attempt records should preserve enough information for later analysis.

Potential fields:

-   student,
-   assessment/question,
-   concept,
-   submitted answer,
-   correctness,
-   score,
-   time taken,
-   attempt number,
-   timestamp,
-   evaluation method.

------------------------------------------------------------------------

# 16. Mastery Update Pipeline

Mastery should not be updated solely from one answer.

Evidence may include:

-   assessment correctness,
-   repeated performance,
-   difficulty,
-   recency,
-   hints used,
-   retries,
-   prerequisite performance,
-   interaction signals.

A conceptual update:

``` text
New Mastery =
    f(
        Previous Mastery,
        New Assessment Evidence,
        Difficulty,
        Recency,
        Historical Performance
    )
```

The exact function should be isolated inside a mastery service so that
the algorithm can evolve without changing API/database code.

------------------------------------------------------------------------

# 17. Prerequisite Graph

The concept graph is one of the most important structured components.

Example:

``` text
Arithmetic
   ↓
Algebra
   ↓
Functions
   ↓
Calculus
   ↓
Derivatives
   ↓
Optimization
```

The database must support directed prerequisite relationships.

Example:

``` text
concept_prerequisites
---------------------
concept_id
prerequisite_id
```

This allows the application to answer:

``` text
"What concepts should the student know before learning X?"
```

and:

``` text
"Which prerequisite is likely causing the current difficulty?"
```

------------------------------------------------------------------------

# 18. Prerequisite Gap Detection

If:

``` text
Target Concept = Optimization
```

and:

``` text
Optimization prerequisites:
- Derivatives
- Functions
- Algebra
```

but student mastery is:

``` text
Derivatives = 0.82
Functions   = 0.76
Algebra     = 0.41
```

then Algebra may be flagged as a prerequisite weakness.

Pipeline:

``` text
Target Concept
      ↓
Fetch prerequisite graph
      ↓
Fetch student mastery
      ↓
Compare required vs actual mastery
      ↓
Rank prerequisite gaps
      ↓
Use gaps in tutor explanation/recommendation
```

------------------------------------------------------------------------

# 19. RAG Pipeline

Retrieval-Augmented Generation should be treated as a separate pipeline.

## 19.1 Ingestion

``` text
Document
   ↓
Parse
   ↓
Clean
   ↓
Split into chunks
   ↓
Attach metadata
   ↓
Generate embeddings
   ↓
Store vectors
```

## 19.2 Retrieval

``` text
Student Question
      ↓
Query normalization
      ↓
Embedding
      ↓
Vector search
      ↓
Metadata filtering
      ↓
Top-K chunks
      ↓
Optional reranking
```

## 19.3 Generation

``` text
Student Context
      +
Retrieved Context
      +
Tutor Instructions
      +
Conversation Context
      ↓
LLM
      ↓
Tutor Response
```

------------------------------------------------------------------------

# 20. RAG Metadata

Each indexed chunk should ideally contain metadata such as:

``` text
document_id
course_id
concept_id
resource_type
source_title
chunk_id
page_number
section
difficulty
version
```

Metadata allows retrieval to be constrained.

For example:

``` text
course_id = Machine Learning
concept_id = Gradient Descent
```

This reduces irrelevant retrieval.

------------------------------------------------------------------------

# 21. Chunking Strategy

Documents should be divided into meaningful chunks.

A chunk should:

-   preserve semantic context,
-   avoid being excessively large,
-   contain enough information to answer a question,
-   preserve source metadata.

Chunk boundaries should ideally follow:

-   headings,
-   sections,
-   paragraphs,
-   semantic units.

Arbitrary fixed-size chunking can be used as a baseline but should not
be the only strategy.

------------------------------------------------------------------------

# 22. Retrieval Strategy

Initial retrieval:

``` text
Top-K semantic search
```

Advanced retrieval:

``` text
Semantic Search
      +
Keyword Search
      +
Metadata Filtering
      +
Reranking
      ↓
Final Context
```

The final context should be small enough for efficient generation.

------------------------------------------------------------------------

# 23. Prompt Construction Pipeline

The tutor prompt should be assembled from structured components.

``` text
System Instructions
        +
Student Profile/State
        +
Current Concept
        +
Prerequisite Information
        +
Recent Conversation
        +
Retrieved Course Context
        +
Current Question
        ↓
Final Prompt
```

The prompt should explicitly distinguish:

-   authoritative retrieved information,
-   learner context,
-   system instructions,
-   user-generated content.

------------------------------------------------------------------------

# 24. Tutor Response Policy

The tutor should:

1.  Answer the student's question.
2.  Match explanation difficulty to the student.
3.  Use retrieved source context when available.
4.  Avoid unnecessary complexity.
5.  Mention prerequisite concepts when relevant.
6.  Provide examples when helpful.
7.  Avoid revealing an answer when the user explicitly asks for a hint.
8.  Encourage understanding rather than blind copying.
9.  Provide uncertainty indicators when evidence is insufficient.
10. Avoid fabricating source citations or claims.

------------------------------------------------------------------------

# 25. Response Types

The tutor can produce structured response categories.

``` text
EXPLANATION
HINT
EXAMPLE
SUMMARY
PRACTICE
CORRECTION
PREREQUISITE_GUIDANCE
RESOURCE_RECOMMENDATION
```

The API may return:

``` json
{
  "response": "...",
  "intent": "concept_explanation",
  "concept_id": "...",
  "related_concepts": [],
  "recommended_next_step": {},
  "sources": []
}
```

------------------------------------------------------------------------

# 26. Recommendation Engine

The recommendation engine converts learning evidence into ranked next
actions.

Conceptual pipeline:

``` text
Student State
      ↓
Candidate Concepts
      ↓
Remove completed/inapplicable items
      ↓
Evaluate prerequisites
      ↓
Evaluate mastery
      ↓
Evaluate difficulty
      ↓
Evaluate course relevance
      ↓
Evaluate recent activity
      ↓
Calculate score
      ↓
Rank
      ↓
Return top recommendations
```

------------------------------------------------------------------------

# 27. Recommendation Candidate Generation

Candidate concepts may come from:

1.  current course sequence,
2.  prerequisites of current concept,
3.  weak concepts,
4.  unfinished concepts,
5.  review candidates,
6.  recommended resources,
7.  assessment failures.

Example:

``` text
Candidate Set =
{
  current concept,
  weak prerequisites,
  next curriculum concept,
  overdue review concepts
}
```

------------------------------------------------------------------------

# 28. Recommendation Scoring

A conceptual model:

``` text
score =
    w1 * weakness
  + w2 * prerequisite_importance
  + w3 * curriculum_relevance
  + w4 * difficulty_fit
  + w5 * review_priority
  + w6 * recent_failure_signal
```

All terms should be normalized.

Example:

``` text
weakness = 1 - mastery
```

The weights should be configuration-driven rather than hard-coded
throughout the codebase.

------------------------------------------------------------------------

# 29. Recommendation Explainability

Every recommendation should ideally have a reason.

Example:

``` text
Recommendation:
Derivatives

Reason:
Your recent attempts show difficulty with derivative-based questions,
and derivatives are a prerequisite for the optimization topic you are studying.
```

This improves trust and makes the system easier to debug.

------------------------------------------------------------------------

# 30. Database Architecture

PostgreSQL is the persistent relational database.

The database should store structured application state.

Conceptual entities include:

``` text
Users
Courses
Concepts
Concept Prerequisites
Course Concepts
Resources
Assessments
Questions
Attempts
Student Progress
Recommendations
Tutor Sessions
Tutor Messages
```

The exact implemented schema is authoritative and should remain
synchronized with SQLAlchemy models and Alembic migrations.

------------------------------------------------------------------------

# 31. SQLAlchemy Role

SQLAlchemy is the ORM layer.

Conceptually:

``` text
Python Object
     ↕
SQLAlchemy ORM
     ↕
Psycopg
     ↕
PostgreSQL
```

A model represents a database entity.

Responsibilities:

-   define table mappings,
-   define relationships,
-   represent columns,
-   define constraints,
-   construct queries,
-   manage persistence.

Business logic should not be embedded directly inside database models
unless appropriate for simple domain behavior.

------------------------------------------------------------------------

# 32. Psycopg Role

Psycopg is the PostgreSQL database driver.

Its role is the low-level Python ↔ PostgreSQL communication layer.

Architecture:

``` text
Application
    ↓
SQLAlchemy
    ↓
Psycopg
    ↓
PostgreSQL
```

SQLAlchemy does not replace the database driver.

------------------------------------------------------------------------

# 33. Alembic Migration Workflow

Alembic manages schema changes.

Workflow:

``` text
Developer changes SQLAlchemy model
        ↓
Generate migration
        ↓
Review migration
        ↓
Commit migration to Git
        ↓
Apply migration
        ↓
Database schema changes
```

Useful operations:

``` text
python -m alembic current
python -m alembic history
python -m alembic upgrade head
python -m alembic downgrade -1
python -m alembic revision --autogenerate -m "description"
```

Alembic tracks schema structure, not normal application records.

------------------------------------------------------------------------

# 34. Migration Integrity

A migration must be:

-   deterministic,
-   reviewable,
-   reproducible,
-   compatible with the application,
-   safe to apply.

The project should avoid manually modifying production schema without
corresponding migration history.

Schema state should be reproducible from:

``` text
Base Database
      +
Alembic Migration Chain
      =
Current Schema
```

------------------------------------------------------------------------

# 35. Database Constraints

Database constraints are part of the data-integrity layer.

Potential constraints include:

### Primary keys

Guarantee unique entity identity.

### Foreign keys

Guarantee valid relationships.

### Unique constraints

Prevent duplicate logical relationships.

Example:

``` text
(concept_id, prerequisite_id)
```

should not appear twice.

### Check constraints

Enforce valid ranges or states.

Example:

``` text
mastery >= 0 AND mastery <= 1
```

### Not-null constraints

Protect required fields.

Application validation should complement database constraints rather
than replace them.

------------------------------------------------------------------------

# 36. Transaction Workflow

Database writes should use transaction boundaries.

Example:

``` text
Start transaction
    ↓
Create attempt
    ↓
Update progress
    ↓
Update mastery
    ↓
Create recommendation event
    ↓
Commit
```

If a critical operation fails:

``` text
Rollback
```

This prevents partially updated learner state.

------------------------------------------------------------------------

# 37. Concurrency Considerations

Two simultaneous requests may update the same student's state.

Examples:

-   assessment submission,
-   tutor interaction,
-   progress update.

The system should eventually consider:

-   transaction isolation,
-   optimistic concurrency,
-   row-level locking where necessary,
-   idempotency for repeated submissions.

The initial implementation can use normal PostgreSQL transactions but
should keep state-update logic centralized.

------------------------------------------------------------------------

# 38. Authentication and Authorization

Authentication establishes:

``` text
Who is the user?
```

Authorization establishes:

``` text
What is the user allowed to access?
```

Student A must not retrieve Student B's private learning data.

Authorization should be enforced server-side.

Do not rely on frontend route restrictions for security.

------------------------------------------------------------------------

# 39. API Security Requirements

The backend should consider:

-   authentication,
-   authorization,
-   input validation,
-   rate limiting,
-   request size limits,
-   secret management,
-   SQL injection prevention,
-   prompt injection defenses,
-   logging without sensitive data,
-   safe error responses.

------------------------------------------------------------------------

# 40. Prompt Injection Considerations

RAG introduces a new attack surface.

Retrieved documents may contain malicious or irrelevant instructions.

The system must distinguish:

``` text
Content to learn from
```

from:

``` text
Instructions the model must follow
```

Retrieved content must not automatically override system-level tutor
rules.

------------------------------------------------------------------------

# 41. Data Flow

## 41.1 Student Chat

``` text
Frontend
  ↓
POST /tutor/chat
  ↓
FastAPI
  ↓
Auth
  ↓
Tutor Service
  ↓
Student Context Service
  ↓
Concept Service
  ↓
Prerequisite Service
  ↓
Retrieval Service
  ↓
LLM Service
  ↓
Interaction Repository
  ↓
Learning State Service
  ↓
Recommendation Service
  ↓
API Response
```

## 41.2 Assessment Submission

``` text
Frontend
  ↓
POST /assessments/{id}/attempt
  ↓
Validate
  ↓
Evaluate
  ↓
Persist Attempt
  ↓
Update Progress
  ↓
Update Mastery
  ↓
Update Weakness
  ↓
Recalculate Recommendations
  ↓
Return Result
```

## 41.3 Resource Ingestion

``` text
Upload
  ↓
File Validation
  ↓
Document Parsing
  ↓
Text Extraction
  ↓
Cleaning
  ↓
Chunking
  ↓
Metadata Assignment
  ↓
Embedding Generation
  ↓
Vector Storage
  ↓
Index Ready
```

------------------------------------------------------------------------

# 42. Backend Service Boundaries

Recommended logical services/modules:

``` text
auth
users
courses
concepts
prerequisites
resources
assessments
progress
tutor
retrieval
recommendations
analytics
```

The exact folder names may differ, but responsibilities should remain
separated.

------------------------------------------------------------------------

# 43. Repository Layer

Repositories abstract persistence operations.

Example:

``` text
StudentRepository
ConceptRepository
ProgressRepository
AttemptRepository
ResourceRepository
```

Repository responsibilities:

-   query database,
-   insert records,
-   update records,
-   delete records where permitted.

Repositories should not decide high-level learning strategy.

------------------------------------------------------------------------

# 44. Service Layer

Services implement business workflows.

Examples:

``` text
TutorService
MasteryService
RecommendationService
AssessmentService
PrerequisiteService
```

A service may call multiple repositories.

Example:

``` text
AssessmentService
    ↓
AttemptRepository
ProgressRepository
ConceptRepository
RecommendationRepository
```

------------------------------------------------------------------------

# 45. Domain Logic Separation

A critical architectural rule:

``` text
API logic ≠ business logic ≠ database logic ≠ AI provider logic
```

Preferred:

``` text
API
 ↓
Service
 ↓
Domain logic
 ↓
Repository
 ↓
Database
```

AI:

``` text
Service
 ↓
LLM interface
 ↓
Provider implementation
```

This allows model/provider replacement.

------------------------------------------------------------------------

# 46. LLM Abstraction

The application should not tightly couple business logic to a single
model provider.

Preferred:

``` text
TutorService
     ↓
LLM Interface
     ↓
Provider Adapter
     ↓
Specific Model
```

This allows future replacement with:

-   local models,
-   hosted APIs,
-   different model providers,
-   specialized models.

------------------------------------------------------------------------

# 47. AI Failure Handling

LLM calls can fail due to:

-   timeout,
-   rate limit,
-   provider outage,
-   invalid response,
-   malformed structured output,
-   context limit,
-   network failure.

The application should define fallback behavior.

Possible fallback:

``` text
LLM unavailable
    ↓
Return retrieval-based explanation/resource
OR
Return controlled retryable error
```

The system should never silently store an invalid AI response as trusted
learning evidence.

------------------------------------------------------------------------

# 48. Observability

The system should eventually expose:

### Logs

-   request lifecycle,
-   exceptions,
-   AI failures,
-   database failures.

### Metrics

-   API latency,
-   retrieval latency,
-   LLM latency,
-   error rates,
-   recommendation generation time,
-   database query latency.

### Traces

For complex requests:

``` text
API
 ↓
Tutor Service
 ↓
DB
 ↓
Retrieval
 ↓
LLM
 ↓
DB
```

Tracing becomes especially useful for debugging slow tutor responses.

------------------------------------------------------------------------

# 49. Logging Rules

Do not log:

-   passwords,
-   API keys,
-   tokens,
-   unnecessary private learner content.

Logs should contain correlation/request IDs where possible.

Example:

``` text
request_id=abc123
student_id=<internal identifier>
operation=tutor_chat
latency_ms=842
retrieval_count=5
llm_status=success
```

------------------------------------------------------------------------

# 50. Configuration Management

Configuration should be separated from source code.

Typical environment variables:

``` text
DATABASE_URL
SECRET_KEY
LLM_API_KEY
VECTOR_DATABASE_URL
ENVIRONMENT
LOG_LEVEL
```

`.env` should not be committed when it contains secrets.

A `.env.example` may contain variable names without secrets.

------------------------------------------------------------------------

# 51. Docker Role

Docker is an environment/containerization mechanism.

It is not required for defining SQL tables.

Its primary value is reproducibility.

Example:

``` text
Developer Machine
       ↓
Docker
       ↓
PostgreSQL Service
```

This reduces "works on my machine" problems.

Docker may eventually run:

-   PostgreSQL,
-   vector database,
-   backend,
-   frontend,
-   supporting services.

------------------------------------------------------------------------

# 52. Development Environment

Python dependencies should be isolated with a virtual environment.

``` text
Project
  ├── .venv
  ├── backend
  └── ...
```

`.venv` prevents project dependencies from interfering with system
Python or unrelated projects.

------------------------------------------------------------------------

# 53. Git Workflow

Git tracks source changes.

Typical workflow:

``` text
Change code
   ↓
Run tests
   ↓
Review git diff
   ↓
git status
   ↓
git add
   ↓
git commit
   ↓
git push
```

Migration files, application source, tests, and configuration templates
should be version-controlled.

Secrets must not be pushed.

------------------------------------------------------------------------

# 54. CI/CD Workflow

Future CI pipeline:

``` text
Git Push / Pull Request
        ↓
Install dependencies
        ↓
Lint / Format Check
        ↓
Unit Tests
        ↓
Database Tests
        ↓
Migration Validation
        ↓
Integration Tests
        ↓
Build
        ↓
Deploy
```

A pull request should fail if critical tests fail.

------------------------------------------------------------------------

# 55. Testing Strategy

Testing is divided into levels.

## 55.1 Unit Tests

Test isolated functions.

Examples:

-   recommendation score,
-   mastery update,
-   prerequisite ranking,
-   input validation.

## 55.2 Database Tests

Test:

-   connection,
-   models,
-   relationships,
-   constraints,
-   CRUD operations,
-   migration compatibility.

## 55.3 Integration Tests

Test multiple components together.

Example:

``` text
API
 ↓
Service
 ↓
SQLAlchemy
 ↓
PostgreSQL
```

## 55.4 AI Pipeline Tests

Test:

-   prompt construction,
-   retrieval,
-   context selection,
-   structured output parsing,
-   fallback behavior.

## 55.5 End-to-End Tests

Simulate:

``` text
Login
 ↓
Choose course
 ↓
Learn concept
 ↓
Ask question
 ↓
Take assessment
 ↓
Update mastery
 ↓
Receive recommendation
```

------------------------------------------------------------------------

# 56. Pytest Role

Pytest is the project's automated testing framework.

Current database-foundation validation should cover:

``` text
Python
  ↓
SQLAlchemy
  ↓
Psycopg
  ↓
PostgreSQL
```

The testing system should verify that database assumptions are correct
before API complexity is added.

------------------------------------------------------------------------

# 57. Test Data Strategy

Tests should use controlled data.

Example:

``` text
Test Course
 ├── Concept A
 ├── Concept B
 └── Concept C

A prerequisite of B
B prerequisite of C
```

Student:

``` text
A mastery = 0.90
B mastery = 0.45
C mastery = 0.10
```

Expected recommendation behavior can then be validated.

------------------------------------------------------------------------

# 58. Test Isolation

Each test should avoid depending on another test's database state.

Possible approaches:

-   transaction rollback,
-   temporary database,
-   test schema,
-   fixture-based setup/cleanup.

The selected strategy must prevent test-order dependency.

------------------------------------------------------------------------

# 59. Error Handling

Errors should be categorized.

Examples:

``` text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
429 Rate Limited
500 Internal Error
503 AI/Dependency Unavailable
```

The backend should return structured error responses.

------------------------------------------------------------------------

# 60. API Design Principles

APIs should:

-   use predictable resource names,
-   use correct HTTP semantics,
-   validate input,
-   return consistent schemas,
-   use pagination where needed,
-   avoid exposing database internals,
-   support versioning if required.

Example:

``` text
GET    /courses
GET    /courses/{course_id}
GET    /concepts/{concept_id}
GET    /students/me/progress
POST   /tutor/chat
POST   /assessments/{assessment_id}/attempt
GET    /recommendations
```

The final endpoint set should be determined during API implementation.

------------------------------------------------------------------------

# 61. Example Tutor API Contract

Request:

``` json
{
  "message": "I don't understand gradient descent.",
  "course_id": "course-123",
  "concept_id": "concept-456",
  "session_id": "session-789"
}
```

Backend processing:

``` text
Validate
→ Authenticate
→ Load student
→ Load course
→ Load concept
→ Load prerequisites
→ Load mastery
→ Retrieve resources
→ Generate response
→ Save interaction
→ Update learning evidence
→ Return response
```

Response:

``` json
{
  "message": "Gradient descent is...",
  "concept_id": "concept-456",
  "intent": "concept_explanation",
  "sources": [],
  "next_action": {
    "type": "practice",
    "concept_id": "concept-456"
  }
}
```

------------------------------------------------------------------------

# 62. Session Workflow

A tutor session may contain:

``` text
Session
 ├── Message 1
 ├── Message 2
 ├── Message 3
 ├── Assessment
 └── Recommendation
```

The session provides short-term conversational continuity.

Long-term learning state belongs in structured student-progress records.

Do not use conversation history as the only source of truth for mastery.

------------------------------------------------------------------------

# 63. Conversation Context Management

A long conversation cannot be sent indefinitely to the LLM.

The system should use:

``` text
Recent messages
+
Conversation summary
+
Relevant structured learner state
+
Retrieved knowledge
```

This reduces token usage and keeps context relevant.

------------------------------------------------------------------------

# 64. Learning Event Model

Important actions can be represented as events.

Examples:

``` text
COURSE_STARTED
CONCEPT_VIEWED
RESOURCE_OPENED
QUESTION_ASKED
HINT_REQUESTED
ASSESSMENT_STARTED
ANSWER_SUBMITTED
ASSESSMENT_COMPLETED
CONCEPT_MASTERED
RECOMMENDATION_ACCEPTED
```

Events can support analytics and future adaptive algorithms.

------------------------------------------------------------------------

# 65. Recommendation Feedback Loop

Recommendations should be evaluated after the learner acts on them.

``` text
Recommendation
      ↓
Student accepts/ignores
      ↓
Student studies
      ↓
Assessment evidence
      ↓
Mastery changes
      ↓
Recommendation quality evaluated
```

This creates a feedback loop for improving the recommendation engine.

------------------------------------------------------------------------

# 66. Adaptive Learning Loop

The complete adaptive loop is:

``` text
Observe
  ↓
Understand
  ↓
Assess
  ↓
Diagnose
  ↓
Teach
  ↓
Practice
  ↓
Measure
  ↓
Update State
  ↓
Recommend
  ↓
Repeat
```

This loop is the core product behavior.

------------------------------------------------------------------------

# 67. Example Full Scenario

Student begins a Machine Learning course.

## Step 1 --- Course selection

``` text
Student → Machine Learning
```

## Step 2 --- Current concept

``` text
Gradient Descent
```

## Step 3 --- Student asks

``` text
"Why does gradient descent need a learning rate?"
```

## Step 4 --- Backend identifies

``` text
Intent = explanation
Concept = learning rate / gradient descent
```

## Step 5 --- Context retrieval

System loads:

``` text
Student mastery
Prerequisites
Recent attempts
Relevant resources
```

## Step 6 --- Prerequisite diagnosis

Suppose:

``` text
Optimization = 0.70
Derivatives = 0.35
```

The system recognizes a possible derivative prerequisite gap.

## Step 7 --- RAG

Retrieve authoritative material about:

``` text
Gradient descent
Learning rate
Derivatives
```

## Step 8 --- LLM

Generate an explanation adjusted to the learner.

## Step 9 --- Persistence

Store:

``` text
Question
Response
Concept
Session
Timestamp
```

## Step 10 --- Evidence update

Interaction contributes learning evidence but does not automatically
mark mastery.

## Step 11 --- Recommendation

Potential recommendation:

``` text
Review derivatives
```

because it is a prerequisite and a weak area.

## Step 12 --- Student continues

The loop repeats.

------------------------------------------------------------------------

# 68. Data Ownership

Each subsystem should have a clear source of truth.

``` text
PostgreSQL
    ↓
Persistent structured learning state

Vector Store
    ↓
Searchable knowledge representations

Conversation Store
    ↓
Tutor interaction history

LLM
    ↓
Generated reasoning/output, not authoritative persistent truth
```

The LLM should not become the source of truth for student progress.

------------------------------------------------------------------------

# 69. Data Consistency Rules

Critical derived state should be reproducible.

For example:

``` text
Attempts
   ↓
Mastery calculation
   ↓
Recommendations
```

If recommendation logic changes, recommendations should be recomputable
from stored evidence.

Avoid storing only opaque final scores without the evidence required to
regenerate them.

------------------------------------------------------------------------

# 70. Performance Requirements

Initial targets should be practical rather than prematurely optimized.

Potential targets:

-   normal CRUD API: low hundreds of milliseconds where practical,
-   database queries: optimized and indexed,
-   retrieval: sub-second target where infrastructure permits,
-   AI response: dependent on model/provider,
-   recommendation generation: preferably fast enough for dashboard use.

AI latency should not be confused with application/database latency.

------------------------------------------------------------------------

# 71. Scalability

The architecture should support future horizontal scaling.

Stateless API instances:

``` text
Client
  ↓
Load Balancer
  ↓
API Instance 1
API Instance 2
API Instance 3
```

Shared state remains in external systems:

``` text
PostgreSQL
Vector Store
Cache
Object Storage
```

------------------------------------------------------------------------

# 72. Caching Opportunities

Potential cache targets:

-   course metadata,
-   concept metadata,
-   prerequisite graphs,
-   frequently retrieved resources,
-   recommendation results,
-   prompt-independent configuration.

Do not cache highly dynamic learner state without an explicit
invalidation strategy.

------------------------------------------------------------------------

# 73. Background Jobs

Some tasks should eventually become asynchronous.

Examples:

-   document ingestion,
-   embedding generation,
-   large-scale recommendation recalculation,
-   analytics aggregation,
-   notification generation.

Workflow:

``` text
API
 ↓
Queue
 ↓
Worker
 ↓
Database / Vector Store
```

The initial prototype can execute some operations synchronously if scale
does not require queues.

------------------------------------------------------------------------

# 74. File / Resource Processing Pipeline

For uploaded resources:

``` text
Upload
 ↓
Validate file
 ↓
Store original
 ↓
Extract text
 ↓
Normalize text
 ↓
Chunk
 ↓
Metadata
 ↓
Embedding
 ↓
Vector index
 ↓
Mark resource READY
```

Resource states may include:

``` text
UPLOADED
PROCESSING
READY
FAILED
```

------------------------------------------------------------------------

# 75. Resource Versioning

If a course document changes, the system should avoid silently mixing
old and new content.

A resource should ideally have:

``` text
resource_id
version
created_at
updated_at
status
```

Vector entries should be traceable to the source version.

------------------------------------------------------------------------

# 76. Source Attribution

When RAG is used, responses should be able to identify supporting
sources where appropriate.

Example:

``` text
Source:
Machine Learning Notes — Section 4.2
```

The system must never fabricate source information.

------------------------------------------------------------------------

# 77. AI Evaluation

AI quality should be measured separately from conventional software
correctness.

Evaluation dimensions:

-   factual accuracy,
-   relevance,
-   groundedness,
-   helpfulness,
-   pedagogical quality,
-   appropriate difficulty,
-   prerequisite awareness,
-   hallucination rate,
-   instruction following.

A response can be grammatically excellent and still be educationally
wrong.

------------------------------------------------------------------------

# 78. Recommendation Evaluation

Metrics may include:

-   recommendation acceptance,
-   completion rate,
-   improvement in assessment performance,
-   mastery gain,
-   repeated recommendation rate,
-   ignored recommendation rate.

The system should eventually compare recommendation strategies.

------------------------------------------------------------------------

# 79. Security Model

Security should include:

``` text
Identity
  ↓
Authentication
  ↓
Authorization
  ↓
Input Validation
  ↓
Database Safety
  ↓
AI Safety
  ↓
Data Protection
```

Sensitive information should be minimized and protected.

------------------------------------------------------------------------

# 80. Privacy

Student learning data may include:

-   performance,
-   questions,
-   mistakes,
-   progress,
-   interaction history.

Access must be limited to authorized users.

The system should define retention policies before production
deployment.

------------------------------------------------------------------------

# 81. Database Indexing Strategy

Indexes should support frequent queries.

Likely candidates:

``` text
user_id
course_id
concept_id
student_id
session_id
created_at
```

Composite indexes may be required for common queries.

Indexes should be added based on actual query patterns rather than
indiscriminately.

------------------------------------------------------------------------

# 82. Referential Integrity

Deleting an entity must consider dependent entities.

Example:

``` text
Course
 ↓
Concept
 ↓
Student Progress
```

Deleting a concept may affect:

-   prerequisites,
-   attempts,
-   recommendations,
-   resources.

Deletion policies should therefore be explicitly defined.

Soft deletion may be preferable for historical learning data.

------------------------------------------------------------------------

# 83. API Pagination

Large collections should use pagination.

Example:

``` text
GET /courses/{id}/resources?page=1&page_size=20
```

Avoid returning thousands of records in a single API response.

------------------------------------------------------------------------

# 84. API Versioning

If breaking changes are expected:

``` text
/api/v1/...
```

Versioning should be introduced before public clients become dependent
on unstable contracts.

------------------------------------------------------------------------

# 85. Environment Strategy

Recommended environments:

``` text
Development
Testing
Staging
Production
```

Each should have:

-   separate configuration,
-   separate database,
-   separate secrets,
-   appropriate logging.

------------------------------------------------------------------------

# 86. Deployment Architecture

A production architecture could be:

``` text
                 Internet
                    ↓
              Load Balancer
                    ↓
              FastAPI Backend
             /       |       \
            /        |        \
     PostgreSQL   Vector DB   Object Storage
                       \
                        \
                         LLM Provider
```

Optional:

``` text
Redis / Cache
Queue / Worker
Monitoring
```

------------------------------------------------------------------------

# 87. Backup and Recovery

Production database strategy should include:

-   automated backups,
-   point-in-time recovery where supported,
-   restore testing,
-   migration rollback strategy,
-   disaster recovery plan.

A backup that has never been restored is not fully validated.

------------------------------------------------------------------------

# 88. Phase-Based Development Roadmap

## Phase 1 --- Planning & Architecture

Status: approximately 90% complete.

Deliverables:

-   product concept,
-   architecture,
-   data model,
-   technology decisions,
-   workflow planning.

## Phase 2 --- Environment + Git/GitHub

Status: complete.

Deliverables:

-   Python environment,
-   dependencies,
-   Git repository,
-   development setup.

## Phase 3 --- Backend + Database Foundation

Status: approximately 95--98% complete.

Implemented/validated areas include:

-   PostgreSQL,
-   Psycopg,
-   SQLAlchemy,
-   database models,
-   relationships,
-   constraints,
-   Alembic,
-   migration structure,
-   schema validation,
-   initial data,
-   Pytest setup,
-   Git integration.

Remaining completion work:

-   final automated test pass,
-   migration/schema consistency verification,
-   configuration/secrets cleanup.

## Phase 4 --- Backend APIs

Next major milestone.

Deliverables:

-   FastAPI application,
-   routers,
-   request/response schemas,
-   authentication,
-   services,
-   repositories,
-   error handling,
-   API tests.

## Phase 5 --- AI / RAG / Tutor Intelligence

Deliverables:

-   LLM abstraction,
-   intent detection,
-   concept identification,
-   retrieval,
-   prompt construction,
-   tutor generation,
-   response validation,
-   AI evaluation.

## Phase 6 --- Adaptive Learning

Deliverables:

-   mastery engine,
-   weak-area detection,
-   prerequisite diagnosis,
-   recommendation engine,
-   adaptive assessment.

## Phase 7 --- Frontend

Deliverables:

-   authentication UI,
-   dashboard,
-   course UI,
-   tutor interface,
-   progress,
-   assessments,
-   recommendations.

## Phase 8 --- Integration

Deliverables:

-   frontend/backend integration,
-   AI/database integration,
-   end-to-end workflows,
-   performance testing,
-   security testing.

## Phase 9 --- Deployment + Final Documentation

Deliverables:

-   production deployment,
-   CI/CD,
-   monitoring,
-   backups,
-   API documentation,
-   architecture documentation,
-   user documentation,
-   final project report.

------------------------------------------------------------------------

# 89. Definition of Done

A feature is not considered complete merely because its code exists.

A feature is complete when:

``` text
Requirement
 ↓
Implementation
 ↓
Validation
 ↓
Tests
 ↓
Error Handling
 ↓
Documentation
 ↓
Git Commit
 ↓
Integration Verification
```

------------------------------------------------------------------------

# 90. Phase 3 Definition of Done

Phase 3 is complete when:

-   PostgreSQL is accessible.
-   Psycopg connection works.
-   SQLAlchemy models represent required schema.
-   Relationships are correct.
-   Primary/foreign keys are correct.
-   Unique constraints are validated.
-   Check constraints are validated.
-   Alembic environment is configured.
-   Initial migration works.
-   Database can migrate to head.
-   Schema matches intended models.
-   Tests pass.
-   Test database state is isolated.
-   Configuration does not expose secrets.
-   Changes are committed to Git.

------------------------------------------------------------------------

# 91. Phase 4 Definition of Done

Phase 4 is complete when:

-   FastAPI application starts.
-   Database dependency injection works.
-   Core routers exist.
-   Request schemas validate input.
-   Response schemas validate output.
-   CRUD operations work.
-   Authentication works.
-   Authorization is enforced.
-   Errors are consistent.
-   API tests pass.
-   OpenAPI documentation is generated.
-   Database transactions are handled correctly.

------------------------------------------------------------------------

# 92. Phase 5 Definition of Done

Phase 5 is complete when:

-   LLM provider abstraction exists.
-   Retrieval pipeline works.
-   Documents can be indexed.
-   Relevant chunks can be retrieved.
-   Tutor prompts are constructed consistently.
-   Student context is injected safely.
-   Responses are validated.
-   AI failures are handled.
-   Tutor interactions are persisted.
-   Grounding/source behavior is tested.
-   Prompt injection risks are addressed.

------------------------------------------------------------------------

# 93. Phase 6 Definition of Done

Phase 6 is complete when:

-   mastery can be calculated,
-   prerequisite gaps can be detected,
-   weak concepts can be identified,
-   recommendation scores can be generated,
-   recommendations can be ranked,
-   recommendation explanations are available,
-   assessment evidence updates learning state,
-   recommendation tests pass.

------------------------------------------------------------------------

# 94. Critical Architectural Invariants

The following rules should remain true throughout development:

### Invariant 1

The frontend never becomes the source of truth for learning state.

### Invariant 2

The LLM is not the source of truth for database state.

### Invariant 3

Database schema changes are represented by migrations.

### Invariant 4

Business logic is not embedded inside API routes.

### Invariant 5

AI provider details are isolated behind an interface.

### Invariant 6

Student data access is authorization-controlled.

### Invariant 7

Recommendations are derived from structured learning evidence.

### Invariant 8

RAG content cannot override system safety/instruction hierarchy.

### Invariant 9

Critical state updates are transactional.

### Invariant 10

Tests must validate both application behavior and data integrity.

------------------------------------------------------------------------

# 95. Complete System Pipeline

The entire intended OpenTutor pipeline can be summarized as:

``` text
                 ┌──────────────────┐
                 │     Student      │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │    Frontend      │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │     FastAPI      │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Auth + Validation│
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Service Layer    │
                 └────────┬─────────┘
                          ↓
              ┌───────────┴───────────┐
              ↓                       ↓
     ┌────────────────┐      ┌────────────────┐
     │ Student State  │      │ Concept Graph  │
     └───────┬────────┘      └───────┬────────┘
             │                       │
             └───────────┬───────────┘
                         ↓
                ┌─────────────────┐
                │ Tutor Orchestr. │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Intent/Concept  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ RAG Retrieval   │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Prompt Builder  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ LLM / AI Tutor  │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Response Guard  │
                └────────┬────────┘
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
     ┌────────────────┐    ┌────────────────┐
     │ Interaction DB │    │ Learning State │
     └────────────────┘    └───────┬────────┘
                                   ↓
                          ┌─────────────────┐
                          │ Mastery Engine  │
                          └────────┬────────┘
                                   ↓
                          ┌─────────────────┐
                          │ Recommendation  │
                          │     Engine      │
                          └────────┬────────┘
                                   ↓
                          ┌─────────────────┐
                          │ Next Action     │
                          └────────┬────────┘
                                   ↓
                               Student
```

------------------------------------------------------------------------

# 96. Technology Responsibility Matrix

  Technology     Responsibility
  -------------- ---------------------------------
  Python         Core backend language
  FastAPI        HTTP/API layer
  PostgreSQL     Persistent relational data
  SQLAlchemy     ORM and database abstraction
  Psycopg        PostgreSQL driver
  Alembic        Database schema migrations
  Pytest         Automated testing
  Docker         Environment/containerization
  Git            Version control
  GitHub         Remote repository/collaboration
  Vector Store   Semantic retrieval
  LLM            Natural-language tutoring
  Frontend       User interface
  CI/CD          Automated validation/deployment

------------------------------------------------------------------------

# 97. Recommended Project Structure

A logical structure:

``` text
OpenTutor/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── dependencies/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── domain/
│   │   ├── ai/
│   │   │   ├── llm/
│   │   │   ├── retrieval/
│   │   │   ├── prompts/
│   │   │   └── tutor/
│   │   └── recommendations/
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── database/
│   │
│   ├── .env.example
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│
├── docs/
│
├── docker/
│
└── README.md
```

This is a target logical architecture; the actual repository structure
should remain authoritative.

------------------------------------------------------------------------

# 98. Future Extensions

Potential future capabilities:

-   voice tutoring,
-   multimodal tutoring,
-   diagram understanding,
-   handwritten answer analysis,
-   adaptive question generation,
-   spaced repetition,
-   knowledge tracing,
-   teacher dashboards,
-   collaborative learning,
-   gamification,
-   multilingual tutoring,
-   offline/local LLM support,
-   personalized study schedules.

These should be implemented without violating the core architecture.

------------------------------------------------------------------------

# 99. Risks

## Technical Risks

-   LLM hallucination.
-   Retrieval quality.
-   Poor chunking.
-   Incorrect prerequisite graphs.
-   Database migration errors.
-   Slow AI inference.
-   Poor recommendation scoring.
-   Context-window limitations.
-   concurrency issues.

## Product Risks

-   Students over-relying on AI.
-   Recommendations becoming repetitive.
-   Incorrect personalization.
-   Explanations being too advanced/simple.
-   Low trust in recommendations.

## Operational Risks

-   API provider outages.
-   Database failure.
-   vector-store failure.
-   secret leakage.
-   insufficient monitoring.

------------------------------------------------------------------------

# 100. Risk Mitigation

  Risk                    Mitigation
  ----------------------- ---------------------------------------------
  Hallucination           RAG + response validation
  Bad retrieval           metadata filters + reranking
  Wrong recommendations   explainability + evaluation
  Migration failure       Alembic + CI validation
  Database corruption     transactions + backups
  LLM outage              fallback/error strategy
  Prompt injection        instruction hierarchy + content isolation
  API abuse               auth + rate limiting
  Secret leakage          environment variables + secret scanning
  Poor performance        caching + profiling + async/background work

------------------------------------------------------------------------

# 101. Final Architectural Principle

OpenTutor should not be viewed as:

``` text
Chatbot + Database
```

It should be viewed as:

``` text
Learning State
      +
Concept Graph
      +
Assessment Evidence
      +
Retrieval
      +
LLM Tutor
      +
Recommendation Engine
      +
Persistent Backend
      =
Adaptive Learning System
```

The intelligence of the platform comes from the interaction between
structured learning data and generative AI.

The database tells the system what is known about the learner.

The concept graph tells the system how knowledge is related.

Assessments provide evidence.

Retrieval provides grounded information.

The LLM provides natural-language tutoring.

The recommendation engine determines what should happen next.

The backend orchestrates all of these components.

The frontend exposes the resulting learning experience.

------------------------------------------------------------------------

# 102. One-Line System Explanation

> **OpenTutor is an adaptive AI tutoring platform where FastAPI
> orchestrates learner state, PostgreSQL-backed learning data,
> prerequisite relationships, RAG retrieval, LLM-based tutoring,
> assessment evidence, and recommendation logic to continuously
> personalize the student's next learning action.**

------------------------------------------------------------------------

# 103. Engineering Mental Model

When implementing any new OpenTutor feature, ask:

``` text
1. What user problem does it solve?
2. Which API owns the operation?
3. Which service contains the business logic?
4. Which database entities are involved?
5. Does the schema require a migration?
6. What learning state changes?
7. Does AI need to be involved?
8. Does retrieval need to be involved?
9. What happens if the dependency fails?
10. What tests prove it works?
11. How is it observed in production?
12. Can the behavior be reproduced from stored data?
```

If these questions have clear answers, the feature is architecturally
grounded.

------------------------------------------------------------------------

# 104. Current Project Position

OpenTutor has completed most of the foundational backend/database work.

Current engineering chain:

``` text
Python
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL
   ↓
Alembic
   ↓
Pytest
```

The immediate milestone is to finish the remaining Phase 3 validation
and then move into:

``` text
FastAPI
   ↓
Backend APIs
   ↓
Services
   ↓
Tutor Orchestration
   ↓
RAG + AI
   ↓
Adaptive Learning
   ↓
Frontend
   ↓
Integration
   ↓
Deployment
```

This sequence intentionally establishes reliable data and application
foundations before introducing the more complex AI pipeline.

------------------------------------------------------------------------

# 105. Final Success Definition

OpenTutor is successful when a student can enter the system, learn a
concept, ask a natural-language question, receive a grounded explanation
appropriate to their learning state, practice the concept, have the
system update evidence about their mastery, identify prerequisite gaps
where necessary, and receive a meaningful next recommendation --- all
through a reliable, testable, secure, and maintainable software
architecture.
