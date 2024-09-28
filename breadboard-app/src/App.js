import React, { useState } from "react";
import ImageUploading from "react-images-uploading";
import { IoMdPhotos } from "react-icons/io";
import './fonts/superbakery.ttf';
function App() {
  const [images, setImages] = useState([]);

  const onChange = (imageList) => {
    setImages(imageList); // Update state with the new image list
  };

  const imageUpload = () => {
    if (images.length > 0) {
      const fd = new FormData();
      fd.append("image", images[0].file); // Use the first image in the array

      fetch("/image", {
        method: "POST",
        body: fd,
      })
        .then((result) => result.json())
        .then((data) => console.log(data)); // log result
    }
  };


  return (
    <div>
      <div
        className="superbakery"
        style={{
          marginTop: "10px",
          fontSize: "50px",
          maxWidth: "1000px",
          margin: "0 auto",
          textAlign: "center",
          marginBottom: "-10px"
        }}
      >
        BreadBoard Bakery
      </div>
      <p style={{ textAlign: "center", padding: "5px", marginBottom: "15px" }}>
        Add your breadboard image to our bakery! <br /> We'll analyze it and give you a
        freshly baked schematic!
      </p>
      <div style={{ maxWidth: "500px", margin: "0 auto", textAlign: "center" }}>
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
                  <div>Browse or Drop Image</div>
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
            backgroundColor: "#f4c089",
            color: "white",
            cursor: "pointer",
          }}
        >
          Upload
        </button>
      </div>
    </div>
  );
}

export default App;
