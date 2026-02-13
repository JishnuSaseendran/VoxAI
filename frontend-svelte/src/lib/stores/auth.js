import { writable } from 'svelte/store';

// User state
export const user = writable(null);
export const token = writable(null);
export const isAuthenticated = writable(false);

// Initialize from localStorage
export function initAuth() {
  const storedToken = localStorage.getItem('token');
  const storedUser = localStorage.getItem('user');

  if (storedToken && storedUser) {
    token.set(storedToken);
    user.set(JSON.parse(storedUser));
    isAuthenticated.set(true);
  }
}

// Set auth data after login/signup
export function setAuth(authToken, userData) {
  token.set(authToken);
  user.set(userData);
  isAuthenticated.set(true);

  localStorage.setItem('token', authToken);
  localStorage.setItem('user', JSON.stringify(userData));
}

// Clear auth data on logout
export function clearAuth() {
  token.set(null);
  user.set(null);
  isAuthenticated.set(false);

  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

// Get current token value
export function getToken() {
  let currentToken = null;
  token.subscribe(value => {
    currentToken = value;
  })();
  return currentToken;
}
