import React, { useState, useEffect } from "react";
import ImageUploading from "react-images-uploading";
import { IoMdPhotos } from "react-icons/io";
import "./fonts/superbakery.ttf";
import "./App.css";

function App() {
  const [images, setImages] = useState([]);
  const [croppedImageUrl, setCroppedImageUrl] = useState(null);
  const [showUploadArea, setShowUploadArea] = useState(true);
  const [schematicImageUrl, setSchematicImageUrl] = useState(null);

  const onChange = (imageList) => {
    setImages(imageList);
  };

  const getCroppedImage = () => {
    fetch("/croppedimage", { method: "GET" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `uh oh Failed to fetch cropped image, status: ${response.status}`
          );
        }
        return response.blob();
      })
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        setCroppedImageUrl(url);
        setShowUploadArea(false);
      })
      .catch((error) => {
        console.error("uh oh Failed to get cropped image:", error);
        alert("Error fetching cropped image. Please try again.");
      });
  };

  const getSchematicImage = () => {
    fetch("/schematic", { method: "GET" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(
            `Failed to fetch schematic image, status: ${response.status}`
          );
        }
        return response.blob();
      })
      .then((blob) => {
        console.log(blob);
        return blob.text();
      })
      .then((text) => {
        console.log(text);
      })
      .catch((error) => {
        console.error("Failed to get schematic image:", error);
        alert("Error fetching schematic image. Please try again.");
      });
  };

  // Cleanup
  useEffect(() => {
    return () => {
      if (schematicImageUrl) {
        URL.revokeObjectURL(schematicImageUrl);
      }
    };
  }, [schematicImageUrl]);

  const imageUpload = () => {
    if (images.length > 0) {
      const fd = new FormData();
      fd.append("image", images[0].file);

      fetch("/image", { method: "POST", body: fd })
        .then((result) => result.json())
        .then((data) => {
          console.log(data);
          getCroppedImage();
          getSchematicImage();
        })
        .catch((error) => {
          console.error("Failed to upload image:", error);
          alert("Error uploading image. Please try again.");
        });
    }
  };

  const changePhoto = () => {
    setImages([]);
    setShowUploadArea(true);
    setCroppedImageUrl(null);
    setSchematicImageUrl(null);
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

      {showUploadArea && (
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

      {!showUploadArea && (
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
            {croppedImageUrl && (
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
            )}
          </div>

          {schematicImageUrl && (
            <div style={{ marginTop: "20px", textAlign: "center" }}>
              <h3 style={{ fontSize: "18px", color: "#524f4f" }}>Schematic:</h3>
              <img
                src={schematicImageUrl}
                style={{
                  maxWidth: "100%",
                  maxHeight: "300px",
                  borderRadius: "10px",
                }}
              />
            </div>
          )}

          <button
            onClick={changePhoto}
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
            Change Photo
          </button>
        </>
      )}
    </div>
  );
}

export default App;
