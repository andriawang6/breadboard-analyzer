import React, { useState, useEffect } from 'react'

function App() {
  const [data, setData] = useState([{}])

  useEffect(() => {
    fetch("/fruit").then(response => {
      return response.json();
    })
    .then((data) => {
      setData(data)
      console.log(data);
    })
  }, [])

  return (
    <div>
      {(typeof data.fruit === 'undefined') ? (
        <p>Loading</p>
      ):(
        <p className="text-3xl font-bold underline">Data works</p>
      )}
    </div>
  )
}

export default App