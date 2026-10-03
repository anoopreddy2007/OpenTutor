import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  animate,
  motion,
  useMotionValue,
  useReducedMotion,
  useTransform,
} from "motion/react";
import { combine, separate, type Interpolator } from "flubber";
import { cn } from "../../lib/utils";

const PLAY = "M9.8 7 L17.7 12 L9.8 17 Z";
const L = "M8.4 5.9 L10.4 5.9 L10.4 18.1 L8.4 18.1 Z";
const R = "M13.6 5.9 L15.6 5.9 L15.6 18.1 L13.6 18.1 Z";

const REPLAY =
  "M17.44 6.56 A7.7 7.7 0 1 1 10.66 4.42 L10.32 2.45 L14.86 4.59 L11.32 8.16 L10.91 5.8 A6.3 6.3 0 1 0 16.45 7.55 Z";

const rest = {
  play: PLAY,
  pause: `${L} ${R}`,
  replay: REPLAY,
};

const morph = (from: string): Interpolator => {
  if (from === "play") {
    return separate(PLAY, [L, R], {
      maxSegmentLength: 0.8,
      single: true,
    });
  }

  return combine([L, R], PLAY, {
    maxSegmentLength: 0.8,
    single: true,
  });
};

function Icon({
  state,
  size,
  reduced,
}: {
  state: "play" | "pause" | "replay";
  size: number;
  reduced: boolean;
}) {
  const shape = useMotionValue(rest[state]);
  const opacity = useMotionValue(1);
  const prev = useRef(state);

  useEffect(() => {
    if (prev.current === state) return;

    const from = prev.current;
    prev.current = state;

    shape.set(rest[state]);

    if (reduced) return;

    if (
      (from === "play" && state === "pause") ||
      (from === "pause" && state === "play")
    ) {
      const m = morph(from);

      const c = animate(0, 1, {
        type: "spring",
        duration: 0.32,
        bounce: 0.22,
        onUpdate: (t) => {
          shape.set(m(Math.max(0, Math.min(1, t))));
        },
      });

      return () => c.stop();
    }

    const c = animate(opacity, 1, {
      duration: 0.26,
    });

    return () => c.stop();
  }, [state, reduced, shape, opacity]);

  return (
    <svg
      viewBox="0 0 24 24"
      width={size}
      height={size}
      aria-hidden="true"
    >
      <motion.path
        d={shape}
        fill="currentColor"
        opacity={opacity}
      />
    </svg>
  );
}

export type StepPlayerStep = {
  duration?: number;
  label?: string;
};

type StepPlayerProps = React.ComponentProps<"div"> & {
  steps?: number | StepPlayerStep[];
  value?: number;
  defaultValue?: number;
  onValueChange?: (value: number) => void;
  playing?: boolean;
  defaultPlaying?: boolean;
  onPlayingChange?: (value: boolean) => void;
  duration?: number;
  loop?: boolean;
  onComplete?: () => void;
  size?: number;
  showControl?: boolean;
  controlPosition?: "left" | "right";
  seekable?: boolean;
};

export default function StepPlayer({
  steps = 4,
  value,
  defaultValue = 0,
  onValueChange,
  playing,
  defaultPlaying = false,
  onPlayingChange,
  duration = 4000,
  loop = false,
  onComplete,
  size = 42,
  showControl = true,
  controlPosition = "right",
  seekable = false,
  className,
  ...props
}: StepPlayerProps) {
  const items = useMemo<StepPlayerStep[]>(
    () =>
      typeof steps === "number"
        ? Array.from(
            {
              length: Math.max(1, steps),
            },
            () => ({}) as StepPlayerStep
          )
        : steps,
    [steps]
  );

  const count = items.length;

  const [idx, setIdx] = useState(
    Math.min(defaultValue, Math.max(0, count - 1))
  );

  const [play, setPlay] = useState(defaultPlaying);
  const [finished, setFinished] = useState(false);

  const controlled = value !== undefined;
  const playingControlled = playing !== undefined;

  const index = Math.min(
    controlled ? value! : idx,
    Math.max(0, count - 1)
  );

  const isPlaying = playingControlled ? playing! : play;

  const reduced = useReducedMotion() ?? false;

  const progress = useMotionValue(0);

  const fill = useTransform(
    progress,
    (p) => `${p * 100}%`
  );

  const complete = useRef(onComplete);

  useEffect(() => {
    complete.current = onComplete;
  }, [onComplete]);

  const commitIndex = useCallback(
    (nextIndex: number) => {
      progress.set(0);
      setFinished(false);

      if (!controlled) {
        setIdx(nextIndex);
      }

      onValueChange?.(nextIndex);
    },
    [controlled, onValueChange, progress]
  );

  const commitPlay = useCallback(
    (nextPlaying: boolean) => {
      if (!playingControlled) {
        setPlay(nextPlaying);
      }

      onPlayingChange?.(nextPlaying);
    },
    [playingControlled, onPlayingChange]
  );

  const stepDuration = items[index]?.duration ?? duration;

  useEffect(() => {
    if (!isPlaying || stepDuration <= 0) {
      return;
    }

    let frame = 0;

    const start =
      performance.now() -
      progress.get() * stepDuration;

    const tick = (now: number) => {
      const elapsed = Math.min(
        1,
        (now - start) / stepDuration
      );

      progress.set(elapsed);

      if (elapsed < 1) {
        frame = requestAnimationFrame(tick);
        return;
      }

      if (index < count - 1) {
        commitIndex(index + 1);
        return;
      }

      complete.current?.();

      if (loop) {
        commitIndex(0);
        return;
      }

      setFinished(true);
      commitPlay(false);
    };

    frame = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(frame);
    };
  }, [
    isPlaying,
    index,
    count,
    stepDuration,
    loop,
    commitIndex,
    commitPlay,
    progress,
  ]);

  const control = () => {
    if (finished) {
      commitIndex(0);
      commitPlay(true);
    } else {
      commitPlay(!isPlaying);
    }
  };

  return (
    <div
      className={cn(
        "step-player",
        controlPosition === "right" && "reverse",
        className
      )}
      {...props}
    >
      {showControl && (
        <motion.button
          type="button"
          className="step-control"
          onClick={control}
          aria-label={
            finished
              ? "Replay"
              : isPlaying
                ? "Pause"
                : "Play"
          }
          whileTap={
            reduced
              ? undefined
              : { scale: 0.88 }
          }
        >
          <Icon
            state={
              finished
                ? "replay"
                : isPlaying
                  ? "pause"
                  : "play"
            }
            size={Math.round(size * 0.64)}
            reduced={reduced}
          />
        </motion.button>
      )}

      <div
        className="step-track"
        role="group"
        aria-label={`Step ${index + 1} of ${count}`}
      >
        {items.map((step, i) => {
          const state =
            i === index
              ? "active"
              : i < index
                ? "past"
                : "pending";

          return (
            <motion.div
              key={i}
              className={`step-dot ${state}`}
              animate={{
                width:
                  state === "active"
                    ? Math.max(26, size * 2.8)
                    : Math.max(6, size * 0.16),
              }}
              transition={{
                type: "spring",
                duration: 0.42,
                bounce: 0.14,
              }}
              style={{
                height: Math.max(5, size * 0.16),
              }}
            >
              {state === "active" && (
                <motion.span
                  className="step-fill"
                  style={{
                    width: fill,
                  }}
                />
              )}

              {seekable && (
                <button
                  type="button"
                  aria-label={
                    step.label ?? `Step ${i + 1}`
                  }
                  className="step-hit"
                  onClick={() => {
                    commitIndex(i);
                    commitPlay(true);
                  }}
                />
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}