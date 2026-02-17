# VoxAI Frontend (Svelte)

A modern Svelte-based web frontend for the VoxAI multi-agent AI assistant, featuring authentication, chat history, real-time status updates, and voice input.

## Features

- **User Authentication** - Login/signup modal with JWT token management
- **Chat Sessions** - Create, switch, and delete conversation sessions via sidebar
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
│   │   │   ├── AuthModal.svelte           # Login/signup authentication modal
│   │   │   ├── Sidebar.svelte             # Session list, new chat, navigation
│   │   │   ├── ChatHistory.svelte         # Message history display
│   │   │   ├── ResponseCard.svelte        # Question & answer display with TTS
│   │   │   ├── VoiceButton.svelte         # Voice recording button
│   │   │   ├── StatusIndicator.svelte     # Live processing status
│   │   │   ├── AgentBadge.svelte          # Agent type badge
│   │   │   └── AgentsList.svelte          # Available agents list
│   │   ├── stores/
│   │   │   ├── assistant.js               # Processing state (step, answer, agent)
│   │   │   ├── auth.js                    # Auth state (user, token, login status)
│   │   │   ├── chat.js                    # Chat state (sessions, messages, active session)
│   │   │   └── config.js                  # API base URL configuration
│   │   └── services/
│   │       └── api.js                     # API calls (auth, sessions, queries, TTS)
│   ├── App.svelte                         # Main application
│   └── main.js                            # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## Setup

### Prerequisites

- Node.js 18+
- npm
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

### AuthModal
Login and signup form with email/password fields. Stores JWT token and user info in the auth store.

### Sidebar
Collapsible sidebar with chat session list, new chat button, and logout. Manages session switching and deletion.

### ChatHistory
Renders the message history for the active session, displaying user messages and AI responses with agent badges.

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

Uses Svelte writable stores across four modules:

```javascript
// assistant.js - Processing state
import { currentStep, answer, question, currentAgent, error } from './lib/stores/assistant.js';

// auth.js - Authentication state
import { user, token, isLoggedIn } from './lib/stores/auth.js';

// chat.js - Chat session state
import { sessions, activeSession, messages } from './lib/stores/chat.js';

// config.js - API configuration
import { API_BASE_URL } from './lib/stores/config.js';
```

## Live Status Updates

The interface shows real-time processing status:

| Status | Description |
|--------|-------------|
| Recording audio... | Voice input being captured |
| Transcribing speech... | Converting audio to text |
| Router analyzing query... | Determining which agent to use |
| [Agent] processing... | Specialized agent working |
| Generating response... | Creating the final answer |
| Complete! | Response ready |

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 14+
- Edge 80+

Requires MediaRecorder API and getUserMedia API for voice recording.

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
