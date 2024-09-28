import React, { useState, useEffect } from 'react'

function App() {
  const [image, setImage] = React.useState([]);

  const imageUpload = () => {
    if(image != null) {
      const fd = new FormData()
      fd.append('image', image)

      fetch("/image", {
        method: "POST",
        body: fd
      })
      .then(result => result.json())
      .then(data => console.log(data)) //log result
    }
    
  }

  return (
    <div>
      <h1>Image Upload</h1>
      <input type="file" onChange={ (event) => { 
        setImage(event.target.files[0]) 
      } } />
      <button onClick={ () => {imageUpload()} }>Upload</button>

    </div>
  )
}

export default App