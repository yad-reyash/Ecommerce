# E-commerce Product Showcase - Copilot Instructions

## Project Overview
A React-based e-commerce product showcase for athletic footwear, featuring immersive video introductions, 3D product visualization, and GSAP-powered scroll animations. Built with Vite, React 19, Tailwind CSS v4, and Zustand for state management.

## Architecture & Key Components

### Application Flow
1. **FullscreenIntro** (`src/Components/FullScreenVideoIntro.jsx`) - Auto-plays 25s intro video on first load
2. **Main sections** render after intro: NavBar → Hero → ProductViewer → Showcase → Performance
3. State managed via Zustand store (`src/store/index.js`) for product viewer color, scale, texture

### Component Structure
- **Monolithic components**: Each component is self-contained in `src/Components/` with inline styles via Tailwind
- **No routing**: Single-page application with scroll-based navigation
- **Constants-driven**: UI data lives in `src/constants/index.js` (nav links, performance images, feature data)

## Critical Patterns

### Video Handling
Videos are core to UX. All videos use:
```jsx
videoRef.current.muted = true;
videoRef.current.loop = true;
videoRef.current.playsInline = true;
```
Example: `src/Components/Hero.jsx` plays at 2x speed (`playbackRate = 2`)

### GSAP ScrollTrigger Setup
GSAP registered globally in `App.jsx`:
```jsx
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);
```
Expected for scroll-based animations in Showcase/Performance sections (implementations pending).

### Styling Convention
**Tailwind CSS v4** with custom theme in `src/index.css`:
- Custom fonts: `Regular`, `Medium`, `SemiBold`, `Bold` from `/public/fonts/`
- Custom utilities: `flex-center`, `flex-between`, `col-center`, `abs-center`
- Theme tokens: `--color-primary`, `--color-dark-100`, `--color-dark-200`
- Component styles use `@layer components` for section-specific CSS (header, #hero, #product-viewer, etc.)

### Zustand State Pattern
Store in `src/store/index.js` follows convention:
```jsx
const useStore = create((set) => ({
    value: defaultValue,
    setValue: (value) => set({ value }),
    reset: () => set({ /* defaults */ }),
}))
```

## Development Workflow

### Commands
- **Dev server**: `npm run dev` (Vite HMR on http://localhost:5173)
- **Build**: `npm run build` (outputs to `dist/`)
- **Lint**: `npm run lint` (ESLint flat config in `eslint.config.js`)
- **Preview**: `npm run preview` (test production build)

### Asset Management
- **Videos**: `/public/videos/` (hero.mp4, egeon-concept-shoe-3d-animation-1080-publer.io.mp4)
- **Fonts**: `/public/fonts/` (9 font weights referenced in index.css)
- **Icons**: `/public/` (logo.svg, cart.svg, search.svg)
- **Images**: `/public/images/` (Nike.png, d2.avif)

## Project-Specific Conventions

### Component Naming
- PascalCase for components (e.g., `FullScreenVideoIntro.jsx`, `ProductViewer.jsx`)
- Export default with function declarations
- Typo in Performance.jsx: function named `Perfomance` (imported as `Performance`)

### Incomplete Features
Several components are stubs awaiting implementation:
- `ProductViewer.jsx` - Empty (should render 3D shoe model with color/size controls)
- `Showcase.jsx` - Empty (section defined in CSS with video mask animations)
- `Performance.jsx` - Basic placeholder (CSS defines image positioning for `performanceImgPositions`)
- `PhotoSearchModal.jsx` - Empty component

### Constants Usage
Always import from `src/constants/index.js` for:
- `navLinks` - Navigation menu items
- `noChangeParts` - Object IDs for 3D model (likely for ProductViewer)
- `performanceImages`, `performanceImgPositions` - Performance section layout
- `features`, `featureSequence` - For future Features component
- `footerLinks` - For future Footer component

### ESLint Rules
Custom rule in `eslint.config.js`:
```js
'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }]
```
Allows unused capitalized constants (common for React components in progress).

## Integration Points

### No External APIs
Currently no backend integration. Future considerations:
- Product data fetching (replace constants)
- Cart functionality (buttons exist but no handlers)
- Search implementation (modal stub exists)

### 3D/Animation Libraries
- `@gsap/react` package installed (imports as `gsap` for scroll animations)
- GSAP ScrollTrigger registered globally in App.jsx
- Note: No Three.js/React Three Fiber despite 3D references in constants (ProductViewer 3D implementation pending)

## Common Gotchas

1. **README.md merge conflict**: File shows merge conflict markers from template merge
2. **Intro duration**: FullscreenIntro default param is 100ms, but App.jsx passes 25000ms
3. **Video paths**: All videos referenced with absolute paths from `/public` (e.g., `/videos/hero.mp4`)
4. **Tailwind v4**: Uses new `@theme` directive in CSS instead of `tailwind.config.cjs` theme extension
5. **Unused parcel dependency**: `package.json` includes Parcel but project uses Vite

## When Adding Features

- Place constants in `src/constants/index.js` for reusability
- Follow video pattern: muted, loop, playsInline for all video elements
- Use custom Tailwind utilities (`flex-center`, `col-center`) for layouts
- Define component-specific styles in `src/index.css` under `@layer components`
- Leverage GSAP ScrollTrigger for scroll-based animations (already registered)
