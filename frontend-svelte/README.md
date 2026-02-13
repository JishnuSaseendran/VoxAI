# Voice Assistant Frontend (Svelte)

A modern Svelte-based frontend for the Voice Assistant multi-agent AI system with real-time status updates.

## Features

- **Text Input** - Type questions directly
- **Voice Recording** - Click to record voice queries
- **Live Status** - Real-time processing status updates
- **Agent Display** - Shows which AI agent handled your query
- **Text-to-Speech** - Listen to responses with stop control
- **Responsive Design** - Works on desktop and mobile

## Project Structure

```
frontend-svelte/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── StatusIndicator.svelte   # Live processing status
│   │   │   ├── AgentBadge.svelte        # Agent type badge
│   │   │   ├── VoiceButton.svelte       # Voice recording button
│   │   │   ├── ResponseCard.svelte      # Question & answer display
│   │   │   └── AgentsList.svelte        # Available agents list
│   │   ├── stores/
│   │   │   ├── assistant.js             # State management
│   │   │   └── config.js                # API configuration
│   │   └── services/
│   │       └── api.js                   # API calls
│   ├── App.svelte                       # Main application
│   └── main.js                          # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Live Status Updates

The interface shows real-time processing status:

| Status | Description |
|--------|-------------|
| 🎤 Recording audio... | Voice input being captured |
| 📝 Transcribing speech... | Converting audio to text |
| 🔀 Router analyzing query... | Determining which agent to use |
| ⚙️ [Agent] processing... | Specialized agent working |
| 💭 Generating response... | Creating the final answer |
| ✅ Complete! | Response ready |

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend server running on port 8000

### Installation

```bash
cd frontend-svelte
npm install
```

### Development

```bash
npm run dev
```

Opens at `http://localhost:3000`

### Production Build

```bash
npm run build
npm run preview
```

## Configuration

### API URL

Edit `src/lib/stores/config.js`:

```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

### Changing Port

Edit `vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 3000  // Change this
  }
})
```

## Components

### StatusIndicator
Displays the current processing step with animated progress bar.

### VoiceButton
Handles microphone access and audio recording. Supports multiple audio formats (webm, ogg, mp4).

### ResponseCard
Shows the question, answer, and which agent handled the query. Includes play and stop buttons for text-to-speech control.

### AgentsList
Expandable list showing all available AI agents and their capabilities.

### AgentBadge
Colored badge displaying the agent type with icon.

## State Management

Uses Svelte stores for reactive state:

```javascript
import { currentStep, answer, question } from './lib/stores/assistant.js';

// Access in components
$currentStep  // Current processing status
$answer       // AI response
$question     // User's question
$currentAgent // Which agent responded
$error        // Error message if any
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 14+
- Edge 80+

Requires:
- MediaRecorder API (for voice recording)
- getUserMedia API (for microphone access)

## Troubleshooting

### Microphone not working

1. Check browser permissions
2. Ensure HTTPS or localhost (required for microphone)
3. Try a different browser

### API connection failed

1. Verify backend is running on port 8000
2. Check CORS settings in backend
3. Verify `API_BASE_URL` in config.js

### Audio not playing

1. Check browser autoplay policies
2. Ensure speakers/headphones connected
3. Try clicking play button again

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
