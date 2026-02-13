<script>
  import { messages } from '../stores/chat.js';
  import { textToSpeech } from '../services/api.js';
  import AgentBadge from './AgentBadge.svelte';

  let playingMessageId = null;
  let currentAudio = null;

  async function playMessage(message) {
    if (playingMessageId === message.id) {
      stopAudio();
      return;
    }

    stopAudio();
    playingMessageId = message.id;

    try {
      currentAudio = await textToSpeech(message.content);
      currentAudio.onended = () => {
        playingMessageId = null;
        currentAudio = null;
      };
    } catch {
      playingMessageId = null;
      currentAudio = null;
    }
  }

  function stopAudio() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    playingMessageId = null;
  }

  function formatTime(dateStr) {
    return new Date(dateStr).toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit'
    });
  }
</script>

{#if $messages.length > 0}
  <div class="chat-history">
    {#each $messages as message (message.id)}
      <div class="message {message.role}">
        <div class="message-header">
          {#if message.role === 'assistant' && message.agent_used}
            <AgentBadge agentType={message.agent_used} />
          {:else}
            <span class="role-label">{message.role === 'user' ? 'You' : 'Assistant'}</span>
          {/if}
          <span class="time">{formatTime(message.created_at)}</span>
        </div>
        <div class="message-content">
          {message.content}
        </div>
        {#if message.role === 'assistant'}
          <div class="message-actions">
            <button
              class="action-btn"
              on:click={() => playMessage(message)}
              title={playingMessageId === message.id ? 'Stop' : 'Play'}
            >
              {playingMessageId === message.id ? '⏹️' : '▶️'}
            </button>
          </div>
        {/if}
      </div>
    {/each}
  </div>
{/if}

<style>
  .chat-history {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 20px;
    max-height: 400px;
    overflow-y: auto;
    padding: 16px;
    background: #f8f9fa;
    border-radius: 12px;
  }

  .message {
    padding: 16px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .message.user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 40px;
  }

  .message.assistant {
    margin-right: 40px;
  }

  .message-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 12px;
  }

  .role-label {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.8;
  }

  .time {
    opacity: 0.6;
    font-size: 11px;
  }

  .message-content {
    line-height: 1.6;
    white-space: pre-wrap;
  }

  .message-actions {
    margin-top: 12px;
    display: flex;
    gap: 8px;
  }

  .action-btn {
    background: #f0f0f0;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
  }

  .action-btn:hover {
    background: #e0e0e0;
  }

  @media (max-width: 600px) {
    .message.user {
      margin-left: 20px;
    }

    .message.assistant {
      margin-right: 20px;
    }
  }
</style>
