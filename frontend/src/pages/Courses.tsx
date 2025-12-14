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
      // VULNERABLE: XSS - search query will be reflected unsafely
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
              <h3>{course.code}</h3>
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

      {/* VULNERABLE: XSS - Search query reflected without sanitization */}
      {searchQuery && (
        <div className="search-results">
          <h3>Search Results for: <span dangerouslySetInnerHTML={{ __html: searchQuery }} /></h3>
        </div>
      )}
    </div>
  )
}

export default Courses

