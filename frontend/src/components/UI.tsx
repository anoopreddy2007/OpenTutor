import {
  ArrowRight,
  Check,
  LockKeyhole,
  Sparkles,
  Target,
  RefreshCw,
  GitBranch,
  AlertTriangle,
  Info,
} from 'lucide-react'
import type { ReactNode } from 'react'
import AnimatedCounter from './animated/AnimatedCounter'

export function Button({
  children,
  variant = 'primary',
  onClick,
  disabled = false,
}: {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'ghost'
  onClick?: () => void
  disabled?: boolean
}) {
  return (
    <button
      className={`btn ${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}

export function Card({
  children,
  className = '',
}: {
  children: ReactNode
  className?: string
}) {
  return (
    <div className={`card ${className}`}>
      {children}
    </div>
  )
}

export function SectionTitle({
  eyebrow,
  title,
  description,
}: {
  eyebrow?: string
  title: string
  description?: string
}) {
  return (
    <div className="section-title">
      {eyebrow && <div className="eyebrow">{eyebrow}</div>}
      <h1>{title}</h1>
      {description && <p>{description}</p>}
    </div>
  )
}

export function ProgressBar({
  value,
  color = 'primary',
}: {
  value: number
  color?: 'primary' | 'success' | 'warning'
}) {
  return (
    <div className="progress">
      <div
        className={`progress-fill ${color}`}
        style={{ width: `${value}%` }}
      />
    </div>
  )
}

export function Metric({
  label,
  value,
  sub,
  tone = 'default',
}: {
  label: string
  value: string | number
  sub?: string
  tone?: string
}) {
  return (
    <Card className="metric">
      <span className="metric-label">{label}</span>

      <strong className={`metric-value ${tone}`}>
        {typeof value === 'number' ? (
          <AnimatedCounter value={value} />
        ) : (
          value
        )}
      </strong>

      {sub && <span className="metric-sub">{sub}</span>}
    </Card>
  )
}

export function MasteryRing({
  value,
  size = 76,
}: {
  value: number
  size?: number
}) {
  return (
    <div
      className="mastery-ring"
      style={{
        width: size,
        height: size,
        background: `conic-gradient(
          #6E5BFF 0 ${value}%,
          #34D399 ${value}% ${Math.min(value + 8, 100)}%,
          rgba(255,255,255,.05) ${Math.min(value + 8, 100)}% 100%
        )`,
      }}
    >
      <div>
        <b>{value}%</b>
      </div>
    </div>
  )
}

export function StatusIcon({
  kind,
}: {
  kind: 'success' | 'warning' | 'error' | 'info' | 'locked'
}) {
  const C =
    kind === 'success'
      ? Check
      : kind === 'warning'
        ? AlertTriangle
        : kind === 'info'
          ? Info
          : kind === 'locked'
            ? LockKeyhole
            : Target

  return (
    <span className={`status-icon ${kind}`}>
      <C size={15} />
    </span>
  )
}

export function RecommendationIcon({
  kind,
}: {
  kind: string
}) {
  const C =
    kind === 'git'
      ? GitBranch
      : kind === 'refresh'
        ? RefreshCw
        : kind === 'target'
          ? Target
          : Sparkles

  return (
    <span className="recommendation-icon">
      <C size={19} />
    </span>
  )
}

export function ArrowButton({
  children,
  onClick,
}: {
  children: ReactNode
  onClick?: () => void
}) {
  return (
    <button className="arrow-btn" onClick={onClick}>
      {children}
      <ArrowRight size={16} />
    </button>
  )
}