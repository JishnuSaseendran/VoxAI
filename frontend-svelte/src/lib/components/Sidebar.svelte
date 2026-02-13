<script>
  import { user, clearAuth } from '../stores/auth.js';
  import {
    sessions,
    currentSessionId,
    isLoadingSessions,
    setCurrentSession,
    clearCurrentSession,
    removeSession,
    setSessions
  } from '../stores/chat.js';
  import { resetState } from '../stores/assistant.js';
  import { fetchSessions, fetchSession, deleteSession } from '../services/api.js';
  import { onMount, createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let isCollapsed = false;
  let deletingSessionId = null;

  onMount(async () => {
    await loadSessions();
  });

  async function loadSessions() {
    isLoadingSessions.set(true);
    try {
      const data = await fetchSessions();
      setSessions(data);
    } catch (err) {
      console.error('Failed to load sessions:', err);
    } finally {
      isLoadingSessions.set(false);
    }
  }

  async function selectSession(sessionId) {
    if ($currentSessionId === sessionId) return;

    try {
      const session = await fetchSession(sessionId);
      setCurrentSession(session.id, session.messages);
      resetState();
    } catch (err) {
      console.error('Failed to load session:', err);
    }
  }

  function startNewChat() {
    clearCurrentSession();
    resetState();
  }

  async function handleDeleteSession(e, sessionId) {
    e.stopPropagation();
    if (deletingSessionId) return;

    deletingSessionId = sessionId;
    try {
      await deleteSession(sessionId);
      removeSession(sessionId);
    } catch (err) {
      console.error('Failed to delete session:', err);
    } finally {
      deletingSessionId = null;
    }
  }

  function handleLogout() {
    clearAuth();
    dispatch('logout');
  }

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  function formatDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;

    if (diff < 86400000) {
      return 'Today';
    } else if (diff < 172800000) {
      return 'Yesterday';
    } else {
      return date.toLocaleDateString();
    }
  }
</script>

<aside class="sidebar" class:collapsed={isCollapsed}>
  <button class="toggle-btn" on:click={toggleSidebar}>
    {isCollapsed ? '>' : '<'}
  </button>

  {#if !isCollapsed}
    <div class="sidebar-header">
      <button class="new-chat-btn" class:active={!$currentSessionId} on:click={startNewChat}>
        <span class="icon">+</span>
        <span>New Chat</span>
      </button>
    </div>

    <div class="sessions-list">
      {#if $isLoadingSessions}
        <div class="loading-sessions">
          <div class="spinner"></div>
          <span>Loading chats...</span>
        </div>
      {:else if $sessions.length === 0}
        <div class="no-sessions">
          <p>No conversations yet</p>
          <p class="hint">Start a new chat to begin</p>
        </div>
      {:else}
        {#each $sessions as session (session.id)}
          <button
            class="session-item"
            class:active={$currentSessionId === session.id}
            on:click={() => selectSession(session.id)}
          >
            <div class="session-info">
              <span class="session-title">{session.title}</span>
              <span class="session-date">{formatDate(session.updated_at)}</span>
            </div>
            <button
              class="delete-btn"
              on:click={(e) => handleDeleteSession(e, session.id)}
              disabled={deletingSessionId === session.id}
              title="Delete chat"
            >
              {deletingSessionId === session.id ? '...' : '🗑️'}
            </button>
          </button>
        {/each}
      {/if}
    </div>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="avatar">{$user?.username?.charAt(0).toUpperCase() || 'U'}</div>
        <div class="user-details">
          <span class="username">{$user?.username || 'User'}</span>
          <span class="email">{$user?.email || ''}</span>
        </div>
      </div>
      <button class="logout-btn" on:click={handleLogout}>
        Logout
      </button>
    </div>
  {/if}
</aside>

<style>
  .sidebar {
    width: 280px;
    min-width: 280px;
    background: #f8f9fa;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    height: 100vh;
    position: relative;
    transition: all 0.3s ease;
  }

  .sidebar.collapsed {
    width: 50px;
    min-width: 50px;
  }

  .toggle-btn {
    position: absolute;
    right: -12px;
    top: 20px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 1px solid #ddd;
    background: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #666;
    z-index: 10;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .toggle-btn:hover {
    background: #f0f0f0;
  }

  .sidebar-header {
    padding: 16px;
    border-bottom: 1px solid #e0e0e0;
  }

  .new-chat-btn {
    width: 100%;
    padding: 12px 16px;
    border: 1px dashed #ccc;
    border-radius: 10px;
    background: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    font-weight: 600;
    color: #333;
    transition: all 0.2s;
  }

  .new-chat-btn:hover {
    border-color: #667eea;
    color: #667eea;
    background: #f8f8ff;
  }

  .new-chat-btn.active {
    border-style: solid;
    border-color: #667eea;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .new-chat-btn .icon {
    font-size: 18px;
    font-weight: bold;
  }

  .sessions-list {
    flex: 1;
    overflow-y: auto;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .loading-sessions,
  .no-sessions {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    color: #888;
    text-align: center;
  }

  .no-sessions p {
    margin: 0;
  }

  .no-sessions .hint {
    font-size: 12px;
    margin-top: 8px;
  }

  .spinner {
    width: 24px;
    height: 24px;
    border: 2px solid #e0e0e0;
    border-top-color: #667eea;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-bottom: 12px;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .session-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px;
    border: none;
    border-radius: 8px;
    background: transparent;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
    width: 100%;
  }

  .session-item:hover {
    background: #e8e8e8;
  }

  .session-item.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .session-info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .session-title {
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .session-date {
    font-size: 11px;
    opacity: 0.7;
  }

  .delete-btn {
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 6px;
    background: transparent;
    color: inherit;
    cursor: pointer;
    opacity: 0;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    flex-shrink: 0;
  }

  .session-item:hover .delete-btn {
    opacity: 0.7;
  }

  .delete-btn:hover {
    opacity: 1 !important;
    background: rgba(220, 38, 38, 0.1);
    color: #dc2626;
  }

  .session-item.active .delete-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    color: white;
  }

  .delete-btn:disabled {
    opacity: 0.5;
    cursor: wait;
  }

  .sidebar-footer {
    padding: 16px;
    border-top: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
  }

  .user-details {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
  }

  .username {
    font-weight: 600;
    font-size: 14px;
    color: #333;
  }

  .email {
    font-size: 12px;
    color: #888;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .logout-btn {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: white;
    color: #666;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .logout-btn:hover {
    background: #fee;
    border-color: #fcc;
    color: #c00;
  }

  @media (max-width: 768px) {
    .sidebar {
      position: fixed;
      left: 0;
      top: 0;
      z-index: 100;
      transform: translateX(0);
    }

    .sidebar.collapsed {
      transform: translateX(-230px);
    }
  }
</style>
