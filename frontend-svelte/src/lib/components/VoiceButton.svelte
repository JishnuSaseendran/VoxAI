<script>
  import { createEventDispatcher } from 'svelte';
  import { isRecording, currentStep, PROCESSING_STEPS } from '../stores/assistant.js';

  const dispatch = createEventDispatcher();

  let mediaRecorder = null;
  let audioChunks = [];

  function getSupportedMimeType() {
    const types = [
      'audio/webm',
      'audio/webm;codecs=opus',
      'audio/ogg;codecs=opus',
      'audio/mp4',
      'audio/mpeg'
    ];
    for (const type of types) {
      if (MediaRecorder.isTypeSupported(type)) {
        return type;
      }
    }
    return 'audio/webm';
  }

  function getExtensionFromMime(mimeType) {
    const mimeToExt = {
      'audio/webm': '.webm',
      'audio/webm;codecs=opus': '.webm',
      'audio/ogg;codecs=opus': '.ogg',
      'audio/ogg': '.ogg',
      'audio/mp4': '.m4a',
      'audio/mpeg': '.mp3',
      'audio/wav': '.wav'
    };
    return mimeToExt[mimeType] || '.webm';
  }

  async function startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = getSupportedMimeType();

      mediaRecorder = new MediaRecorder(stream, { mimeType });
      audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const mimeType = mediaRecorder.mimeType;
        const audioBlob = new Blob(audioChunks, { type: mimeType });
        const extension = getExtensionFromMime(mimeType);
        stream.getTracks().forEach(track => track.stop());
        dispatch('recorded', { audioBlob, extension });
      };

      mediaRecorder.start();
      isRecording.set(true);
      currentStep.set(PROCESSING_STEPS.RECORDING);
    } catch (err) {
      dispatch('error', { message: 'Microphone access denied. Please allow microphone access.' });
    }
  }

  function stopRecording() {
    if (mediaRecorder && $isRecording) {
      mediaRecorder.stop();
      isRecording.set(false);
    }
  }

  function toggleRecording() {
    if ($isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  }
</script>

<button
  class="voice-button"
  class:recording={$isRecording}
  on:click={toggleRecording}
  disabled={$currentStep.id !== 'idle' && $currentStep.id !== 'complete' && $currentStep.id !== 'error' && !$isRecording}
>
  <span class="icon">{$isRecording ? '⏹️' : '🎤'}</span>
  <span class="label">{$isRecording ? 'Stop Recording' : 'Click to Speak'}</span>
</button>

<style>
  .voice-button {
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
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    color: white;
    flex: 1;
  }

  .voice-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.4);
  }

  .voice-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .voice-button.recording {
    background: linear-gradient(135deg, #c0392b 0%, #96281b 100%);
    animation: pulse 1.5s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
    50% { box-shadow: 0 0 0 15px rgba(231, 76, 60, 0); }
  }

  .icon {
    font-size: 20px;
  }
</style>
