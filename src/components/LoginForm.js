import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

function LoginForm({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        username,
        password,
      })
      const token = response.data.access_token
      onLogin(token)
      navigate('/search') // Redirect to search page after login
    } catch (error) {
      setError('Invalid credentials')
    }
  }

  return (
    <div>
      <h2>Login</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}

export default LoginForm
