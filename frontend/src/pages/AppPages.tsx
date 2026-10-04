import { useEffect, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock3,
  FileText,
  Filter,
  Flame,
  Lock,
  MessageSquare,
  Play,
  Search,
  Sparkles,
  Target,
  Trophy,
  Video,
  Zap
} from 'lucide-react'

import { concepts, history, recommendations } from '../data/mock'

import {
  ArrowButton,
  Button,
  Card,
  MasteryRing,
  Metric,
  ProgressBar,
  RecommendationIcon,
  SectionTitle,
  StatusIcon
} from '../components/UI'

import MatrixOrb from '../components/animated/MatrixOrb'
import StepPlayer from '../components/animated/StepPlayer'
import BounceSidebar from '../components/animated/BounceSidebar'
import GridReveal from '../components/animated/GridReveal'
import GooeyNav from '../components/animated/GooeyNav'
import ProximitySidebar from '../components/animated/ProximitySidebar'
import ScrollProgress from '../components/animated/ScrollProgress'
import DurationPicker from '../components/animated/DurationPicker'
import TaskList from '../components/animated/TaskList'
import DeleteButton from '../components/animated/DeleteButton'

import {
  getQuestion,
  submitAttempt,
  getLearnerStates,
  getUserAttempts,
  getNextRecommendation,
  type LearnerState,
  type Attempt,
  type Recommendation,
  type Question,
  type AttemptResponse,
} from '../services/api'


export function Dashboard() {
  const nav = useNavigate()

  const TEST_USER_ID = 630

  const [learnerStates, setLearnerStates] = useState<LearnerState[]>([])
  const [attempts, setAttempts] = useState<Attempt[]>([])
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let mounted = true

    async function loadDashboard() {
      try {
        setLoading(true)
        setError('')

        const [states, userAttempts, nextRecommendation] = await Promise.all([
          getLearnerStates(TEST_USER_ID),
          getUserAttempts(TEST_USER_ID),
          getNextRecommendation(TEST_USER_ID),
        ])

        if (!mounted) return

        setLearnerStates(states)
        setAttempts(userAttempts)
        setRecommendation(nextRecommendation)
      } catch (err) {
        if (mounted) {
          setError(
            err instanceof Error
              ? err.message
              : 'Failed to load learner dashboard data.'
          )
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadDashboard()

    return () => {
      mounted = false
    }
  }, [])

  const overallMastery = learnerStates.length
    ? learnerStates.reduce((sum, state) => sum + state.mastery, 0) /
      learnerStates.length
    : 0

  const overallConfidence = learnerStates.length
    ? learnerStates.reduce((sum, state) => sum + state.confidence, 0) /
      learnerStates.length
    : 0

  const totalAttempts = attempts.length
  const correctAttempts = attempts.filter((attempt) => attempt.is_correct).length
  const accuracy = totalAttempts
    ? correctAttempts / totalAttempts
    : 0

  const masteredConcepts = learnerStates.filter(
    (state) => state.mastery >= 0.8
  ).length

  const conceptsNeedingPractice = learnerStates.filter(
    (state) => state.mastery < 0.7
  ).length

  const recentAttempt = attempts.length
    ? [...attempts].sort(
        (a, b) =>
          new Date(b.created_at).getTime() -
          new Date(a.created_at).getTime()
      )[0]
    : null

  const weakestState = learnerStates.length
    ? [...learnerStates].sort((a, b) => a.mastery - b.mastery)[0]
    : null

  const masteryPercent = Math.round(overallMastery * 100)
  const confidencePercent = Math.round(overallConfidence * 100)
  const accuracyPercent = Math.round(accuracy * 100)

  return (
    <>
      <div className="page-heading">
        <SectionTitle
          eyebrow="LEARNER OVERVIEW"
          title="Good morning, Anoop."
          description={
            loading
              ? 'Synchronizing your learner state with the adaptive engine.'
              : 'Your learning state is synchronized. Here is the next useful place to focus.'
          }
        />

        <Button onClick={() => nav('/app/tutor')}>
          Ask Tutor <MessageSquare size={16} />
        </Button>
      </div>

      {error && (
        <Card>
          <span className="eyebrow">DASHBOARD ERROR</span>
          <p className="lead" style={{ marginTop: '0.75rem' }}>
            {error}
          </p>
        </Card>
      )}

      <div className="dashboard-grid">
        <Card className="continue-card">
          <div className="continue-copy">
            <span className="eyebrow">ADAPTIVE LEARNING STATE</span>

            <h2>Python Fundamentals</h2>

            <p>
              {weakestState
                ? <>Current focus: <b>Concept {weakestState.concept_id}</b></>
                : <>Complete an assessment to establish your learner state.</>}
            </p>

            <div className="inline-progress">
              <ProgressBar value={masteryPercent} />
              <span>{masteryPercent}%</span>
            </div>

            <Button onClick={() => nav('/app/assessment')}>
              Continue Learning <ArrowRight size={16} />
            </Button>
          </div>

          <MasteryRing value={masteryPercent} size={128} />
        </Card>

        <div className="metric-grid">
          <Metric
            label="Mastery"
            value={`${masteryPercent}%`}
            sub={`${learnerStates.length} tracked concepts`}
            tone="primary"
          />

          <Metric
            label="Confidence"
            value={`${confidencePercent}%`}
            sub="Average learner confidence"
            tone="warning"
          />

          <Metric
            label="Accuracy"
            value={`${accuracyPercent}%`}
            sub={`${correctAttempts}/${totalAttempts} correct`}
            tone="success"
          />
        </div>
      </div>

      <div className="two-col">
        <Card>
          <div className="card-head">
            <div>
              <span className="eyebrow">ADAPTIVE QUEUE</span>
              <h3>Recommended next</h3>
            </div>

            <Link to="/app/recommendations">
              View all
            </Link>
          </div>

          {recommendation ? (
            <div className="recommend-list">
              <div className="recommend-row">
                <div className="recommend-icon"><Zap size={18} /></div>

                <div>
                  <strong>
                    Concept {recommendation.concept_id ?? '—'}
                  </strong>
                  <span>
                    {recommendation.reason ?? 'Continue with the next adaptive learning action.'}
                  </span>
                </div>

                <ArrowRight size={16} />
              </div>
            </div>
          ) : (
            <p className="muted">
              No recommendation is available yet. Complete an assessment to generate one.
            </p>
          )}
        </Card>

        <Card>
          <div className="card-head">
            <div>
              <span className="eyebrow">LEARNER COVERAGE</span>
              <h3>Tracked concepts</h3>
            </div>

            <span className="mono">
              {learnerStates.length}
            </span>
          </div>

          <ProgressBar value={masteryPercent} />

          <div className="mini-stats">
            <span><b>{masteredConcepts}</b> mastered</span>
            <span><b>{conceptsNeedingPractice}</b> practice</span>
            <span><b>{learnerStates.length}</b> tracked</span>
          </div>

          <div className="concept-mini">
            {learnerStates
              .slice()
              .sort((a, b) => a.mastery - b.mastery)
              .slice(0, 4)
              .map((state) => (
                <div key={state.concept_id}>
                  <span>Concept {state.concept_id}</span>

                  <ProgressBar
                    value={Math.round(state.mastery * 100)}
                    color={
                      state.mastery < 0.5
                        ? 'warning'
                        : state.mastery >= 0.8
                          ? 'success'
                          : 'primary'
                    }
                  />

                  <b>{Math.round(state.mastery * 100)}%</b>
                </div>
              ))}
          </div>
        </Card>
      </div>

      <div className="three-col">
        <Card>
          <span className="eyebrow">LEARNING SIGNAL</span>

          <h3>
            {recentAttempt
              ? recentAttempt.is_correct
                ? 'Recent attempt was correct'
                : 'Recent attempt needs review'
              : 'No attempts recorded'}
          </h3>

          <p className="muted">
            {recentAttempt
              ? `Question ${recentAttempt.question_id} is the latest recorded assessment attempt.`
              : 'Complete your first assessment to start building a learner model.'}
          </p>

          <div
            className={`signal ${
              recentAttempt?.is_correct ? 'success' : 'warning'
            }`}
          >
            {recentAttempt
              ? recentAttempt.is_correct
                ? 'Positive retrieval signal'
                : 'Review recommended'
              : 'Waiting for learner signal'}
          </div>
        </Card>

        <Card>
          <span className="eyebrow">LEARNER STATE</span>

          <h3>{conceptsNeedingPractice} concepts need practice</h3>

          <p className="muted">
            Concepts below 70% mastery are currently treated as practice candidates on this dashboard.
          </p>

          <ArrowButton
            onClick={() => nav('/app/weak-areas')}
          >
            View weak areas
          </ArrowButton>
        </Card>

        <Card>
          <span className="eyebrow">ASSESSMENT ACTIVITY</span>

          <h3>{totalAttempts} attempts recorded</h3>

          <div className="streak">
            <Trophy size={20} />
            <b>{accuracyPercent}%</b>
            <span>accuracy</span>
          </div>
        </Card>
      </div>
    </>
  )
}

export function Courses() {
  return (
    <>
      <SectionTitle
        eyebrow="LEARNING LIBRARY"
        title="Your courses"
        description="Continue an existing path or explore another learning environment."
      />

      <div className="toolbar">
        <div className="search">
          <Search size={17} />
          <input placeholder="Search courses..." />
        </div>

        <Button variant="secondary">
          <Filter size={16} />
          Filter
        </Button>
      </div>

      <div className="course-grid">
        {[
          'Python Fundamentals',
          'Data Structures & Algorithms',
          'Machine Learning Foundations'
        ].map((c, i) => (
          <Card
            className="course-card"
            key={c}
          >
            <GridReveal
              className="course-thumb"
              src={[
                '/functions.svg',
                '/data-structures.svg',
                '/ml-foundations.svg'
              ][i]}
              alt={c}
              caption="Adaptive course preview"
            />

            <div className="course-icon">
              <BookOpen size={20} />
            </div>

            <span className="eyebrow">
              {i === 0 ? 'IN PROGRESS' : 'AVAILABLE'}
            </span>

            <h3>{c}</h3>

            <p className="muted">
              {i === 0
                ? 'Build core Python fluency through concepts, practice, and adaptive assessment.'
                : 'A structured concept path with prerequisite-aware progression.'}
            </p>

            <ProgressBar
              value={[72, 41, 18][i]}
            />

            <div className="course-meta">
              <span>{[24, 32, 28][i]} concepts</span>
              <span>{[18, 13, 5][i]} mastered</span>
            </div>

            <Link
              className="card-link"
              to="/app/courses/python"
            >
              Open course <ArrowRight size={15} />
            </Link>
          </Card>
        ))}
      </div>
    </>
  )
}


export function CourseOverview() {
  return (
    <>
      <div className="back-link">
        <Link to="/app/courses">
          <ArrowLeft size={15} />
          Courses
        </Link>
      </div>

      <div className="page-heading">
        <SectionTitle
          eyebrow="COURSE OVERVIEW"
          title="Python Fundamentals"
          description="A prerequisite-aware path from core syntax to confident problem solving."
        />

        <div className="course-score">
          <MasteryRing value={72} size={92} />

          <span>
            <b>72%</b>
            <small>overall progress</small>
          </span>
        </div>
      </div>

      <div className="course-gooey">
        <GooeyNav
          items={[
            'Overview',
            'Concepts',
            'Practice'
          ]}
          defaultValue={0}
          activeColor="#6E5BFF"
        />
      </div>

      <Card className="course-hero">
        <div>
          <span className="eyebrow">
            CURRENT FRONTIER
          </span>

          <h2>Functions</h2>

          <p className="muted">
            Your next diagnostic frontier. Prerequisites are complete and additional practice is recommended.
          </p>

          <Button>
            Continue <ArrowRight size={16} />
          </Button>
        </div>

        <div className="frontier-status">
          <span className="status-dot" />
          READY
        </div>
      </Card>

      <div className="concept-list">
        {concepts.map((c, i) => (
          <Card
            className="concept-row"
            key={c.name}
          >
            <div className="concept-state">
              <StatusIcon
                kind={
                  c.status === 'mastered'
                    ? 'success'
                    : c.status === 'attention'
                      ? 'warning'
                      : c.status === 'locked'
                        ? 'locked'
                        : 'info'
                }
              />

              <div>
                <span className="eyebrow">
                  CONCEPT {i + 1}
                </span>

                <h3>{c.name}</h3>
              </div>
            </div>

            <div className="concept-progress">
              <MasteryRing
                value={c.mastery}
                size={54}
              />

              <span>{c.status}</span>
            </div>

            <ArrowRight size={17} />
          </Card>
        ))}
      </div>
    </>
  )
}


export function Concept() {
  const nav = useNavigate()

  const sections = [
    {
      id: 'overview',
      label: 'Overview',
      kind: 'title' as const
    },
    {
      id: 'example',
      label: 'Example',
      kind: 'section' as const
    },
    {
      id: 'practice',
      label: 'Practice',
      kind: 'section' as const
    },
    {
      id: 'summary',
      label: 'Summary',
      kind: 'section' as const
    }
  ]

  return (
    <>
      <div className="back-link">
        <Link to="/app/courses/python">
          <ArrowLeft size={15} />
          Python Fundamentals
        </Link>
      </div>

      <div className="lesson-page">
        <ProximitySidebar
          sections={sections}
          side="right"
        />

        <article className="lesson">
          <div className="lesson-local-nav">
            <BounceSidebar
              items={[
                {
                  label: 'Overview',
                  href: '/app/concepts/functions#overview'
                },
                {
                  label: 'Example',
                  href: '/app/concepts/functions#example'
                },
                {
                  label: 'Practice',
                  href: '/app/assessment'
                },
                {
                  label: 'Summary',
                  href: '/app/concepts/functions#summary'
                }
              ]}
              dotColor="#6E5BFF"
            />
          </div>

          <span className="eyebrow">
            CONCEPT • FUNCTIONS
          </span>

          <h1>Functions in Python</h1>

          <StepPlayer
            steps={[
              {
                label: 'Overview',
                duration: 2600
              },
              {
                label: 'Example',
                duration: 2600
              },
              {
                label: 'Practice',
                duration: 2600
              },
              {
                label: 'Summary',
                duration: 2600
              }
            ]}
            seekable
            size={38}
            className="lesson-player"
          />

          <section id="overview">
            <p className="lead">
              Functions let you package a repeatable computation into a named block of logic. They are one of the most important building blocks for readable programs.
            </p>
          </section>

          <section id="example">
            <h2>Defining a function</h2>

            <p>
              A function is introduced with the <code>def</code> keyword. Parameters receive values from the caller, and <code>return</code> sends a result back.
            </p>

            <pre>
              <code>
                {`def add(a, b):
    return a + b

result = add(2, 3)`}
              </code>
            </pre>

            <h2>
              Parameters and return values
            </h2>

            <p>
              Think of parameters as the inputs to a small machine. A return value is the output. Keeping this boundary clear makes code easier to reason about and test.
            </p>
          </section>

          <section id="practice">
            <div className="callout">
              <Sparkles size={17} />

              <div>
                <b>Try explaining it yourself.</b>

                <span>
                  Before moving on, describe what happens when <code>add(2, 3)</code> runs.
                </span>
              </div>
            </div>
          </section>

          <section id="summary">
            <h2>Summary</h2>

            <p>
              Functions define reusable behavior, accept inputs through parameters, and can return outputs to the caller.
            </p>
          </section>
        </article>

        <aside className="lesson-side">
          <Card>
            <span className="eyebrow">
              YOUR UNDERSTANDING
            </span>

            <div className="side-metric">
              <MasteryRing value={48} />

              <div>
                <b>48%</b>
                <span>mastery</span>
              </div>
            </div>

            <div className="side-row">
              <span>Confidence</span>
              <b>35%</b>
            </div>

            <div className="side-row">
              <span>Revision</span>
              <b>Due today</b>
            </div>

            <Button
              onClick={() => nav('/app/assessment')}
            >
              Practice concept
              <Play size={15} />
            </Button>
          </Card>

          <Card>
            <span className="eyebrow">
              PREREQUISITES
            </span>

            <div className="prereq">
              <StatusIcon kind="success" />
              <span>Variables & Data Types</span>
              <b>92%</b>
            </div>

            <div className="prereq">
              <StatusIcon kind="success" />
              <span>Control Flow</span>
              <b>84%</b>
            </div>
          </Card>
        </aside>
      </div>

      <ScrollProgress
        sections={sections.map(({ id, label }) => ({
          id,
          label
        }))}
      />
    </>
  )
}


/* =========================================================
   REAL BACKEND ASSESSMENT
   ========================================================= */

export function Assessment() {
  const nav = useNavigate()
  const location = useLocation()

  const [question, setQuestion] = useState<Question | null>(null)
  const [selectedAnswer, setSelectedAnswer] = useState('')
  const [confidence, setConfidence] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [startedAt, setStartedAt] = useState<number | null>(null)

  const TEST_USER_ID = 630

  useEffect(() => {
    let mounted = true

    async function loadQuestion() {
      try {
        setLoading(true)
        setError('')

        const navigationState = location.state as
          | { questionId?: number | null }
          | null

        const questionId =
          typeof navigationState?.questionId === 'number'
            ? navigationState.questionId
            : 12

        const data = await getQuestion(questionId)

        if (mounted) {
          setQuestion(data)
          setStartedAt(Date.now())
        }
      } catch (err) {
        if (mounted) {
          setError(
            err instanceof Error
              ? err.message
              : 'Failed to load question.'
          )
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadQuestion()

    return () => {
      mounted = false
    }
  }, [location.state])

  async function handleSubmit() {
    if (!question || !selectedAnswer || confidence === null || submitting) {
      return
    }

    try {
      setSubmitting(true)
      setError('')

      const isCorrect =
        question.correct_answer !== null &&
        question.correct_answer !== undefined &&
        selectedAnswer === question.correct_answer

      const timeTaken = startedAt
        ? Math.max(1, Math.round((Date.now() - startedAt) / 1000))
        : 1

      const response: AttemptResponse = await submitAttempt({
        user_id: TEST_USER_ID,
        question_id: question.id,
        answer: selectedAnswer,
        is_correct: isCorrect,
        time_taken: timeTaken,
        confidence,
      })

      nav('/app/assessment/feedback', {
        state: {
          questionId: question.id,
          answer: selectedAnswer,
          confidence,
          isCorrect,
          timeTaken,
          attemptResponse: response,
        },
      })
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to submit attempt.'
      )
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="feedback-wrap">
        <span className="eyebrow">
          ADAPTIVE ASSESSMENT
        </span>

        <h1>
          Loading question...
        </h1>

        <p className="lead">
          The adaptive engine is preparing your next question.
        </p>
      </div>
    )
  }

  if (error && !question) {
    return (
      <div className="feedback-wrap">
        <span className="eyebrow">
          ASSESSMENT ERROR
        </span>

        <h1>
          Unable to load question.
        </h1>

        <p className="lead">
          {error}
        </p>

        <Button
          onClick={() => window.location.reload()}
        >
          Retry
        </Button>
      </div>
    )
  }

  if (!question) {
    return (
      <div className="feedback-wrap">
        <span className="eyebrow">
          ASSESSMENT
        </span>

        <h1>
          No question available.
        </h1>
      </div>
    )
  }

  const options = question.options
    ? Object.entries(question.options)
    : []

  return (
    <>
      <div className="assessment-top">
        <div>
          <span className="eyebrow">
            PYTHON FUNDAMENTALS
          </span>

          <h1>
            Assessment
          </h1>
        </div>

        <span className="mono">
          QUESTION {question.id}
        </span>
      </div>

      <div className="assessment-layout">
        <Card className="question-card">
          <div className="question-meta">
            <span>
              Question {question.id}
            </span>

            <span>
              Concept {question.concept_id}
            </span>
          </div>

          <h2>
            {question.question_text}
          </h2>

          <div className="options">
            {options.map(([key, text]) => (
              <button
                type="button"
                key={key}
                className={`option ${
                  selectedAnswer === key
                    ? 'selected'
                    : ''
                }`}
                onClick={() => setSelectedAnswer(key)}
                disabled={submitting}
              >
                <span>{key}</span>
                {text}
              </button>
            ))}
          </div>

          <div className="confidence">
            <div>
              <span className="eyebrow">
                CONFIDENCE
              </span>

              <p>
                How confident are you in your answer?
              </p>
            </div>

            <div
              className="confidence-scale"
              style={{
                position: 'relative',
                zIndex: 9999,
                pointerEvents: 'auto',
              }}
            >
              {[1, 2, 3, 4, 5].map((n) => (
                <button
                  type="button"
                  key={n}
                  className={
                    confidence === n
                      ? 'selected'
                      : ''
                  }
                  onPointerDown={(event) => {
                    event.preventDefault()
                    if (!submitting) {
                      setConfidence(n)
                    }
                  }}
                  onClick={() => {
                    if (!submitting) {
                      setConfidence(n)
                    }
                  }}
                  style={{
                    position: 'relative',
                    zIndex: 10000,
                    pointerEvents: 'auto',
                    cursor: submitting
                      ? 'not-allowed'
                      : 'pointer',
                  }}
                >
                  {n}
                </button>
              ))}
            </div>
          </div>

          {error && (
            <p className="lead" style={{ marginTop: '1rem' }}>
              {error}
            </p>
          )}

          <Button
            disabled={
              !selectedAnswer ||
              confidence === null ||
              submitting
            }
            onClick={handleSubmit}
          >
            {submitting ? 'Recording attempt...' : 'Submit answer'}
            {!submitting && <ArrowRight size={16} />}
          </Button>
        </Card>

        <Card className="assessment-rail">
          <span className="eyebrow">
            SESSION SIGNAL
          </span>

          <h3>
            Adaptive assessment
          </h3>

          <p className="muted">
            Questions adjust around your current learner state.
          </p>

          <div className="rail-item">
            <Clock3 size={16} />

            <span>
              Session duration
            </span>
          </div>

          <DurationPicker
            defaultValue={{
              hours: 0,
              minutes: 4
            }}
            onConfirm={() => {}}
          />

          <div className="rail-item">
            <Target size={16} />

            <span>
              Difficulty: {question.difficulty}/5
            </span>
          </div>

          <ProgressBar value={40} />
        </Card>
      </div>
    </>
  )
}


/* =========================================================
   FEEDBACK
   ========================================================= */

export function Feedback() {
  const nav = useNavigate()
  const location = useLocation()

  const state = location.state as
    | {
        questionId?: number
        answer?: string
        confidence?: number
        isCorrect?: boolean
        timeTaken?: number
        attemptResponse?: AttemptResponse
      }
    | null

  const response = state?.attemptResponse

  // The backend returns adaptive fields directly on AttemptResponse.
  const adaptiveResult = response

  const isCorrect =
    state?.isCorrect ??
    response?.is_correct ??
    false

  const mastery =
    typeof adaptiveResult?.mastery === 'number'
      ? adaptiveResult.mastery
      : null

  const confidence =
    typeof adaptiveResult?.confidence === 'number'
      ? adaptiveResult.confidence
      : state?.confidence ?? null

  const revisionNeed =
    typeof adaptiveResult?.revision_need === 'number'
      ? adaptiveResult.revision_need
      : null

  const action =
    typeof adaptiveResult?.action === 'string'
      ? adaptiveResult.action
      : 'PRACTICE_CONCEPT'

  const reason =
    typeof adaptiveResult?.reason === 'string'
      ? adaptiveResult.reason
      : 'Your learner state has been updated by the adaptive engine.'

  const nextQuestionId =
    typeof adaptiveResult?.next_question_id === 'number'
      ? adaptiveResult.next_question_id
      : null

  const actionLabel = action
    .replaceAll('_', ' ')
    .toLowerCase()
    .replace(/\b\w/g, (char: string) => char.toUpperCase())

  return (
    <>
      <div className="feedback-wrap">
        <div className="feedback-icon">
          <CheckCircle2 size={30} />
        </div>

        <span className="eyebrow">
          ATTEMPT RECORDED
        </span>

        <h1>
          {isCorrect ? 'Correct.' : 'Not quite.'}
        </h1>

        <p className="lead">
          Your learner state has been updated and the adaptive engine has selected your next useful action.
        </p>

        <div className="feedback-grid">
          <Metric
            label="Mastery"
            value={
              mastery !== null
                ? `${Math.round(mastery * 100)}%`
                : 'Updated'
            }
            sub="Updated from attempt"
            tone="primary"
          />

          <Metric
            label="Confidence"
            value={
              confidence !== null
                ? `${Math.round(
                    confidence <= 1
                      ? confidence * 100
                      : (confidence / 5) * 100
                  )}%`
                : 'Recorded'
            }
            sub="Learner confidence"
            tone="warning"
          />

          <Metric
            label="Revision need"
            value={
              revisionNeed !== null
                ? revisionNeed.toFixed(2)
                : 'Updated'
            }
            sub={
              revisionNeed !== null
                ? 'Adaptive revision signal'
                : 'Revision state updated'
            }
            tone="success"
          />
        </div>

        <Card className="adaptive-result">
          <div>
            <span className="eyebrow">
              NEXT LEARNING ACTION
            </span>

            <h2>
              {actionLabel}
            </h2>

            <p>
              {reason}
            </p>

            {nextQuestionId !== null && (
              <span className="mono">
                NEXT QUESTION {nextQuestionId}
              </span>
            )}
          </div>

          <Button
            onClick={() =>
              nav('/app/assessment', {
                state: {
                  questionId: nextQuestionId,
                },
              })
            }
          >
            Next question
            <ArrowRight size={16} />
          </Button>
        </Card>
      </div>
    </>
  )
}


export function Recommendations() {
  const nav = useNavigate()

  return (
    <>
      <SectionTitle
        eyebrow="ADAPTIVE QUEUE"
        title="Recommendations"
        description="Actions selected from your current mastery, confidence, revision state, misconceptions, and prerequisites."
      />

      <div className="recommend-cards">
        {recommendations.map((r) => (
          <Card
            key={r.title}
            className="big-recommend"
          >
            <div className="recommend-top">
              <RecommendationIcon
                kind={r.icon}
              />

              <span className="action-code">
                {r.action}
              </span>
            </div>

            <h2>
              {r.title}
            </h2>

            <p className="muted">
              {r.reason}
            </p>

            <div className="recommend-metrics">
              <span>
                <small>Mastery</small>
                <b>{r.mastery}%</b>
              </span>

              <span>
                <small>Confidence</small>
                <b>{r.confidence}%</b>
              </span>

              <span>
                <small>Priority</small>
                <b>
                  {r.action === 'PRACTICE_CONCEPT'
                    ? '0.546'
                    : '0.42'}
                </b>
              </span>
            </div>

            <Button
              onClick={() =>
                nav('/app/assessment')
              }
            >
              Start action
              <ArrowRight size={16} />
            </Button>
          </Card>
        ))}
      </div>
    </>
  )
}


export function WeakAreas() {
  return (
    <>
      <SectionTitle
        eyebrow="DIAGNOSTIC VIEW"
        title="Weak areas"
        description="Concepts where mastery, confidence, errors, misconception signals, or prerequisites need attention."
      />

      <div className="weak-grid">
        {concepts
          .filter((c) => c.mastery < 70)
          .map((c, i) => (
            <Card
              key={c.name}
              className="weak-card"
            >
              <div className="weak-head">
                <MasteryRing
                  value={c.mastery}
                  size={70}
                />

                <div>
                  <span className="eyebrow">
                    {i === 0
                      ? 'MISCONCEPTION SIGNAL'
                      : 'LOW MASTERY'}
                  </span>

                  <h3>{c.name}</h3>
                </div>
              </div>

              <div className="signal warning">
                {i === 0
                  ? 'Frequent errors detected'
                  : 'Additional practice recommended'}
              </div>

              <div className="side-row">
                <span>Mastery</span>
                <b>{c.mastery}%</b>
              </div>

              <div className="side-row">
                <span>Confidence</span>
                <b>
                  {i === 0 ? '28%' : '35%'}
                </b>
              </div>

              <Button variant="secondary">
                Open concept
                <ArrowRight size={15} />
              </Button>
            </Card>
          ))}
      </div>
    </>
  )
}


export function Progress() {
  return (
    <>
      <SectionTitle
        eyebrow="LEARNING ANALYTICS"
        title="Progress"
        description="A calm view of how your knowledge is developing across the course."
      />

      <div className="progress-overview">
        <Card className="progress-big">
          <div>
            <span className="eyebrow">
              OVERALL MASTERY
            </span>

            <h2>74%</h2>

            <p className="muted">
              Across active concepts
            </p>
          </div>

          <MasteryRing
            value={74}
            size={128}
          />
        </Card>

        <Metric
          label="Concepts mastered"
          value="18"
          sub="of 24 active"
        />

        <Metric
          label="Questions answered"
          value="86"
          sub="72% correct"
        />
      </div>

      <Card>
        <div className="card-head">
          <div>
            <span className="eyebrow">
              CONCEPT MASTERY
            </span>

            <h3>
              Python Fundamentals
            </h3>
          </div>

          <span className="mono">
            24 concepts
          </span>
        </div>

        <div className="mastery-table">
          {concepts.map((c) => (
            <div key={c.name}>
              <span>{c.name}</span>

              <ProgressBar
                value={c.mastery}
                color={
                  c.tone === 'warning'
                    ? 'warning'
                    : c.tone === 'success'
                      ? 'success'
                      : 'primary'
                }
              />

              <b>{c.mastery}%</b>
            </div>
          ))}
        </div>
      </Card>
    </>
  )
}


export function Resources() {
  return (
    <>
      <SectionTitle
        eyebrow="KNOWLEDGE LIBRARY"
        title="Resources"
        description="Reference material connected to your active concepts."
      />

      <div className="toolbar">
        <div className="search">
          <Search size={17} />
          <input placeholder="Search resources..." />
        </div>

        <Button variant="secondary">
          <Filter size={16} />
          All types
        </Button>
      </div>

      <div className="saved-resource">
        <div>
          <span className="eyebrow">
            SAVED
          </span>

          <strong>
            Functions — Course Notes
          </strong>
        </div>

        <DeleteButton
          onConfirm={() => {}}
        />
      </div>

      <div className="resource-grid">
        {[
          [
            'Functions — Course Notes',
            'PDF',
            '12 min read',
            FileText
          ],
          [
            'Functions Explained',
            'VIDEO',
            '18 min',
            Video
          ],
          [
            'Practice Worksheet',
            'PDF',
            '8 questions',
            FileText
          ],
          [
            'Python Style Guide',
            'ARTICLE',
            '10 min read',
            BookOpen
          ]
        ].map(
          ([title, type, meta, Icon], i) => (
            <Card
              key={String(title)}
              className="resource-card"
            >
              <GridReveal
                className="resource-thumb"
                src={[
                  '/functions.svg',
                  '/data-structures.svg',
                  '/ml-foundations.svg',
                  '/functions.svg'
                ][i]}
                alt={String(title)}
                caption="Loading resource"
              />

              <div className="resource-icon">
                <Icon size={19} />
              </div>

              <span className="eyebrow">
                {String(type)}
              </span>

              <h3>
                {String(title)}
              </h3>

              <p className="muted">
                {String(meta)}
              </p>

              <ArrowButton>
                Open resource
              </ArrowButton>
            </Card>
          )
        )}
      </div>
    </>
  )
}


export function History() {
  return (
    <>
      <SectionTitle
        eyebrow="LEARNING ACTIVITY"
        title="History"
        description="Your recent learning sessions, assessments, reviews, and tutor interactions."
      />

      <div className="timeline">
        {history.map((day) => (
          <section key={day.date}>
            <div className="timeline-date">
              {day.date}
            </div>

            {day.items.map(
              ([title, meta, tone]) => (
                <Card
                  className="timeline-item"
                  key={title}
                >
                  <StatusIcon
                    kind={
                      tone as
                        | 'success'
                        | 'info'
                    }
                  />

                  <div>
                    <h3>{title}</h3>
                    <span>{meta}</span>
                  </div>

                  <span className="mono">
                    logged
                  </span>
                </Card>
              )
            )}
          </section>
        ))}
      </div>
    </>
  )
}


export function Profile() {
  return (
    <>
      <SectionTitle
        eyebrow="LEARNER PROFILE"
        title="Profile"
        description="Your learner identity and high-level learning statistics."
      />

      <div className="profile-grid">
        <Card className="profile-card">
          <div className="profile-avatar">
            AR
          </div>

          <h2>
            Anoop Reddy
          </h2>

          <p className="muted">
            student@opentutor.dev
          </p>

          <div className="profile-stats">
            <span>
              <b>3</b>
              <small>courses</small>
            </span>

            <span>
              <b>18</b>
              <small>mastered</small>
            </span>

            <span>
              <b>86</b>
              <small>questions</small>
            </span>
          </div>
        </Card>

        <Card>
          <span className="eyebrow">
            LEARNER STATE
          </span>

          <h3>
            Adaptive profile
          </h3>

          <div className="side-row">
            <span>Current focus</span>
            <b>Functions</b>
          </div>

          <div className="side-row">
            <span>Learning streak</span>
            <b>7 days</b>
          </div>

          <div className="side-row">
            <span>Revision due</span>
            <b>3 concepts</b>
          </div>

          <div className="side-row">
            <span>Preferred mode</span>
            <b>Guided practice</b>
          </div>
        </Card>
      </div>
    </>
  )
}


export function Tutor() {
  return (
    <div className="tutor-layout">
      <Card className="chat-card">
        <div className="chat-head">
          <div>
            <span className="eyebrow">
              SOCRATIC TUTOR
            </span>

            <h2>
              Functions
            </h2>
          </div>

          <MatrixOrb
            state="thinking"
            size={58}
            dots={9}
            labels={{
              thinking: 'Thinking'
            }}
            className="tutor-orb"
          />

          <span className="live-label">
            <span className="pulse-dot" />
            LIVE
          </span>
        </div>

        <div className="chat-messages">
          <div className="message tutor">
            <span className="message-label">
              Tutor
            </span>

            <p>
              Let's work through this step by step. What do you think happens when <code>add(2, 3)</code> is called?
            </p>
          </div>

          <div className="message student">
            <span className="message-label">
              You
            </span>

            <p>
              I think it returns 5 because the parameters receive 2 and 3.
            </p>
          </div>

          <div className="message tutor">
            <span className="message-label">
              Tutor
            </span>

            <p>
              Exactly. Now explain why <code>return</code> is different from printing the value.
            </p>
          </div>
        </div>

        <div className="chat-input">
          <input placeholder="Ask a question..." />

          <Button>
            <ArrowRight size={16} />
          </Button>
        </div>
      </Card>

      <aside className="tutor-context">
        <Card>
          <span className="eyebrow">
            LEARNER CONTEXT
          </span>

          <h3>
            Current state
          </h3>

          <div className="context-row">
            <span>Mastery</span>
            <b>48%</b>
          </div>

          <div className="context-row">
            <span>Confidence</span>
            <b>35%</b>
          </div>

          <div className="context-row">
            <span>Revision</span>
            <b>Due today</b>
          </div>
        </Card>

        <Card>
          <span className="eyebrow">
            PREREQUISITES
          </span>

          <div className="prereq">
            <StatusIcon kind="success" />
            <span>Variables</span>
            <b>92%</b>
          </div>

          <div className="prereq">
            <StatusIcon kind="success" />
            <span>Control Flow</span>
            <b>84%</b>
          </div>
        </Card>
      </aside>
    </div>
  )
}