<script>
  import { answer, question, currentAgent, currentStep } from '../stores/assistant.js';
  import { textToSpeech } from '../services/api.js';
  import AgentBadge from './AgentBadge.svelte';

  let isPlaying = false;
  let currentAudio = null;

  async function playAnswer() {
    if (!$answer || isPlaying) return;

    isPlaying = true;
    try {
      currentAudio = await textToSpeech($answer);
      currentAudio.onended = () => {
        isPlaying = false;
        currentAudio = null;
      };
      currentAudio.onerror = () => {
        isPlaying = false;
        currentAudio = null;
      };
    } catch {
      isPlaying = false;
      currentAudio = null;
    }
  }

  function stopAnswer() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
      currentAudio = null;
    }
    isPlaying = false;
  }

  $: showResponse = $currentStep.id === 'complete' && $answer;
</script>

{#if showResponse}
  <div class="response-card">
    <div class="response-header">
      <AgentBadge agentType={$currentAgent} />
    </div>

    <div class="response-body">
      <div class="question-section">
        <span class="label">Your question</span>
        <p class="question-text">{$question}</p>
      </div>

      <div class="answer-section">
        <span class="label">Answer</span>
        <p class="answer-text">{$answer}</p>
      </div>
    </div>

    <div class="response-footer">
      <button class="play-button" on:click={playAnswer} disabled={isPlaying}>
        <span class="icon">{isPlaying ? '🔊' : '▶️'}</span>
        <span>{isPlaying ? 'Playing...' : 'Play Answer'}</span>
      </button>
      {#if isPlaying}
        <button class="stop-button" on:click={stopAnswer}>
          <span class="icon">⏹️</span>
          <span>Stop</span>
        </button>
      {/if}
    </div>
  </div>
{/if}

<style>
  .response-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    overflow: hidden;
    margin-top: 20px;
    animation: slideUp 0.3s ease;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .response-header {
    padding: 16px 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
  }

  .response-body {
    padding: 20px;
  }

  .question-section {
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
  }

  .label {
    display: block;
    font-size: 12px;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }

  .question-text {
    color: #555;
    font-style: italic;
    line-height: 1.5;
    margin: 0;
  }

  .answer-text {
    color: #1a1a2e;
    line-height: 1.7;
    white-space: pre-wrap;
    margin: 0;
  }

  .response-footer {
    padding: 16px 20px;
    background: #f8f9fa;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
  }

  .play-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    background: linear-gradient(135deg, #27ae60 0%, #1e8449 100%);
    color: white;
  }

  .play-button:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
  }

  .play-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .stop-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    color: white;
  }

  .stop-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
  }

  .icon {
    font-size: 16px;
  }
</style>
