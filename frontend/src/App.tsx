import { Route, Routes } from 'react-router-dom'
import { Home, Event } from '@/pages'

function App() {
  return (
    <>
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/home' element={<Home />} />
      <Route path='/events/:id' element={<Event />} />
    </Routes>
    </>
  )
}

export default App
