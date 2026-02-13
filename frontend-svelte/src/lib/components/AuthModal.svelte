<script>
  import { createEventDispatcher } from 'svelte';
  import { login, signup } from '../services/api.js';
  import { setAuth } from '../stores/auth.js';

  const dispatch = createEventDispatcher();

  let mode = 'login'; // 'login' or 'signup'
  let email = '';
  let username = '';
  let password = '';
  let confirmPassword = '';
  let error = null;
  let isLoading = false;

  function toggleMode() {
    mode = mode === 'login' ? 'signup' : 'login';
    error = null;
  }

  async function handleSubmit() {
    error = null;

    if (!email || !password) {
      error = 'Please fill in all required fields';
      return;
    }

    if (mode === 'signup') {
      if (!username) {
        error = 'Username is required';
        return;
      }
      if (password !== confirmPassword) {
        error = 'Passwords do not match';
        return;
      }
      if (password.length < 6) {
        error = 'Password must be at least 6 characters';
        return;
      }
    }

    isLoading = true;

    try {
      let result;
      if (mode === 'login') {
        result = await login(email, password);
      } else {
        result = await signup(email, username, password);
      }

      setAuth(result.access_token, result.user);
      dispatch('success');
    } catch (err) {
      error = err.message;
    } finally {
      isLoading = false;
    }
  }

  function handleKeydown(e) {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  }
</script>

<div class="auth-overlay">
  <div class="auth-modal">
    <div class="auth-header">
      <h2>{mode === 'login' ? 'Welcome Back' : 'Create Account'}</h2>
      <p class="subtitle">
        {mode === 'login' ? 'Sign in to access your chat history' : 'Sign up to save your conversations'}
      </p>
    </div>

    <form on:submit|preventDefault={handleSubmit} class="auth-form">
      {#if error}
        <div class="error-message">{error}</div>
      {/if}

      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          bind:value={email}
          on:keydown={handleKeydown}
          placeholder="your@email.com"
          disabled={isLoading}
        />
      </div>

      {#if mode === 'signup'}
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            bind:value={username}
            on:keydown={handleKeydown}
            placeholder="Your name"
            disabled={isLoading}
          />
        </div>
      {/if}

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          bind:value={password}
          on:keydown={handleKeydown}
          placeholder="••••••••"
          disabled={isLoading}
        />
      </div>

      {#if mode === 'signup'}
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            bind:value={confirmPassword}
            on:keydown={handleKeydown}
            placeholder="••••••••"
            disabled={isLoading}
          />
        </div>
      {/if}

      <button type="submit" class="submit-button" disabled={isLoading}>
        {#if isLoading}
          <span class="spinner"></span>
        {:else}
          {mode === 'login' ? 'Sign In' : 'Create Account'}
        {/if}
      </button>
    </form>

    <div class="auth-footer">
      <p>
        {mode === 'login' ? "Don't have an account?" : 'Already have an account?'}
        <button class="toggle-button" on:click={toggleMode} disabled={isLoading}>
          {mode === 'login' ? 'Sign up' : 'Sign in'}
        </button>
      </p>
    </div>

    <div class="guest-option">
      <button class="guest-button" on:click={() => dispatch('skip')}>
        Continue as Guest
      </button>
    </div>
  </div>
</div>

<style>
  .auth-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    z-index: 1000;
  }

  .auth-modal {
    background: white;
    border-radius: 20px;
    padding: 40px;
    max-width: 400px;
    width: 100%;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  }

  .auth-header {
    text-align: center;
    margin-bottom: 30px;
  }

  .auth-header h2 {
    color: #1a1a2e;
    margin: 0 0 10px;
    font-size: 1.8em;
  }

  .subtitle {
    color: #666;
    font-size: 14px;
    margin: 0;
  }

  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .form-group label {
    font-size: 14px;
    font-weight: 600;
    color: #333;
  }

  .form-group input {
    padding: 12px 16px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    font-size: 16px;
    transition: border-color 0.2s;
  }

  .form-group input:focus {
    outline: none;
    border-color: #667eea;
  }

  .form-group input:disabled {
    background: #f5f5f5;
  }

  .error-message {
    background: #fee;
    color: #c00;
    padding: 12px;
    border-radius: 8px;
    font-size: 14px;
    text-align: center;
  }

  .submit-button {
    padding: 14px;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .submit-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
  }

  .submit-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .spinner {
    width: 20px;
    height: 20px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .auth-footer {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #eee;
  }

  .auth-footer p {
    color: #666;
    font-size: 14px;
    margin: 0;
  }

  .toggle-button {
    background: none;
    border: none;
    color: #667eea;
    font-weight: 600;
    cursor: pointer;
    padding: 0;
    font-size: 14px;
  }

  .toggle-button:hover {
    text-decoration: underline;
  }

  .guest-option {
    margin-top: 20px;
    text-align: center;
  }

  .guest-button {
    background: none;
    border: 1px solid #ddd;
    color: #666;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .guest-button:hover {
    background: #f5f5f5;
    border-color: #ccc;
  }
</style>
