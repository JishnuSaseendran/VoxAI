<script>
  import { onMount } from 'svelte';
  import { askText, askVoice } from './lib/services/api.js';
  import {
    currentStep,
    error,
    resetState,
    PROCESSING_STEPS
  } from './lib/stores/assistant.js';
  import { isAuthenticated, initAuth, clearAuth } from './lib/stores/auth.js';
  import { messages, clearChatState, clearCurrentSession } from './lib/stores/chat.js';

  import AuthModal from './lib/components/AuthModal.svelte';
  import Sidebar from './lib/components/Sidebar.svelte';
  import StatusIndicator from './lib/components/StatusIndicator.svelte';
  import VoiceButton from './lib/components/VoiceButton.svelte';
  import ResponseCard from './lib/components/ResponseCard.svelte';
  import AgentsList from './lib/components/AgentsList.svelte';
  import ChatHistory from './lib/components/ChatHistory.svelte';

  let inputText = '';
  let isProcessing = false;
  let showAuth = true;
  let isGuest = false;

  onMount(() => {
    initAuth();
    // If already authenticated, don't show auth modal
    if ($isAuthenticated) {
      showAuth = false;
    }
  });

  $: isProcessing = $currentStep.id !== 'idle' &&
                    $currentStep.id !== 'complete' &&
                    $currentStep.id !== 'error';

  function handleAuthSuccess() {
    showAuth = false;
    isGuest = false;
    // Ensure user starts with a fresh chat window
    clearCurrentSession();
    resetState();
  }

  function handleSkipAuth() {
    showAuth = false;
    isGuest = true;
  }

  function handleLogout() {
    clearAuth();
    clearChatState();
    resetState();
    showAuth = true;
    isGuest = false;
  }

  async function handleTextSubmit() {
    if (!inputText.trim() || isProcessing) return;

    const query = inputText.trim();
    inputText = ''; // Clear input immediately

    try {
      await askText(query);
    } catch (err) {
      // Error is handled in the store
    }
  }

  async function handleVoiceRecorded(event) {
    const { audioBlob, extension } = event.detail;

    try {
      await askVoice(audioBlob, extension);
    } catch (err) {
      // Error is handled in the store
    }
  }

  function handleVoiceError(event) {
    error.set(event.detail.message);
    currentStep.set(PROCESSING_STEPS.ERROR);
  }

  function handleKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleTextSubmit();
    }
  }

  function clearError() {
    resetState();
  }

  function startNewChat() {
    clearCurrentSession();
    resetState();
  }
</script>

{#if showAuth && !$isAuthenticated}
  <AuthModal on:success={handleAuthSuccess} on:skip={handleSkipAuth} />
{:else}
  <div class="app-layout" class:with-sidebar={$isAuthenticated}>
    {#if $isAuthenticated}
      <Sidebar on:logout={handleLogout} />
    {/if}

    <main>
      <div class="container">
        <header>
          <h1>Voice Assistant</h1>
          <p class="subtitle">Powered by Multi-Agent AI System</p>
          {#if isGuest}
            <button class="login-prompt" on:click={() => { showAuth = true; }}>
              Sign in to save your chats
            </button>
          {/if}
        </header>

        {#if $isAuthenticated && $messages.length > 0}
          <ChatHistory />
        {/if}

        <div class="input-section">
          <label for="question">Ask me anything</label>
          <textarea
            id="question"
            bind:value={inputText}
            on:keydown={handleKeydown}
            placeholder="Type your question here... (coding, math, grammar, research, planning)"
            disabled={isProcessing}
          ></textarea>
        </div>

        <div class="button-group">
          <button
            class="text-button"
            on:click={handleTextSubmit}
            disabled={!inputText.trim() || isProcessing}
          >
            <span class="icon">✨</span>
            <span>Ask</span>
          </button>

          <VoiceButton
            on:recorded={handleVoiceRecorded}
            on:error={handleVoiceError}
          />
        </div>

        <StatusIndicator />

        {#if $error}
          <div class="error-message">
            <span class="error-icon">⚠️</span>
            <span class="error-text">{$error}</span>
            <button class="error-close" on:click={clearError}>×</button>
          </div>
        {/if}

        {#if !$isAuthenticated || $messages.length === 0}
          <ResponseCard />
        {/if}

        <AgentsList />
      </div>
    </main>
  </div>
{/if}

<style>
  :global(*) {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  :global(body) {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
    color: #333;
  }

  .app-layout {
    display: flex;
    min-height: 100vh;
  }

  .app-layout.with-sidebar main {
    flex: 1;
    margin-left: 0;
  }

  main {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 40px 20px;
    overflow-y: auto;
  }

  .container {
    background: rgba(255, 255, 255, 0.97);
    border-radius: 24px;
    padding: 40px;
    max-width: 700px;
    width: 100%;
    box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3);
  }

  header {
    text-align: center;
    margin-bottom: 32px;
  }

  h1 {
    font-size: 2.2em;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 8px;
  }

  .subtitle {
    color: #888;
    font-size: 14px;
    font-weight: 500;
  }

  .login-prompt {
    margin-top: 12px;
    padding: 8px 16px;
    border: 1px solid #667eea;
    border-radius: 20px;
    background: transparent;
    color: #667eea;
    font-size: 13px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .login-prompt:hover {
    background: #667eea;
    color: white;
  }

  .input-section {
    margin-bottom: 20px;
  }

  label {
    display: block;
    font-size: 14px;
    font-weight: 600;
    color: #444;
    margin-bottom: 10px;
  }

  textarea {
    width: 100%;
    padding: 16px;
    border: 2px solid #e8e8e8;
    border-radius: 12px;
    font-size: 16px;
    font-family: inherit;
    resize: vertical;
    min-height: 100px;
    transition: all 0.2s;
    background: #fafafa;
  }

  textarea:focus {
    outline: none;
    border-color: #667eea;
    background: white;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  }

  textarea:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  textarea::placeholder {
    color: #aaa;
  }

  .button-group {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
  }

  .text-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 16px 32px;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    flex: 1;
  }

  .text-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  .text-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .icon {
    font-size: 18px;
  }

  .error-message {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 18px;
    background: #fef2f2;
    border: 1px solid #fecaca;
    border-radius: 10px;
    margin-bottom: 20px;
    animation: shake 0.3s ease;
  }

  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
  }

  .error-icon {
    font-size: 18px;
  }

  .error-text {
    flex: 1;
    color: #dc2626;
    font-size: 14px;
  }

  .error-close {
    background: none;
    border: none;
    font-size: 20px;
    color: #999;
    cursor: pointer;
    padding: 0 4px;
    line-height: 1;
  }

  .error-close:hover {
    color: #666;
  }

  @media (max-width: 768px) {
    .app-layout.with-sidebar main {
      margin-left: 50px;
    }
  }

  @media (max-width: 500px) {
    .container {
      padding: 24px;
    }

    .button-group {
      flex-direction: column;
    }

    h1 {
      font-size: 1.8em;
    }
  }
</style>
