import React from 'react'
import './page.css'

const Landing = () => {
  
  return (
    <div id='Landing'>
      		<div className="box" id="message-box"></div>
          <div className="inputs">
            <input type="text" className="question" placeholder="Enter a question"></input>
            <input type="file" className="file-picker" accept=".pdf"></input>
          </div>
    </div>
  )
}

export default Landing