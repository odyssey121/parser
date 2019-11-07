import React, { useState, useEffect } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  useEffect(() => {
    fetch("/api/news").then(response =>
      response.json().then(json => console.log(json))
    );
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>my token {window.token}</p>
      </header>
    </div>
  );
}

export default App;
