# OpenTutor — Detailed PRD v2.0

This document consolidates the current architecture, completed foundation, revised AI/adaptive-learning roadmap, workflows, pipelines, data model, testing strategy and research direction.

# OpenTutor — Detailed Product Requirements Document (PRD) v2.0
**Status:** Active Development  
**Updated:** September 2026  
**Repository:** `anoopreddy2007/OpenTutor`

OpenTutor is an open-source, measurable adaptive-learning platform. It explicitly models learner knowledge, memory, confidence, prerequisite readiness and interaction evidence, then uses those signals to decide what the learner should study, practice, review or receive help with.

The core principle is: **the LLM is the language layer, not the source of truth for learner state.**

The product therefore separates:
- deterministic learner-state computation,
- knowledge/prerequisite modeling,
- adaptive assessment,
- spaced revision,
- tutoring policy,
- RAG,
- LLM generation,
- evaluation.

OpenTutor is not a foundation model. Its technical value is the adaptive-learning system surrounding an interchangeable LLM.

# 1. Vision, Goals & Non-Goals

## Vision
Build an open, reproducible tutor where every learning interaction becomes structured evidence, evidence updates an explicit learner model, and the learner model controls subsequent tutoring and assessment.

## Product Goals
1. Explicit learner modeling per learner/concept.
2. Adaptive sequencing instead of static course order.
3. Learning-science algorithms: BKT, FSRS and eventually IRT.
4. Deterministic Socratic tutoring control.
5. Grounded RAG-based explanations.
6. Explainable recommendations.
7. Repeatable evaluation of personalization and outcomes.
8. Open and reproducible experiments.

## Non-Goals
- Training a foundation LLM from scratch.
- Competing with GPT/Claude/Gemini as general LLMs.
- Supporting every subject immediately.
- Replacing teachers.
- Allowing generated text to become authoritative learner-state data.
- Implementing data-hungry models before sufficient interaction data exists.

# 2. Master Architecture

```text
                         LEARNER
                            |
                     OpenTutor Frontend
                            |
                          FastAPI
                            |
          +-----------------+------------------+
          |                 |                  |
       Content            Attempts            Tutor
          |                 |                  |
          |                 v                  |
          |          Evidence Processing       |
          |                 |                  |
          |        +--------+--------+         |
          |        |                 |         |
          |       BKT          Metacognition   |
          |        |                 |         |
          |        +--------+--------+         |
          |                 |                  |
          |            Learner State           |
          |                 |                  |
          |             +---+---+              |
          |             |       |              |
          |            FSRS    IRT             |
          |             |       |              |
          +-------------+-------+--------------+
                        |
                 Adaptive Policy
                        |
          +-------------+-------------+
          |             |             |
    Recommendation   Assessment   Tutor Level
          |             |             |
          +-------------+-------------+
                        |
                   TutorService
                    /                          RAG     Socratic Policy
                    \        /
                     LLM Interface
                          |
                 Provider Adapters
                          |
                    Tutor Response
                          |
                       Learner
                          |
                          +----> New Evidence
```

## Architectural Separation

**RAG:** what information should be used?  
**Learner model:** what does this learner probably know/remember?  
**Policy:** how much help should be provided?  
**LLM:** how should the response be phrased?

The LLM must not directly write mastery, prerequisite readiness, revision dates or recommendation truth.

# 3. Core Data Model

```text
User
 | | +---- Enrollment ---- Course ---- Topic ---- Concept
 |                                           /   |   \
 |                                          /    |    \
 |                              Prerequisite   Question
 |                                                   |
 +------------------------------------------------ Attempt
 |
 +------------------------------ LearnerState ---- Concept
```

## Current entities

### User
`id, username, email, created_at`

### Course
`id, name, description, created_at`

### Topic
`id, course_id, name, description, order_index`

### Concept
`id, topic_id, name, description, difficulty`

### Question
`id, concept_id, question_text, question_type, difficulty, options, correct_answer, explanation, created_at`

### Attempt
`id, user_id, question_id, answer, is_correct, time_taken, confidence, created_at`

### LearnerState
`id, user_id, concept_id, mastery, confidence, attempts_count, correct_count, last_attempt_at, updated_at`

### Enrollment
`id, user_id, course_id, enrolled_at`

### ConceptPrerequisite
`id, concept_id, prerequisite_concept_id`

## Important invariants
- learner state is unique per user/concept;
- confidence on attempts is 1–5 or null;
- learner mastery/confidence are bounded;
- correct count cannot exceed attempts;
- no self-prerequisite;
- duplicate prerequisite edges are prohibited;
- foreign keys are valid;
- transactions preserve consistency.

## Future state fields
BKT: probability known, learning parameters and evidence metadata.  
FSRS: difficulty, stability, retrievability, next review time, review count.  
IRT: learner ability and item discrimination/difficulty parameters.  
Interaction quality: hints, session, input modality, suspicious-interaction score.

# 4. Master Workflows

## 4.1 Complete Learning Session

```text
Open Course
 -> Load Enrollment
 -> Load Concept Graph
 -> Load Learner State
 -> Generate Eligible Candidates
 -> Apply Prerequisite Filter
 -> Apply Revision/Assessment Policy
 -> Select Concept/Question
 -> Present Content
 -> Learner Answers
 -> Capture Correctness + Confidence + Time + Hints
 -> Persist Attempt
 -> Update Learner Model
 -> Update BKT
 -> Update FSRS
 -> Recalculate Recommendation
 -> Determine Tutor Policy
 -> Retrieve Grounded Context
 -> Generate Tutor Response
 -> Log Interaction
 -> Continue Session
```

## 4.2 Answer Submission

```text
POST /attempts
 -> validate user/question
 -> score answer
 -> persist Attempt
 -> update learner state
 -> update BKT
 -> update FSRS
 -> recompute recommendation
 -> return result/state
```

## 4.3 Recommendation

```text
Enrollment
 -> Course Concepts
 -> Prerequisite Eligibility
 -> Learner State
 -> BKT Knowledge
 -> FSRS Review Need
 -> IRT Information (later)
 -> Interaction Reliability
 -> Adaptive Ranking
 -> Recommended Learning Action
 -> Explain Decision
```

## 4.4 Tutor

```text
User Message
 -> identify interaction
 -> load concept
 -> load learner state
 -> load prerequisites
 -> load hint history/time/attempts
 -> deterministic Socratic level
 -> RAG retrieval
 -> construct context
 -> LLM generation
 -> response validation
 -> tutor response
 -> interaction evidence
```

## 4.5 RAG

```text
Approved Material
 -> clean
 -> chunk
 -> metadata
 -> embed
 -> vector store
 -> query
 -> retrieve
 -> rerank (optional)
 -> grounded context
 -> TutorService
 -> LLM
```

## 4.6 Handwritten Input (later)

```text
Image
 -> OCR/Vision
 -> structured student work
 -> concept identification
 -> misconception/evidence extraction
 -> learner model
 -> tutor/recommendation
```


# 5. Learning Intelligence

## 5.1 Bayesian Knowledge Tracing (BKT)

BKT replaces the current placeholder mastery function.

Parameters:
- `P(L0)` initial knowledge probability;
- `P(T)` learning/transition probability;
- `P(G)` guess probability;
- `P(S)` slip probability.

```text
Initial P(Knowledge)
 -> response evidence
 -> Bayesian update
 -> learning transition
 -> new P(Knowledge)
```

A correct answer is not automatically proof of knowledge because guessing exists. An incorrect answer is not automatically proof of ignorance because slips exist.

Implementation:
1. deterministic update function;
2. learner/concept state;
3. unit tests;
4. calibration from data;
5. comparison against current heuristic baseline.

## 5.2 FSRS

FSRS replaces simplistic recency scoring with memory scheduling.

State:
- Difficulty
- Stability
- Retrievability
- Next review time

```text
Learning
 -> initial memory state
 -> time passes
 -> retrievability falls
 -> review becomes due
 -> review result
 -> FSRS update
 -> next review
```

Recommendation should consider review urgency rather than only elapsed time.

## 5.3 Item Response Theory (IRT)

A basic 2PL model:

`P(correct) = 1 / (1 + e^(-a(θ-b)))`

Where:
- `θ` = learner ability,
- `a` = item discrimination,
- `b` = item difficulty.

Question selection eventually uses information/Fisher information rather than a hand-written difficulty score.

IRT should be delayed until sufficient response data exists for meaningful calibration.

## 5.4 Knowledge Graph

Prerequisites define eligibility:

```text
Variables -> Functions -> Recursion -> Trees -> Graph Algorithms
```

If a prerequisite is below the configured readiness threshold, the advanced concept is blocked or the learner is redirected.

Future:
- cycle detection,
- prerequisite strength,
- alternative prerequisites,
- curriculum mapping,
- graph visualization.

# 6. AI Tutor System

## 6.1 TutorService

TutorService combines:

```text
User message
+ concept
+ learner state
+ prerequisites
+ attempt history
+ hint history
+ retrieved knowledge
+ tutoring policy
```

## 6.2 Deterministic Socratic Ladder

The application chooses the level; the LLM only generates natural language.

### L1 — Leading Question
Guide the learner to the next reasoning step.

### L2 — Prerequisite Pointer
Identify the specific missing prerequisite.

### L3 — Partial Example
Provide part of the reasoning or a partially completed example.

### L4 — Full Explanation
Provide a complete explanation after escalation.

Inputs to policy:
- hint count,
- attempts,
- time-on-task,
- mastery/knowledge estimate,
- confidence,
- previous interactions.

```text
Interaction
 -> Policy Engine
 -> L1/L2/L3/L4
 -> RAG
 -> LLM
 -> Response
```

## 6.3 Metacognition

Capture confidence before correctness is revealed and occasionally ask what the learner already knows.

Useful evidence combinations:

| Correct | Confidence | Interpretation |
|---|---|---|
| Yes | High | strong evidence |
| Yes | Low | potentially fragile knowledge |
| No | High | possible misconception |
| No | Low | uncertain/weak knowledge |

Confident-wrong responses should trigger stronger diagnostic reasoning rather than simply lowering a score.

# 7. Recommendation Engine

## Current baseline

The current recommendation engine is a stepping stone:

`Priority = 0.50 * mastery_gap + 0.30 * revision_need + 0.20 * difficulty_fit`

with prerequisite readiness and enrollment filtering.

This is intentionally treated as a baseline, not the final intelligence layer.

## Target

```text
Candidates
 -> Enrollment filter
 -> Prerequisite filter
 -> BKT knowledge
 -> FSRS retrievability/review urgency
 -> IRT information
 -> interaction reliability
 -> adaptive policy/ranking
 -> next learning action
```

Every recommendation should expose machine-readable reasoning:

```json
{
  "decision": "recommend_concept",
  "concept_id": 12,
  "signals": {
    "knowledge_gap": 0.64,
    "review_urgency": 0.81,
    "prerequisite_ready": true
  },
  "reason": "Weak knowledge estimate and high review urgency."
}
```

The system should eventually recommend not only a concept but an action:

`LEARN | PRACTICE | REVIEW | REVISIT_PREREQUISITE | ASSESS`.

# 8. Evaluation & Research

Evaluation is a core product component.

## 8.1 Test layers

### Unit
BKT, FSRS, IRT math, prerequisite logic, ranking.

### Integration
`Attempt -> Learner State -> Recommendation`

### Tutor Policy
Same question under different learner states must produce different permitted assistance levels.

### RAG
Retrieval relevance, groundedness and hallucination checks.

### End-to-End
Simulated learner sessions.

## 8.2 Personalization Test

Student A:
`mastery 0.85, hints 0`

Expected: challenge-oriented, low scaffolding.

Student B:
`mastery 0.25, hints 2`

Expected: prerequisite review and stronger scaffolding.

Student C:
`mastery 0.40, confidence 5, incorrect`

Expected: misconception-oriented intervention.

The evaluation must test whether state actually changes behavior rather than assuming that including state in a prompt is personalization.

## 8.3 Metrics

Learning:
- pre/post mastery gain;
- delayed retention;
- attempts to mastery;
- prerequisite recovery.

Recommendation:
- recommendation success;
- mastery improvement after recommendation;
- revision completion;
- inappropriate recommendation rate.

Assessment:
- information gain;
- prediction/calibration;
- question efficiency.

Tutor:
- Socratic-level compliance;
- groundedness;
- factual accuracy;
- hint appropriateness;
- misconception detection;
- learning progress after intervention.

## 8.4 Ablation

Compare:
1. heuristic baseline;
2. BKT;
3. BKT + FSRS;
4. BKT + FSRS + IRT;
5. full adaptive tutor.

Remove individual components to measure their actual contribution.

# 9. Phase-Wise Roadmap

## PHASE 0 — Foundation
**Goal:** professional repo/environment.
- GitHub, README, license, gitignore;
- Python environment;
- Docker/PostgreSQL;
- CI foundation.

**Gate:** clean clone works, DB starts, tests run.

## PHASE 1 — Backend Foundation
- FastAPI;
- database connection;
- SQLAlchemy Base;
- configuration;
- health endpoint;
- initial tests.

**Gate:** API and DB foundation stable.

## PHASE 2 — Core Database
- User;
- Course;
- Topic;
- Concept;
- Question;
- Attempt;
- Alembic migrations and constraints.

**Gate:** educational domain can be persisted reliably.

## PHASE 3 — Learner State & Adaptive Foundation
**Current phase: essentially complete.**

Completed:
- LearnerState;
- Enrollment;
- ConceptPrerequisite;
- uniqueness/graph hardening;
- learner-state service;
- baseline recommendation;
- forgetting-aware recommendation;
- tests.

Remaining hardening:
- dedicated revision tests;
- timezone-aware datetime cleanup;
- edge-case tests.

**Gate:** complete DB-level learning loop is stable.

## PHASE 4 — API Layer
**Next major phase.**

Build:
- Pydantic schemas;
- user/course/topic/concept/question APIs;
- enrollment API;
- attempt submission API;
- learner-state API;
- recommendation API;
- validation/error handling;
- API integration tests.

Target flow:

`User -> Course -> Concept -> Question -> Attempt -> LearnerState -> Recommendation`

## PHASE 5 — AI / RAG / Tutor
Build:
- provider-agnostic LLM interface;
- provider adapters;
- ingestion/chunking/retrieval;
- TutorService;
- Socratic ladder;
- metacognitive prompts;
- basic evaluation harness.

**Gate:** tutor demonstrates measurable state-dependent behavior.

## PHASE 6 — Adaptive Learning
This is the main learning-science phase.
- BKT;
- FSRS;
- learner-state migration from heuristic mastery;
- adaptive recommendation upgrade;
- revision queue;
- feedback loop;
- adaptive question selection groundwork.

**Gate:** advanced algorithms demonstrably improve decisions over baseline.

## PHASE 7 — IRT / Advanced Assessment
- item parameters;
- learner ability;
- Fisher information;
- adaptive question selection;
- calibration;
- simulations;
- evaluation.

## PHASE 8 — Advanced Learner Analytics
- rapid guessing;
- hint abuse;
- suspicious interaction patterns;
- evidence reliability;
- confidence calibration;
- only later, DKT/learned policies if enough data exists.

## PHASE 9 — Content Authoring
- syllabus/textbook ingestion;
- LLM concept extraction;
- prerequisite proposals;
- question generation;
- human review;
- draft/pending/approved/published states.

## PHASE 10 — Multimodal
- image upload;
- OCR/vision;
- structured work extraction;
- concept/misconception detection;
- learner evidence integration.

## PHASE 11 — Curriculum Alignment
Create bounded curriculum packs containing:
- syllabus;
- topics;
- concepts;
- prerequisites;
- learning objectives;
- questions.

The core adaptive engine remains curriculum-agnostic.

## PHASE 12 — Research Benchmarking
- synthetic learner simulator;
- baseline comparisons;
- ablations;
- reproducible configurations;
- datasets;
- reports;
- limitations.

# 10. Repository & Frontend Architecture

## Target repository

```text
OpenTutor/
├── .github/workflows/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   └── README.md
├── ai/
│   ├── llm/
│   ├── rag/
│   ├── tutoring/
│   └── prompts/
├── training/
│   ├── bkt/
│   ├── fsrs/
│   ├── irt/
│   └── simulation/
├── evaluation/
│   ├── scenarios/
│   ├── metrics/
│   ├── tutor/
│   └── reports/
├── datasets/
├── frontend/
├── notebooks/
├── scripts/
├── docker/
├── docs/
├── docker-compose.yml
├── README.md
└── LICENSE
```

## Frontend

### Dashboard
- course;
- progress;
- current target;
- review queue;
- recent performance.

### Learning screen
- concept;
- question;
- answer;
- confidence;
- submit.

### Tutor panel
- explanation;
- hints;
- Socratic interaction;
- prerequisite pointer;
- escalation control.

### Revision queue
- due now;
- due soon;
- upcoming.

### Recommendation explanation
Show why the system selected the next activity.

# 11. Security, Privacy & Operations

## LLM safety
- protect system/developer instructions from prompt injection;
- treat retrieved documents as untrusted data;
- validate generated output;
- never let LLM text mutate authoritative learner state.

## Privacy
Learner state is sensitive educational information.
- minimize stored personal data;
- secure database access;
- anonymize research datasets;
- obtain consent where required.

## Failure handling

```text
LLM unavailable
 -> deterministic fallback
 -> preserve learner state
 -> log failure
```

## Observability
Track:
- API latency;
- database errors;
- LLM latency/errors;
- retrieval latency;
- recommendation decisions;
- tutor policy level;
- evaluation failures.

Avoid logging unnecessary sensitive learner content.

# 12. Definition of Done

## MVP
- [ ] User/course/content APIs work.
- [ ] Enrollment works.
- [ ] Attempt submission works.
- [ ] Learner state updates automatically.
- [ ] Prerequisites affect recommendations.
- [ ] Recommendation explanations exist.
- [ ] RAG retrieves approved course material.
- [ ] TutorService generates grounded responses.
- [ ] Socratic escalation is deterministic.
- [ ] Confidence is captured.
- [ ] BKT is implemented and tested.
- [ ] FSRS is implemented and tested.
- [ ] Basic adaptive recommendation works.
- [ ] Evaluation harness runs reproducibly.
- [ ] Frontend supports a complete learner session.
- [ ] CI passes.
- [ ] Documentation is complete.

## Research-grade release
Additionally:
- [ ] IRT calibration.
- [ ] synthetic learner simulator.
- [ ] baseline comparisons.
- [ ] tutor personalization evaluation.
- [ ] recommendation outcome evaluation.
- [ ] retention experiments.
- [ ] ablation studies.
- [ ] reproducible experiment configs.
- [ ] dataset documentation.
- [ ] privacy-preserving logs.
- [ ] limitations documented.

# 13. Final Product Positioning

OpenTutor should be described as:

> **An open-source adaptive learning system that explicitly models learner knowledge, memory and learning behavior, then uses those estimates to control assessment, revision and AI tutoring.**

Not simply:

> An AI tutor powered by an LLM.

The complete intelligence stack is:

```text
Learner Evidence
      |
      v
Knowledge Graph
      |
      +--> BKT --------+
      |                |
      +--> FSRS -------+--> Adaptive Policy
      |                |
      +--> IRT --------+
      |
      v
Recommendation / Assessment
      |
      v
Socratic Tutor Policy
      |
      v
RAG
      |
      v
LLM
      |
      v
Learner Response
      |
      +------> New Evidence
```

## Immediate execution order

```text
PHASE 3 COMPLETE
      |
      v
PHASE 4 — APIs
      |
      v
PHASE 5 — RAG + Tutor + Socratic + Evaluation
      |
      v
PHASE 6 — BKT + FSRS
      |
      v
PHASE 7 — IRT
      |
      v
PHASE 8 — Advanced Analytics
      |
      v
PHASE 9 — Authoring
      |
      v
PHASE 10 — Multimodal
      |
      v
PHASE 11 — Curriculum
      |
      v
PHASE 12 — Research Benchmarking
```

## Four-question engineering rule

Every new feature must answer:

1. What learner problem does it solve?
2. What data does it consume?
3. What decision/output does it produce?
4. How will we evaluate whether it works?

If it cannot answer these, it does not belong in the core adaptive engine yet.

## Final architectural principle

```text
Evidence
  ↓
Learner Modeling
  ↓
Learning Science
  ↓
Adaptive Decision
  ↓
Controlled Tutoring
  ↓
LLM Generation
  ↓
Measured Outcome
  ↓
New Evidence
```

This feedback loop is the defining architecture of OpenTutor.
