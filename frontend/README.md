# OpenTutor Phase 7 Frontend

React + TypeScript + Vite frontend implementing the Nocturne / OpenTutor adaptive-learning design system.

## Run

```bash
npm install
npm run dev
```

Open the local Vite URL shown in the terminal.

## UI stack

- React + TypeScript + Vite
- React Router
- Lucide React
- Motion
- Flubber
- Radix Slot
- Figma Squircle
- React Use Measure

## Animated components integrated

- FluidOrb — authentication / AI visual
- MatrixOrb — Socratic tutor state
- BounceSidebar — concept navigation
- HookSidebar — application navigation
- StepPlayer — concept progression
- AnimatedCounter — dashboard metrics
- GridReveal — course/resource previews
- GooeyNav — course overview mode navigation
- ProximitySidebar — concept section minimap
- ScrollProgress — concept reading progress
- DurationPicker — assessment session duration
- TaskList — dashboard revision queue
- NotificationBell — top-bar notifications
- DeleteButton — saved-resource removal interaction

The animation layer respects reduced-motion preferences where supported and keeps the core OpenTutor visual system: deep navy canvas, purple primary accent, restrained depth, and non-gamified learning UX.

Current data is mock data. Backend/API integration remains the next major step.
