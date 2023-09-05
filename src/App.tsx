import "./fonts/fonts.css";
import React from "react";
import Header from "./components/Header";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Main from "./styles/pages/main";
import Login from "./styles/pages/login";
import Footer from "./components/Footer";
import Register from "./styles/pages/register";

function App() {
  return (
    <div className="App">
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
