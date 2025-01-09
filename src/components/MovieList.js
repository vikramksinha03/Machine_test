import React, { useEffect, useState } from 'react'
import axios from 'axios'

function MovieList({ token }) {
  const [movies, setMovies] = useState([])

  const fetchMovies = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/search_movie', {
        params: {
          year: 2022, // Example search criteria
          genre: 'Drama',
          type: 'Movie',
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      setMovies(response.data)
    } catch (error) {
      console.error('Error fetching movies', error)
    }
  }

  useEffect(() => {
    fetchMovies()
  }, [token])

  return (
    <div>
      <h2>Movie List</h2>
      <div>
        {movies.map((movie, index) => (
          <div key={index}>
            <h3>{movie.Title}</h3>
            <p>{movie['Original Title']}</p>
            <p>{movie['Year Released']}</p>
            <p>{movie.Genre}</p>
            <p>{movie.Type}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default MovieList
