import { writable } from 'svelte/store';

// Processing status steps
export const PROCESSING_STEPS = {
  IDLE: { id: 'idle', label: '', icon: '' },
  RECORDING: { id: 'recording', label: 'Recording audio...', icon: '🎤' },
  TRANSCRIBING: { id: 'transcribing', label: 'Transcribing speech...', icon: '📝' },
  ROUTING: { id: 'routing', label: 'Router analyzing query...', icon: '🔀' },
  PROCESSING: { id: 'processing', label: 'Agent processing...', icon: '⚙️' },
  GENERATING: { id: 'generating', label: 'Generating response...', icon: '💭' },
  COMPLETE: { id: 'complete', label: 'Complete!', icon: '✅' },
  ERROR: { id: 'error', label: 'Error occurred', icon: '❌' }
};

// Agent information
export const AGENTS = {
  general: { name: 'General', color: '#4a90d9', icon: '💡', description: 'Knowledge & explanations' },
  coding: { name: 'Coding', color: '#f39c12', icon: '💻', description: 'Programming & debugging' },
  grammar: { name: 'Grammar', color: '#9b59b6', icon: '✏️', description: 'Sentence correction' },
  research: { name: 'Research', color: '#1abc9c', icon: '🔍', description: 'Deep analysis' },
  planning: { name: 'Planner', color: '#e74c3c', icon: '📋', description: 'Step-by-step plans' },
  creative: { name: 'Creative', color: '#e91e63', icon: '🎨', description: 'Writing & content' },
  math: { name: 'Math', color: '#3498db', icon: '🔢', description: 'Calculations & problems' },
  conversation: { name: 'Conversation', color: '#27ae60', icon: '💬', description: 'Casual chat' }
};

// Create stores
export const isRecording = writable(false);
export const currentStep = writable(PROCESSING_STEPS.IDLE);
export const currentAgent = writable(null);
export const question = writable('');
export const answer = writable('');
export const error = writable(null);
export const history = writable([]);

// Helper to update step with agent name
export function setProcessingStep(step, agentType = null) {
  if (agentType && step.id === 'processing') {
    const agent = AGENTS[agentType] || AGENTS.general;
    currentStep.set({
      ...step,
      label: `${agent.icon} ${agent.name} agent processing...`
    });
    currentAgent.set(agentType);
  } else {
    currentStep.set(step);
  }
}

// Reset to idle state
export function resetState() {
  currentStep.set(PROCESSING_STEPS.IDLE);
  error.set(null);
}
