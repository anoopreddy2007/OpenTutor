import React, { useEffect, useState } from "react";
import {
  AnimatePresence,
  motion,
  useReducedMotion,
  useScroll,
  useSpring,
} from "motion/react";
import { cn } from "../../lib/utils";

export type ScrollProgressSection = {
  id: string;
  label: string;
};

export default function ScrollProgress({
  sections = [],
  className,
  offset = 120,
}: {
  sections?: ScrollProgressSection[];
  className?: string;
  offset?: number;
}) {
  const reduce = useReducedMotion();

  const { scrollYProgress } = useScroll();

  const progress = useSpring(scrollYProgress, {
    stiffness: 120,
    damping: 30,
    mass: 0.3,
  });

  const [active, setActive] = useState(sections[0]?.id);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const update = () => {
      const anchor = window.innerHeight * 0.25 + offset;

      const found = [...sections]
        .reverse()
        .find(
          (section) =>
            (
              document
                .getElementById(section.id)
                ?.getBoundingClientRect().top ?? Infinity
            ) <= anchor
        );

      setActive(found?.id ?? sections[0]?.id);
    };

    update();

    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);

    return () => {
      window.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, [sections, offset]);

  const label = sections.find((section) => section.id === active)?.label;

  return (
    <div className={cn("scroll-progress", className)}>
      <motion.div
        className="scroll-progress-surface"
        animate={{
          width: open
            ? Math.max(190, (label?.length ?? 8) * 7 + 58)
            : 190,
          height: open ? 180 : 38,
          borderRadius: open ? 18 : 19,
        }}
        transition={
          reduce
            ? { duration: 0 }
            : {
                type: "spring",
                bounce: 0.16,
                duration: 0.5,
              }
        }
      >
        <AnimatePresence initial={false} mode="popLayout">
          {open ? (
            <motion.div
              key="list"
              className="scroll-progress-list"
              initial={{
                opacity: 0,
                filter: "blur(4px)",
              }}
              animate={{
                opacity: 1,
                filter: "blur(0)",
              }}
              exit={{
                opacity: 0,
                filter: "blur(4px)",
              }}
            >
              <div className="scroll-progress-items">
                {sections.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => {
                      document
                        .getElementById(section.id)
                        ?.scrollIntoView({
                          behavior: reduce ? "auto" : "smooth",
                        });

                      setActive(section.id);
                      setOpen(false);
                    }}
                    className={cn(section.id === active && "active")}
                  >
                    {section.label}
                  </button>
                ))}
              </div>
            </motion.div>
          ) : (
            <motion.button
              key="pill"
              className="scroll-progress-pill"
              onClick={() => setOpen(true)}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <svg viewBox="0 0 24 24">
                <circle
                  cx="12"
                  cy="12"
                  r="9"
                  className="track"
                />

                <motion.circle
                  cx="12"
                  cy="12"
                  r="9"
                  className="progress"
                  style={{ pathLength: progress }}
                />
              </svg>

              <span>{label}</span>
            </motion.button>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  );
}