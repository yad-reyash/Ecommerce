# Ecommerce

This is an e-commerce web application built with React and Vite, featuring a modern product showcase with animations.

## Getting Started

### Prerequisites
- Node.js (v16 or higher recommended)
- npm

### Installation

1. Install dependencies:
```bash
npm install
```

### Running the Application

**Important:** Make sure you have run `npm install` before starting the dev server.

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173/`

### Troubleshooting

**Error: "Cannot find package 'vite'"**

If you encounter an error like `Cannot find package 'vite'` or similar module not found errors, it means the dependencies are not installed. Follow these steps:

1. Make sure you're in the correct project directory
2. Delete the `node_modules` folder (if it exists) and `package-lock.json`
3. Run `npm install` again
4. Try running `npm run dev` again

If the issue persists, ensure you have Node.js v16 or higher installed:
```bash
node --version
```

### Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run preview` - Preview the production build
- `npm run lint` - Run ESLint to check code quality

## Technology Stack

- **React** - UI library
- **Vite** - Build tool and dev server
- **GSAP (React integration)** - Animation library
- **Tailwind CSS** - Utility-first CSS framework
