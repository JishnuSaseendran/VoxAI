<script>
  import { AGENTS } from '../stores/assistant.js';

  export let agentType = 'general';

  $: agent = AGENTS[agentType] || AGENTS.general;
</script>

<div class="agent-badge" style="--agent-color: {agent.color}">
  <span class="agent-icon">{agent.icon}</span>
  <span class="agent-name">{agent.name}</span>
  <span class="agent-desc">{agent.description}</span>
</div>

<style>
  .agent-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--agent-color);
    color: white;
    padding: 8px 16px;
    border-radius: 24px;
    font-size: 13px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  .agent-icon {
    font-size: 16px;
  }

  .agent-name {
    font-weight: 700;
  }

  .agent-desc {
    opacity: 0.85;
    font-weight: 400;
  }

  @media (max-width: 500px) {
    .agent-desc {
      display: none;
    }
  }
</style>
