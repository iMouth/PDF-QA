'use client'

import React, { useState, useEffect } from 'react'
import "./landing.css"
import axios from 'axios'

const Landing = () => {

  useEffect(() => {
    const getAnswer = async (question: string) => {
      console.log("question: " + question);
      let message = "";

      try {
        const response = await fetch('http://localhost:8000/return_message?question=' + question, {
          method: "GET",
        });
        if (response.ok) {

          // we want the message attribute of the response
          const data = await response.json();
          message = data.message;
          console.log("message: " + message);
        }
      } catch (error) {
        console.log(error);
      }


      try {
        const response = await fetch(`http://localhost:8000/question?question=${encodeURIComponent(question)}`, {
          method: "GET",
        });

        if (response.ok) {
          // Read and process the stream
          const reader = response.body.getReader();
          const decoder = new TextDecoder("utf-8");

          // Create a message element
          const messageElement = document.createElement('div');
          addMessage("A: ", messageElement);

          // Create a span to hold the answer text
          const answerSpan = document.createElement('span');
          messageElement.appendChild(answerSpan);

          let previousText = '';

          while (true) {
            const { value, done } = await reader.read();
            if (done) {
              break;
            }

            const chunks = decoder.decode(value).split("\0");

            for (const chunk of chunks) {
              if (chunk.trim() === "") {
                continue;
              }

              // Parse the chunk and extract the text
              const data = JSON.parse(chunk);
              if (data.error_code === 0) {
                const output = data.text.trim();
                const newText = output.slice(message.length);

                if (newText !== previousText) {
                  answerSpan.innerText += newText.slice(previousText.length);
                  previousText = newText;
                }
              } else {
                const output = data.text + ` (error_code: ${data.error_code})`;
                answerSpan.innerText += output;
                break;
              }
            }
          }
        }
      } catch (error) {
        console.log(error);
      }
    };


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
      //const fileName = document.querySelector('.fileName') as HTMLHeadingElement;
      const question = document.querySelector('.question') as HTMLInputElement;
      const body = document.querySelector('body') as HTMLBodyElement;
      const files = filePicker.files as FileList;
      const file = files[0];
      putPDF(file);

      body.style.cursor = "wait"
      question.readOnly = true;
      question.placeholder = "Loading...";
      //fileName.innerText = file.name.slice(0, -4);
      fileLabel.innerText = "Selected"

      sendFile(file);

    });
  }, []);

  const addMessage = (message: string, messageElement?: HTMLDivElement) => {
    const messageBox = document.getElementById('message-box') as HTMLDivElement;

    if (!messageElement) {
      messageElement = document.createElement('div');
    }
    messageElement.className = 'message';
    messageElement.innerText = message;
    messageBox.appendChild(messageElement);
    messageBox.scrollTop = messageBox.scrollHeight;
  };

  const sendFile = async (file: File) => {
    const question = document.querySelector('.question') as HTMLInputElement;
    const body = document.querySelector('body') as HTMLBodyElement;
    const formData = new FormData();
    formData.append('file', file);
    axios.post('http://localhost:8000/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then((response: { status: number }) => {
      question.readOnly = false;
      body.style.cursor = "";
      if (response.status == 201) {
        question.placeholder = "Enter a question...";
        console.log(response);
      }
    }).catch((error: any) => {
      console.log(error);
    });
  }

  const putPDF = (pdf: File) => {
    const pdfPreview = document.getElementById('pdf-preview') as HTMLObjectElement;
    const reader = new FileReader();
    reader.readAsDataURL(pdf);
    reader.onload = () => {
      const pdfData = reader.result as string;
      pdfPreview.innerHTML = '<embed src="' + pdfData + '" width="100%" height="100%" type="application/pdf">';
    };
  }


  return (
    <div id='Landing'>
      <div id="user-interface">
        {/* <p className='fileName'>&nbsp;</p> */}
        <div className="box" id="message-box"></div>
        <div className="inputs">
          <input type="text" className="question" placeholder="Enter a question..."></input>
          <label className="file-label">
            <input type="file" className="file-picker" accept='.pdf' />
            <span>Select PDF</span>
          </label>
        </div>
      </div>
      <div id="pdf-preview"></div>
    </div>
  )
}

export default Landing;