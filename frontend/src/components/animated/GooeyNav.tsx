import {
  useEffect,
  useState,
  type ComponentProps,
  type CSSProperties,
  type ReactNode,
} from "react";
import { Link, useLocation } from "react-router-dom";
import {
  motion,
  useReducedMotion,
  useSpring,
  useTransform,
} from "motion/react";
import { cn } from "../../lib/utils";

type Item = {
  label: string;
  href?: string;
  icon?: ReactNode;
};

export type GooeyNavItem = string | Item;

const toItem = (x: GooeyNavItem): Item =>
  typeof x === "string" ? { label: x } : x;

const SIZES = {
  sm: {
    label: "gap-1.5 px-3 py-2 text-xs",
    radius: 10,
    separation: 14,
  },
  md: {
    label: "gap-2 px-4 py-2.5 text-sm",
    radius: 12,
    separation: 18,
  },
  lg: {
    label: "gap-2.5 px-5 py-3 text-base",
    radius: 14,
    separation: 22,
  },
} as const;

type GooeyNavProps = {
  items: GooeyNavItem[];
  value?: number;
  defaultValue?: number;
  onChange?: (index: number) => void;
  size?: keyof typeof SIZES;
  activeColor?: string;
  activeLabelColor?: string;
} & Omit<ComponentProps<"nav">, "onChange">;

export default function GooeyNav({
  items,
  value,
  defaultValue = 0,
  onChange,
  size = "md",
  activeColor = "#6E5BFF",
  activeLabelColor = "#fff",
  className,
  ...props
}: GooeyNavProps) {
  const { pathname } = useLocation();

  const reduced = useReducedMotion() ?? false;

  const route = items.findIndex(
    (item) => toItem(item).href === pathname
  );

  const [internal, setInternal] = useState(
    route === -1 ? defaultValue : route
  );

  const active = value ?? (route === -1 ? internal : route);

  const span = SIZES[size].separation;
  const radius = SIZES[size].radius;

  return (
    <nav
      className={cn("inline-block", className)}
      {...props}
    >
      <ul className="gooey-nav-list">
        {items.map((raw, index) => {
          const item = toItem(raw);
          const isActive = index === active;

          const segmentStyle = {
            "--gooey-color": isActive
              ? activeColor
              : "transparent",
            "--gooey-radius": `${radius}px`,
            "--gooey-gap": `${span}px`,
          } as CSSProperties;

          return (
            <li
              key={`${index}-${item.label}`}
              className={cn(
                "gooey-segment",
                isActive && "active"
              )}
              style={segmentStyle}
            >
              <GooeyItem
                {...item}
                active={isActive}
                color={activeLabelColor}
                onClick={() => {
                  if (value === undefined) {
                    setInternal(index);
                  }

                  onChange?.(index);
                }}
              />
            </li>
          );
        })}
      </ul>
    </nav>
  );
}

type GooeyItemProps = {
  label: string;
  href?: string;
  icon?: ReactNode;
  active: boolean;
  color: string;
  onClick: () => void;
};

function GooeyItem({
  label,
  href,
  icon,
  active,
  color,
  onClick,
}: GooeyItemProps) {
  const reduced = useReducedMotion() ?? false;

  const scale = useSpring(active ? 1 : 0.98, {
    stiffness: 240,
    damping: 24,
  });

  useEffect(() => {
    scale.set(active ? 1 : 0.98);
  }, [active, scale]);

  const glow = useTransform(
    scale,
    (value) =>
      value > 0.99
        ? "0 8px 28px rgba(110, 91, 255, 0.18)"
        : "none"
  );

  const className = cn(
    "gooey-item",
    active && "active"
  );

  const content = (
    <>
      <span className="gooey-icon">
        {icon}
      </span>
      {label}
    </>
  );

  if (href) {
    return (
      <Link
        to={href}
        className={className}
        onClick={onClick}
        style={{
          color: active ? color : undefined,
          boxShadow: reduced ? undefined : glow.get(),
        }}
      >
        {content}
      </Link>
    );
  }

  return (
    <motion.button
      type="button"
      className={className}
      onClick={onClick}
      animate={{
        scale: active ? 1 : 0.98,
      }}
      transition={
        reduced
          ? { duration: 0 }
          : {
              type: "spring",
              stiffness: 240,
              damping: 24,
            }
      }
      style={{
        color: active ? color : undefined,
      }}
    >
      {content}
    </motion.button>
  );
}