import React, { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import LoginForm from './components/LoginForm'
import SearchForm from './components/SearchForm'
import MovieList from './components/MovieList'
import PersonList from './components/PersonList'
import './App.css'

function App() {
  const [token, setToken] = useState('')

  const handleLogin = (token) => {
    setToken(token)
  }

  return (
    <Router>
      <div className="App">
        <h1>Movie and Person Search</h1>

        <Routes>
          <Route path="/login" element={<LoginForm onLogin={handleLogin} />} />
          <Route path="/search" element={<SearchForm token={token} />} />
          <Route path="/movies" element={<MovieList token={token} />} />
          <Route path="/people" element={<PersonList token={token} />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
