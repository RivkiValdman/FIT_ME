import React, { useState } from 'react';
import './App.css';
import Login from './Login';
import Sign_Up from './Sign_Up';
import CameraCapture from './CameraCapture';

function App() {
  const [page, setPage] = useState("home");

  return (
    <div className="container">
      <h1 className="main-title">Welcome to Fit Me</h1>
      <div className="nav-buttons">
        <button onClick={() => setPage("login")}>connected</button>
        <button onClick={() => setPage("signup")}>new user</button>
        <button onClick={() => setPage("camera")}>open a camera </button>
      </div>

      {page === "login" && <Login />}
      {page === "signup" && <Sign_Up />}
      {page === "camera" && <CameraCapture />}
    </div>
  );
}

export default App;
