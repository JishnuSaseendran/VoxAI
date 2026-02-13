<script>
  import { currentStep, PROCESSING_STEPS } from '../stores/assistant.js';

  $: isActive = $currentStep.id !== 'idle' && $currentStep.id !== 'complete';
  $: isComplete = $currentStep.id === 'complete';
  $: isError = $currentStep.id === 'error';
</script>

{#if $currentStep.id !== 'idle'}
  <div class="status-container" class:active={isActive} class:complete={isComplete} class:error={isError}>
    <div class="status-content">
      {#if isActive}
        <div class="spinner"></div>
      {/if}
      <span class="status-icon">{$currentStep.icon}</span>
      <span class="status-label">{$currentStep.label}</span>
    </div>

    {#if isActive}
      <div class="progress-bar">
        <div class="progress-fill"></div>
      </div>
    {/if}
  </div>
{/if}

<style>
  .status-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    color: white;
    transition: all 0.3s ease;
  }

  .status-container.complete {
    background: linear-gradient(135deg, #27ae60 0%, #1e8449 100%);
  }

  .status-container.error {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  }

  .status-content {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .status-icon {
    font-size: 18px;
  }

  .status-label {
    font-weight: 500;
    font-size: 14px;
  }

  .progress-bar {
    margin-top: 12px;
    height: 4px;
    background: rgba(255,255,255,0.2);
    border-radius: 2px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: white;
    border-radius: 2px;
    animation: progress 2s ease-in-out infinite;
  }

  @keyframes progress {
    0% { width: 0%; transform: translateX(0); }
    50% { width: 70%; }
    100% { width: 100%; transform: translateX(0); }
  }
</style>
