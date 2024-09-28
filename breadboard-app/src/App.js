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
        });
    }
  };

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

      {appState === "identifyChips" && (
        <>
          <div
            style={{
              marginTop: "20px",
              maxWidth: "500px",
              margin: "0 auto",
              textAlign: "center",
              padding: "20px",
              borderRadius: "10px",
              backgroundColor: "#ffffff",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              border: "2px dashed #ccc",
            }}
          >
            <h3 style={{ fontSize: "18px", color: "#524f4f" }}>
              Cropped Image:
            </h3>
            <div
              style={{
                padding: "20px",
                borderRadius: "10px",
                backgroundColor: "#ffffff",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <img
                src={croppedImageUrl}
                alt="Cropped"
                style={{
                  maxWidth: "100%",
                  maxHeight: "300px",
                  borderRadius: "10px",
                  marginTop: "10px",
                }}
              />
            </div>
          </div>

          <div
            style={{
              textAlign: "center",
              marginTop: "20px",
            }}
          >
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
        </>
      )}
    </div>
  );
}

export default App;
