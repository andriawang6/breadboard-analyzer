import React, { useState } from "react";
import ImageUploading from "react-images-uploading";
import { IoMdPhotos } from "react-icons/io";
import "./fonts/superbakery.ttf";
import "./App.css"; // Ensure to import the CSS file if you're using one

function App() {
  const [images, setImages] = useState([]);
  const [chipPos, setChipPos] = useState([]);
  const [croppedImageUrl, setCroppedImageUrl] = useState(null);
  const [appState, setAppState] = useState("upload"); //either upload, identifyChips, or viewSchematic
  const [unknownChips, setUnknownChips] = useState([]);
  const [chipTypes, setChipTypes] = useState([]);

  const onChange = (imageList) => {
    setImages(imageList);
  };

  function handleChipSubmit(e) {
    // Prevent the browser from reloading the page
    e.preventDefault();
    // Read the form data
    const form = e.target;
    const formData = new FormData(form);
    setChipTypes(chipTypes.concat([formData.get("chips")]))
    //chipTypes.push(formData.get("chips"))
    setUnknownChips(unknownChips - 1)
  }

  const sendChipInfo = () => {
    if(unknownChips === 0) {
      const fd = new FormData();
      fd.append("chips", JSON.parse(JSON.stringify(chipTypes)));
      //POST request to send form info
      fetch("/chipinfo", {
        method: "POST",
        body: fd,
      })
      .then((result) => result.json())
      .then((data) => console.log(data))
      .then(() => {
        getSVG();
      });
    }
  }

  const getChipLocations = () => {
    fetch("/chips", {
      method: "GET"
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`uh oh HTTP error! status: ${response.status}`);
      }
      return response.json()
    })
    .then((data) => {
      setChipPos(data)
      setUnknownChips(data.length)
    });
  }

  const getCroppedImage = () => {
    fetch("/croppedimage", {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`uh oh HTTP error! status: ${response.status}`);
        }
        return response.blob();
      })
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setCroppedImageUrl(url);
        setAppState("identifyChips")
      })
      .catch((error) => {
        console.error("Failed to get cropped image:", error.message);
      });
  };

  const imageUpload = () => {
    if (images.length > 0) {
      const fd = new FormData();
      fd.append("image", images[0].file);

      fetch("/image", {
        method: "POST",
        body: fd,
      })
        .then((result) => result.json())
        .then((data) => console.log(data))
        .then(() => {
          getCroppedImage();
        })
        .then(() => {
          getChipLocations();
        });
    }
  };

  const getSVG = () => {
    fetch("/getSVG", {
      method: "GET",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`svg: uh oh HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log(data)
      });

  }

  const changePhoto = () => {
    // Reset image and show upload area again
    setImages([]);
    setAppState("upload")
  };

  return (
    <div
      style={{
        backgroundImage: `url(static/background.jpg)`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        padding: "20px",
      }}
    >
      <div
        className="superbakery"
        style={{
          marginTop: "10px",
          fontSize: "50px",
          maxWidth: "1000px",
          margin: "0 auto",
          textAlign: "center",
          marginBottom: "-50px",
          color: "#524f4f",
        }}
      >
        BreadBoard Bakery
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "row",
          marginBottom: "-30px",
        }}
      >
        <p
          style={{
            textAlign: "center",
            padding: "5px",
            color: "#524f4f",
            marginRight: "-50px",
          }}
        >
          Add your breadboard image to our bakery! <br /> We'll analyze it and
          give you a freshly baked schematic!
        </p>
        <img
          src={"static/bear.png"}
          style={{
            maxWidth: "15%",
            height: "auto",
            marginLeft: "10px",
          }}
        />
      </div>

      {/* Image upload box */}
      {appState === "upload" && (
        <div
          style={{ maxWidth: "500px", margin: "0 auto", textAlign: "center" }}
        >
          <ImageUploading
            value={images}
            onChange={onChange}
            maxNumber={1}
            dataURLKey="data_url"
          >
            {({
              imageList,
              onImageUpload,
              isDragging,
              dragProps,
              onImageUpdate,
            }) => (
              <div
                style={{
                  border: "2px dashed #ccc",
                  padding: "20px",
                  cursor: "pointer",
                  borderRadius: "10px",
                  backgroundColor: isDragging ? "#f4c089" : "#ffffff",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  minHeight: "200px",
                  width: "100%",
                }}
                onClick={imageList.length === 0 ? onImageUpload : null}
                {...dragProps}
              >
                {imageList.length === 0 ? (
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                      justifyContent: "center",
                      height: "100%",
                    }}
                  >
                    <IoMdPhotos
                      size={50}
                      color="#ccc"
                      style={{ marginBottom: "10px" }}
                    />
                    <div style={{ color: "gray" }}>Browse or Drop Image</div>
                  </div>
                ) : (
                  <div
                    style={{
                      textAlign: "center",
                      width: "100%",
                      display: "flex",
                      flexDirection: "column",
                      alignItems: "center",
                    }}
                  >
                    {imageList.map((image, index) => (
                      <div key={index}>
                        <img
                          src={image.data_url}
                          alt=""
                          style={{
                            width: "auto",
                            maxWidth: "100%",
                            maxHeight: "300px",
                            marginTop: "10px",
                            borderRadius: "10px",
                          }}
                          onClick={() => onImageUpdate(index)}
                        />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </ImageUploading>
          <button
            onClick={imageUpload}
            style={{
              marginTop: "20px",
              padding: "10px 20px",
              borderRadius: "5px",
              border: "none",
              backgroundColor: "#ab7d58",
              color: "white",
              cursor: "pointer",
            }}
          >
            Let's Get Analyzing
          </button>
        </div>
      )}

        {/* show cropped image */}
      {appState === "identifyChips" && (
        <div>
        <div
          style={{
            marginTop: "5px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <p
            style={{
              textAlign: "center",
              padding: "5px",
              color: "#524f4f",
              fontsize: "18 px"
            }}
          >
            Cropped Image
          </p>
        </div>

        {chipPos.length > 0 && ( 
        <div>
        {/* IMAGE CONTAINER */}
        <div style = {{
          position: "relative",
          width: "100%", /* Adjust width as needed */
          maxWidth: "200px" /* Optional: Set a maximum width */,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          margin: "0 auto"
        }}>
          <img
            src={croppedImageUrl}
            alt="Cropped"
            style={{
              width: "100%", /* Make bottom image responsive */
              height: "auto", /* Maintain aspect ratio */
              display: "block"
            }}
          />
          <img
            src="static/pin_icon.svg"
            style={{
              position: "absolute",
              top: `${chipPos[chipPos.length - unknownChips]-2}%`, /* Adjust this value to position the top image */
              left: "50%", /* Center horizontally */
              transform: "translateX(-50%)", /* Adjust to center the image */
              width: "15%", /* Adjust width as needed */
              height: "auto" /* Maintain aspect ratio */
            }}
          />
        </div>
        </div> )}
{/* 
        PROMPT USER */}
        {unknownChips > 0 && (<div style={{ display: "flex", justifyContent: "center", alignItems: "center", flexDirection: "column", margin: "20px 0" }}>
          <p
            style={{
              textAlign: "center",
              padding: "5px",
              marginTop: "-12px",
              marginRight: "10px",
              color: "#524f4f"
            }}
          >
          What chip is this?
          </p>

          <form onSubmit={handleChipSubmit} style={{ display: "flex", alignItems: "center", justifyContent: "center"}}>
            <select name="chips" style={{ marginRight: "10px", padding: "5px"}}>
              <option value="74HCT00">NAND (74HCT00)</option>
              <option value="74HCT02">NOR (74HCT02)</option>
              <option value="74HCT04">NOT (74HCT04)</option>
              <option value="74HCT08">AND (74HCT08)</option>
              <option value="74HCT32">OR (74HCT32)</option>
              <option value="74HCT86">XOR (74HCT86)</option>
            </select>

            <button 
              type="submit"
              style={{
                marginTop: "0",
                marginBottom: "100 px",
                padding: "5px 20px",
                borderRadius: "5px",
                border: "none",
                backgroundColor: "#ab7d58",
                color: "white",
                cursor: "pointer",
              }} 
            >
              Next Chip
            </button>
          </form>

        </div>)}

        {unknownChips === 0 && (<div style={{ display: "flex", justifyContent: "center", alignItems: "center", flexDirection: "column", margin: "20px" }}>
          <button type="button" onClick={sendChipInfo} 
            style={{
              marginTop: "0",
                  padding: "10px 20px",
                  borderRadius: "5px",
                  border: "none",
                  backgroundColor: "#ab7d58",
                  color: "white",
                  cursor: "pointer",
            }}
          >
            Submit
          </button>
        
        </div>)} 
            <button
              onClick={changePhoto}
              style={{
                padding: "10px 20px",
                borderRadius: "5px",
                border: "none",
                backgroundColor: "#ab7d58",
                color: "white",
                cursor: "pointer",
              }}
            >
              Change Photo
            </button>
          </div>
      )}
      
    </div>
  );
}

export default App;