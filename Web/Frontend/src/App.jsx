import React from 'react'
import { Routes, Route} from 'react-router-dom'
import './App.css'
import SideNavigation from './component/SideNav/nav'
import Download from './component/Upload/upload'
import Upload from './component/Upload/upload'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap-icons/font/bootstrap-icons.css'

function App() {
  return (
    
    <SideNavigation
      content={
        <Routes>
            <Route path="/upload" element={<Upload />} />
            <Route path='/download' element={<Download />} />
        </Routes>
      }
    />
  )
}

export default App
