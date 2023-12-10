import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

export function TextWidget() {
  const socket = new WebSocket("ws://localhost:8000/ws/message");
  const text = useState("default text");

  // Connection opened
  socket.addEventListener("open", (event) => {
    socket.send("Connection established");
    console.log("Connection established");
  });

  // Listen for messages
  socket.addEventListener("message", (event) => {
    console.log("Message from server ", event.data);
  });

  return (
    <div>
      <div className="animation"></div>
      <div className="text">text</div>
    </div>
  );
}
export function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}
