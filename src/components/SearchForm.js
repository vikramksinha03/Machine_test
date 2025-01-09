import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function SearchForm({ token }) {
  const [year, setYear] = useState('')
  const [genre, setGenre] = useState('')
  const [type, setType] = useState('')
  const navigate = useNavigate()

  const searchMovies = () => {
    navigate(`/movies?year=${year}&genre=${genre}&type=${type}`)
  }

  const searchPeople = () => {
    navigate(`/people?movie_title=${genre}&name=${type}`)
  }

  return (
    <div>
      <h2>Search Movies and People</h2>
      <div>
        <input
          type="number"
          placeholder="Year"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />
        <input
          type="text"
          placeholder="Genre"
          value={genre}
          onChange={(e) => setGenre(e.target.value)}
        />
        <input
          type="text"
          placeholder="Type"
          value={type}
          onChange={(e) => setType(e.target.value)}
        />
        <button onClick={searchMovies}>Search Movies</button>
        <button onClick={searchPeople}>Search People</button>
      </div>
    </div>
  )
}

export default SearchForm
