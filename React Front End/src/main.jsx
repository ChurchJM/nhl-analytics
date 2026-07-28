import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import BoxScore from './BoxScore.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BoxScore />
  </StrictMode>,
)
