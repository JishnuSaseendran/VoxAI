import { API_BASE_URL } from '../stores/config.js';
import {
  currentStep,
  currentAgent,
  answer,
  question,
  error,
  PROCESSING_STEPS,
  setProcessingStep
} from '../stores/assistant.js';
import { token } from '../stores/auth.js';
import {
  currentSessionId,
  addSession,
  addMessagePair,
  updateSessionInList
} from '../stores/chat.js';
import { get } from 'svelte/store';

// Get auth headers
function getAuthHeaders() {
  const currentToken = get(token);
  if (currentToken) {
    return { 'Authorization': `Bearer ${currentToken}` };
  }
  return {};
}

// Simulate processing steps with delays for visual feedback
async function simulateStep(step, delay = 500) {
  currentStep.set(step);
  await new Promise(resolve => setTimeout(resolve, delay));
}

// ============== Auth API ==============

export async function signup(email, username, password) {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, username, password })
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Signup failed');
  }

  return response.json();
}

export async function login(email, password) {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Login failed');
  }

  return response.json();
}

export async function getMe() {
  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    throw new Error('Not authenticated');
  }

  return response.json();
}

// ============== Sessions API ==============

export async function fetchSessions() {
  const response = await fetch(`${API_BASE_URL}/api/sessions`, {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to fetch sessions');
  }

  return response.json();
}

export async function fetchSession(sessionId) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to fetch session');
  }

  return response.json();
}

export async function createSession(title = 'New Chat') {
  const response = await fetch(`${API_BASE_URL}/api/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({ title })
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to create session');
  }

  return response.json();
}

export async function updateSession(sessionId, title) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders()
    },
    body: JSON.stringify({ title })
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to update session');
  }

  return response.json();
}

export async function deleteSession(sessionId) {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });

  if (!response.ok) {
    const err = await response.json();
    throw new Error(err.detail || 'Failed to delete session');
  }

  return response.json();
}

// ============== Chat API ==============

export async function askText(queryText) {
  try {
    error.set(null);
    question.set(queryText);

    // Step 1: Routing
    await simulateStep(PROCESSING_STEPS.ROUTING, 300);

    // Build request body
    const body = { question: queryText };
    const sessionId = get(currentSessionId);
    if (sessionId) {
      body.session_id = sessionId;
    }

    // Make API call with optional auth
    const response = await fetch(`${API_BASE_URL}/api/ask/text/detailed`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders()
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Failed to get response');
    }

    const data = await response.json();

    // Step 2: Show agent processing
    setProcessingStep(PROCESSING_STEPS.PROCESSING, data.agent_used);
    await new Promise(resolve => setTimeout(resolve, 400));

    // Step 3: Generating
    await simulateStep(PROCESSING_STEPS.GENERATING, 300);

    // Step 4: Complete
    currentAgent.set(data.agent_used || 'general');
    answer.set(data.answer);
    currentStep.set(PROCESSING_STEPS.COMPLETE);

    // Handle session updates if authenticated
    if (data.session_id) {
      // If this is a new session, add it to the list
      if (!sessionId && data.session_id) {
        const title = data.session_title || queryText.substring(0, 50) + (queryText.length > 50 ? '...' : '');
        addSession({
          id: data.session_id,
          title: title,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        });
        currentSessionId.set(data.session_id);
      }

      // Add messages to current session view
      addMessagePair(queryText, data.answer, {
        message_id: data.message_id,
        query_type: data.query_type,
        agent_used: data.agent_used,
        plan: data.plan
      });

      // Update session in sidebar (move to top)
      updateSessionInList(data.session_id, {
        updated_at: new Date().toISOString()
      });
    }

    return data;
  } catch (err) {
    currentStep.set(PROCESSING_STEPS.ERROR);
    error.set(err.message);
    throw err;
  }
}

export async function askVoice(audioBlob, extension = '.webm') {
  try {
    error.set(null);

    // Step 1: Transcribing
    await simulateStep(PROCESSING_STEPS.TRANSCRIBING, 300);

    const formData = new FormData();
    formData.append('audio', audioBlob, `recording${extension}`);

    // Add session_id if available
    const sessionId = get(currentSessionId);
    if (sessionId) {
      formData.append('session_id', sessionId);
    }

    const response = await fetch(`${API_BASE_URL}/api/ask/voice/detailed`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Failed to process audio');
    }

    const data = await response.json();
    question.set(data.question);

    // Step 2: Routing
    await simulateStep(PROCESSING_STEPS.ROUTING, 300);

    // Step 3: Show agent processing
    setProcessingStep(PROCESSING_STEPS.PROCESSING, data.agent_used);
    await new Promise(resolve => setTimeout(resolve, 400));

    // Step 4: Generating
    await simulateStep(PROCESSING_STEPS.GENERATING, 300);

    // Step 5: Complete
    currentAgent.set(data.agent_used || 'general');
    answer.set(data.answer);
    currentStep.set(PROCESSING_STEPS.COMPLETE);

    // Handle session updates if authenticated
    if (data.session_id) {
      if (!sessionId && data.session_id) {
        const title = data.session_title || data.question.substring(0, 50) + (data.question.length > 50 ? '...' : '');
        addSession({
          id: data.session_id,
          title: title,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        });
        currentSessionId.set(data.session_id);
      }

      addMessagePair(data.question, data.answer, {
        message_id: data.message_id,
        query_type: data.query_type,
        agent_used: data.agent_used,
        plan: data.plan
      });

      updateSessionInList(data.session_id, {
        updated_at: new Date().toISOString()
      });
    }

    return data;
  } catch (err) {
    currentStep.set(PROCESSING_STEPS.ERROR);
    error.set(err.message);
    throw err;
  }
}

export async function textToSpeech(text) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: text })
    });

    if (!response.ok) {
      throw new Error('Failed to generate speech');
    }

    const audioBlob = await response.blob();
    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);
    audio.play();

    return audio;
  } catch (err) {
    error.set('Failed to play audio: ' + err.message);
    throw err;
  }
}
