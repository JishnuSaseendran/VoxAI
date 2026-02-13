<script>
  import { AGENTS } from '../stores/assistant.js';

  let expanded = false;

  const agentEntries = Object.entries(AGENTS);
</script>

<div class="agents-section">
  <button class="toggle-button" on:click={() => expanded = !expanded}>
    <span>Available Agents</span>
    <span class="arrow" class:expanded>{expanded ? '▲' : '▼'}</span>
  </button>

  {#if expanded}
    <div class="agents-grid">
      {#each agentEntries as [key, agent]}
        <div class="agent-card" style="--agent-color: {agent.color}">
          <span class="agent-icon">{agent.icon}</span>
          <div class="agent-info">
            <span class="agent-name">{agent.name}</span>
            <span class="agent-desc">{agent.description}</span>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  .agents-section {
    margin-top: 24px;
  }

  .toggle-button {
    width: 100%;
    padding: 12px 20px;
    background: transparent;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 500;
    color: #666;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s;
  }

  .toggle-button:hover {
    background: #f8f9fa;
    border-color: #ccc;
  }

  .arrow {
    transition: transform 0.2s;
  }

  .agents-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 12px;
    margin-top: 16px;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .agent-card {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: #f8f9fa;
    border-radius: 10px;
    border-left: 4px solid var(--agent-color);
    transition: all 0.2s;
  }

  .agent-card:hover {
    background: #f0f0f0;
    transform: translateX(4px);
  }

  .agent-icon {
    font-size: 24px;
  }

  .agent-info {
    display: flex;
    flex-direction: column;
  }

  .agent-name {
    font-weight: 600;
    color: #333;
    font-size: 14px;
  }

  .agent-desc {
    font-size: 12px;
    color: #888;
  }
</style>
