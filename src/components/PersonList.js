import React, { useEffect, useState } from 'react'
import axios from 'axios'

function PersonList({ token }) {
  const [people, setPeople] = useState([])

  const fetchPeople = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/search_person', {
        params: {
          movie_title: 'Inception', // Example search criteria
          name: 'Leonardo',
          profession: 'Actor',
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      setPeople(response.data)
    } catch (error) {
      console.error('Error fetching people', error)
    }
  }

  useEffect(() => {
    fetchPeople()
  }, [token])

  return (
    <div>
      <h2>Person List</h2>
      <div>
        {people.map((person, index) => (
          <div key={index}>
            <h3>{person.Name}</h3>
            <p>{person.Profession}</p>
            <p>{person['Birth Year']}</p>
            <p>{person['Known for Titles'].join(', ')}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default PersonList
