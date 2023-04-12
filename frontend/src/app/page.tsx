'use client'

import React, { useState, useEffect } from 'react'
import "./landing.css"
import axios from 'axios'

const Landing = () => {

  const addMessage = (message: string) => {
    const messageBox = document.getElementById('message-box') as HTMLDivElement;
    const messageElement = document.createElement('div') as HTMLDivElement;
    messageElement.className = 'message';
    messageElement.innerText = message;
    messageBox.appendChild(messageElement);
    messageBox.scrollTop = messageBox.scrollHeight;
  }


  const sendFile = async (file: File) => {
    const question = document.querySelector('.question') as HTMLInputElement;
    const body = document.querySelector('body') as HTMLBodyElement;
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://localhost:8000/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then((response) => {
      question.readOnly = false;
      body.style.cursor = "";
      if (response.status == 201) {
        question.placeholder = "Enter a question...";
        console.log(response);
      }
    }).catch((error) => {
      console.log(error);
    });
  }

  useEffect(() => {
    const getAnswer = async (question: string) => {
      console.log("queston: " + question);
      axios.get('http://localhost:8000/question/', {
        params: {
          question: question
        }
      }).then((response) => {
        if (response.status == 200) {
          addMessage(response.data.answer);
        }
      }).catch((error) => {
        console.log(error);
      });
    }

    const input = document.querySelector('.question') as HTMLInputElement;
    input.addEventListener('keydown', (e) => {
      const filePicker = document.querySelector('.file-picker') as HTMLInputElement;
      if (e.key === 'Enter') {
        if (input.value == "") {
          return;
        }
        if (filePicker.files && filePicker.files.length > 0) {
          addMessage("Q: " + input.value);
          getAnswer(input.value);
          input.value = '';
          input.placeholder = 'Enter a question...';

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
      const body = document.querySelector('body') as HTMLBodyElement; 
      const files = filePicker.files as FileList;
      const file = files[0];

      body.style.cursor = "wait"
      question.readOnly = true;
      question.placeholder = "Loading...";
      fileName.innerText = file.name.slice(0, -4);
      fileLabel.innerText = "Selected"
      
      sendFile(file);

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