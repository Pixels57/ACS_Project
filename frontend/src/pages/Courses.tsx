import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { coursesAPI } from '../services/api'
import './Courses.css'

interface Course {
  id: number
  code: string
  title: string
  description: string
  capacity: number
}

const Courses = () => {
  const [courses, setCourses] = useState<Course[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadCourses()
  }, [])

  const loadCourses = async () => {
    try {
      const data = await coursesAPI.getAll()
      setCourses(data)
    } catch (error) {
      console.error('Failed to load courses:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadCourses()
      return
    }

    try {
      // SECURE: We just send the text. The backend handles the filtering logic.
      const data = await coursesAPI.search(searchQuery)
      setCourses(data)
    } catch (error) {
      console.error('Search failed:', error)
    }
  }

  return (
    <div className="courses-page">
      <h1>Course Catalog</h1>
      
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search courses..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="courses-grid">
          {courses.map((course) => (
            <div key={course.id} className="course-card">
              {/* Display code if available */}
              <h3>{course.code || `CS${course.id}00`}</h3>
              <h4>{course.title}</h4>
              <p>{course.description}</p>
              <div className="course-meta">
                <span>Capacity: {course.capacity}</span>
              </div>
              <Link to={`/courses/${course.id}`} className="view-btn">
                View Details
              </Link>
            </div>
          ))}
        </div>
      )}

      {searchQuery && (
        <div className="search-results">
          {/* SECURE FIX: Removed dangerouslySetInnerHTML */}
          {/* React will now treat <img...> as the string "<img...>" */}
          <h3>Search Results for: <span>{searchQuery}</span></h3>
        </div>
      )}
    </div>
  )
}

export default Courses