# OpenTutor Recommendation Engine

## Overview

OpenTutor uses an adaptive recommendation pipeline to determine which concept a learner should work on next.

The recommendation system does not rely on a single signal such as percentage accuracy. It combines learner mastery, confidence, revision urgency, concept difficulty, and prerequisite readiness.

The current pipeline is:

Student Interaction
        ↓
Learner State
        ↓
Mastery + Confidence
        ↓
Revision State
        ↓
Revision Need
        ↓
Adaptive Decision Layer
        ↓
Concept Priority
        ↓
Next Concept
        ↓
Recommendation Reason


## 1. Learner State

OpenTutor maintains a learner state for each user and concept.

The state includes:

- mastery
- confidence
- attempts count
- correct count
- last attempt timestamp

Mastery represents the estimated state of knowledge rather than simply storing the learner's percentage of correct answers.

Confidence represents the learner's reported confidence and is normalized to a value between 0 and 1.


## 2. Bayesian Knowledge Tracing

OpenTutor uses Bayesian Knowledge Tracing (BKT) to update mastery.

The BKT model contains:

- Initial knowledge
- Learning rate
- Guess probability
- Slip probability

For each new response, the learner's knowledge estimate is updated according to whether the response was correct or incorrect.

This allows the system to maintain an evolving estimate of knowledge instead of treating every question independently.


## 3. Prerequisite Awareness

Concepts can have prerequisite relationships.

Before recommending a concept, OpenTutor checks whether all of its prerequisites have reached the required mastery threshold.

The current prerequisite mastery threshold is:

0.70

If a prerequisite is missing or its mastery is below the threshold, the dependent concept is not recommended.


## 4. Revision State

OpenTutor maintains a separate revision state for concepts.

The revision state contains information such as:

- stability
- difficulty
- retrievability
- last review time
- next review time
- review count

This allows the recommendation engine to account for forgetting and revision needs.


## 5. Retrievability

Retrievability estimates how likely the learner is to successfully recall a concept at a given point in time.

The current implementation uses elapsed time and memory stability to calculate a value between 0 and 1.

As more time passes after a review, retrievability decreases.

This produces a revision urgency signal for the recommendation engine.


## 6. Revision Scheduling

OpenTutor calculates a target review interval from concept stability and a target retrievability.

The current default target retrievability is:

0.90

Review intervals are bounded between:

- 1 day minimum
- 30 days maximum

A concept becomes increasingly important to review as its scheduled review point approaches.


## 7. Adaptive Decision Layer

The adaptive decision layer combines four signals:

| Signal | Weight |
|---|---:|
| Mastery gap | 40% |
| Confidence gap | 20% |
| Revision need | 30% |
| Difficulty | 10% |

The resulting priority is constrained to the range 0 to 1.

Concepts with a higher priority have a stronger reason to be selected as the learner's next concept.


## 8. Mastery Gap

Mastery gap is calculated as:

mastery gap = 1 - mastery

Therefore:

- low mastery → large mastery gap
- high mastery → small mastery gap

This gives concepts with weaker mastery greater priority.


## 9. Confidence Gap

Confidence gap is calculated as:

confidence gap = 1 - confidence

This allows the recommendation system to distinguish between learners who have similar mastery but different confidence levels.

For example:

Learner A:

- mastery = 0.60
- confidence = 0.20

Learner B:

- mastery = 0.60
- confidence = 0.90

The adaptive layer assigns greater priority to the concept associated with the lower confidence state.


## 10. Recommendation Policies

OpenTutor includes an evaluation module that compares three policies.

### Mastery-only baseline

The baseline uses only mastery gap.

This provides a simple reference point for evaluating more complex policies.

### Revision-aware policy

The revision-aware policy combines:

- mastery gap
- revision need

The current weighting is:

- mastery gap: 60%
- revision need: 40%

### Adaptive policy

The adaptive policy combines:

- mastery gap
- confidence gap
- revision need
- difficulty

This is the primary recommendation policy currently used by the recommendation service.


## 11. Recommendation Evaluation

The evaluation module can calculate priorities for the same learner state under all three policies.

This allows controlled comparison without changing the learner state between policies.

For each evaluation sample, the system calculates:

- mastery-only priority
- revision-aware priority
- adaptive priority

Average priorities can then be calculated across multiple learner states.


## 12. Recommendation Reasons

OpenTutor also generates an explanation for the selected recommendation.

Possible reasons include:

- significant practice is required
- confidence is low
- revision is due
- revision is approaching
- additional practice can improve mastery
- the concept is challenging
- the concept is the next suitable concept

The explanation is generated from the learner state and revision information rather than being an unrelated generic message.


## 13. Recommendation Flow

The current recommendation flow is:

1. Identify the learner's enrolled courses.
2. Retrieve concepts belonging to those courses.
3. Check prerequisite readiness.
4. Retrieve the learner state.
5. Retrieve the revision state.
6. Calculate revision need.
7. Calculate adaptive priority.
8. Compare priorities across eligible concepts.
9. Select the highest-priority concept.
10. Generate a reason for the recommendation.


## 14. Testing

The recommendation system is covered by unit and service-level tests.

The tests currently verify:

- low mastery increases priority
- low confidence increases priority
- revision need increases priority
- priority remains within valid bounds
- invalid difficulty configuration raises an error
- prerequisites can block recommendations
- mastery affects recommendation selection
- revision urgency can affect recommendation selection
- confidence affects recommendation selection
- recommendation reasons reflect learner state
- recommendation policies can be compared
- empty evaluation input is handled safely

The full backend test suite currently passes.


## 15. Current Scope

The current recommendation engine is a deterministic adaptive-learning component.

It does not attempt to replace a general-purpose language model.

Instead, the architecture separates:

### Adaptive learning logic

Responsible for:

- learner state
- mastery estimation
- revision
- prerequisites
- prioritization
- recommendation

### Future AI tutor layer

Responsible for:

- natural-language explanations
- Socratic interaction
- hints
- examples
- conversational tutoring

This separation allows the tutoring interface and underlying learning policy to evolve independently.


## 16. Future Extensions

Potential future improvements include:

- Item Response Theory (IRT)
- stronger forgetting models
- FSRS-based revision scheduling
- Socratic tutoring levels
- misconception detection
- disengagement and gaming detection
- curriculum alignment
- larger-scale recommendation evaluation
- offline learner simulation
- LLM-assisted explanations
- personalized question difficulty selection