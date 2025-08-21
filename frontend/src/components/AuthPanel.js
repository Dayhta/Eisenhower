import React, { useState } from 'react';
import { authService, setAccessToken } from '../services/api';

const AuthPanel = ({ onAuth }) => {
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const toggleMode = () => { setMode(mode === 'login' ? 'register' : 'login'); setError(''); };

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      if (mode === 'register') {
        await authService.login(email, password); // placeholder for register
      }
      const { access_token } = await authService.login(email, password);
      setAccessToken(access_token);
      onAuth(access_token, email);
    } catch {
      setError('Authentication failed');
    } finally { setLoading(false); }
  };

  return (
    <div className="auth-panel">
      <h3>{mode === 'login' ? 'Login' : 'Register'}</h3>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} required minLength={6} />
        </div>
        <button type="submit" disabled={loading}>{loading ? 'Please wait...' : (mode==='login'?'Login':'Create Account')}</button>
      </form>
      <button className="link" onClick={toggleMode}>
        {mode === 'login' ? 'Need an account? Register' : 'Already have an account? Login'}
      </button>
    </div>
  );
};

export default AuthPanel;
