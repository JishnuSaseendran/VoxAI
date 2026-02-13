import { writable, get } from 'svelte/store';

// Chat sessions list
export const sessions = writable([]);

// Current active session
export const currentSessionId = writable(null);

// Messages for current session
export const messages = writable([]);

// Loading state
export const isLoadingSessions = writable(false);
export const isLoadingMessages = writable(false);

// Set sessions list
export function setSessions(sessionsList) {
  sessions.set(sessionsList);
}

// Add a new session to the list
export function addSession(session) {
  sessions.update(list => [session, ...list]);
}

// Remove a session from the list
export function removeSession(sessionId) {
  sessions.update(list => list.filter(s => s.id !== sessionId));

  // If it's the current session, clear it
  if (get(currentSessionId) === sessionId) {
    currentSessionId.set(null);
    messages.set([]);
  }
}

// Update session in list (e.g., after title change)
export function updateSessionInList(sessionId, updates) {
  sessions.update(list =>
    list.map(s => s.id === sessionId ? { ...s, ...updates } : s)
  );
}

// Set current session and its messages
export function setCurrentSession(sessionId, sessionMessages = []) {
  currentSessionId.set(sessionId);
  messages.set(sessionMessages);
}

// Clear current session (for new chat)
export function clearCurrentSession() {
  currentSessionId.set(null);
  messages.set([]);
}

// Add a message to current session
export function addMessage(message) {
  messages.update(list => [...list, message]);
}

// Add user and assistant messages together
export function addMessagePair(userContent, assistantContent, metadata = {}) {
  const userMessage = {
    id: `temp-user-${Date.now()}`,
    role: 'user',
    content: userContent,
    created_at: new Date().toISOString()
  };

  const assistantMessage = {
    id: metadata.message_id || `temp-assistant-${Date.now()}`,
    role: 'assistant',
    content: assistantContent,
    query_type: metadata.query_type,
    agent_used: metadata.agent_used,
    plan: metadata.plan,
    created_at: new Date().toISOString()
  };

  messages.update(list => [...list, userMessage, assistantMessage]);
}

// Clear all chat state (on logout)
export function clearChatState() {
  sessions.set([]);
  currentSessionId.set(null);
  messages.set([]);
}
