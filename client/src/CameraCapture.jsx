import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";
import "./CameraCapture.css";

export default function CameraCapture() {
  const webcamRef = useRef(null);
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState("");

  const capture = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
    setMessage("");
  };

  const sendToServer = async () => {
    if (!image) return;

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload_image", {
        image,
      });
      setMessage(response.data.message);
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.error || "אירעה שגיאה בשרת");
      } else {
        setMessage("לא ניתן להתחבר לשרת");
      }
    }
  };

  return (
    <div className="container">
      <div className="camera-frame">
        <h2 className="title">צילום תמונה</h2>
        {!image ? (
          <>
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              width={400}
              videoConstraints={{
                width: 400,
                height: 300,
                facingMode: "user",
              }}
              className="webcam-container"
            />
            <button className="capture-btn" onClick={capture}>
              צלמי תמונה
            </button>
          </>
        ) : (
          <>
            <div className="image-container">
              <img src={image} alt="Captured" />
            </div>
            <button onClick={sendToServer}>שלחי לעיבוד</button>
            <button onClick={() => setImage(null)}>new picture</button>
          </>
        )}
        {message && <p>{message}</p>}
      </div>
    </div>
  );
}
