'use client'

import React, { useState, useEffect } from 'react'
import "./landing.css"

const Landing = () => {

  useEffect(() => {

    const addMessage = (message: string) => {
      const messageBox = document.getElementById('message-box') as HTMLDivElement;
      const messageElement = document.createElement('div') as HTMLDivElement;
      messageElement.className = 'message';
      messageElement.innerText = message;
      messageBox.appendChild(messageElement);
      messageBox.scrollTop = messageBox.scrollHeight;
    }

    const input = document.querySelector('.question') as HTMLInputElement;
    input.addEventListener('keydown', (e) => {
      const filePicker = document.querySelector('.file-picker') as HTMLInputElement;
      if (e.key === 'Enter') {
        if (input.value == "") {
          return;
        }
        if (filePicker.files && filePicker.files.length > 0) {
          addMessage(input.value);
          input.value = '';
          input.placeholder = 'Enter a question...';

          // Send question to backend to be parsed and stored in database (possibly)
          // Should return a response from backend to be displayed in message box
          // addMessage(response);
        } else {
          input.placeholder = 'Please select a PDF first!';
          input.value = '';
        }
      }
    });
  }, []);

  useEffect(() => {

    const filePicker = document.querySelector('.file-picker') as HTMLInputElement;
    filePicker.addEventListener('change', (e) => {
      const fileLabel = document.querySelector('.file-label span') as HTMLLabelElement;
      const fileName = document.querySelector('.fileName') as HTMLHeadingElement;
      const question = document.querySelector('.question') as HTMLInputElement;
      const files = filePicker.files as FileList;
      const file = files[0];

      fileLabel.innerText = "Selected"
      fileName.innerText = file.name.slice(0, -4);
      question.placeholder = "Enter a question...";

      // Sent file to backend to be parsed and stored in database (possibly)
      // TODO: Display some type of loading animation while file is being parsed
    });
  }, []);

  return (
    <div id='Landing'>
      <p className='fileName'>&nbsp;</p>
      <div className="box" id="message-box"></div>
      <div className="inputs">
        <input type="text" className="question" placeholder="Enter a question..."></input>
        <label className="file-label">
          <input type="file" className="file-picker" accept='.pdf' />
          <span>Select PDF</span>
        </label>
      </div>
    </div>
  )
}

export default Landing;