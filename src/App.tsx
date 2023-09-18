import "./fonts/fonts.css";
import React from "react";
import Header from "./components/Header";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Main from "./pages/main";
import Login from "./pages/login";
import Footer from "./components/Footer";
import Register from "./pages/register";
import Premium from "./pages/premium";
import EditAccount from "./pages/edit-account";
import AddCourse from "./pages/add-course";
import EditCourse from "./pages/edit-course";
import Video from "./pages/video";
import Channel from "./pages/channel";
import Error404 from "./pages/404";

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Main />
              </>
            }
          />
          <Route
            path="/login"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Login />
              </>
            }
          />
          <Route
            path="/register"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Register />
              </>
            }
          />
          <Route
            path="/edit-account"
            element={
              <>
                <Header isBurgerMenu={true} />
                <EditAccount />
              </>
            }
          />
          <Route
            path="/add-course"
            element={
              <>
                <Header isBurgerMenu={true} />
                <AddCourse />
              </>
            }
          />
          <Route
            path="/edit-course"
            element={
              <>
                <Header isBurgerMenu={true} />
                <EditCourse />
              </>
            }
          />
          <Route
            path="/premium"
            element={
              <>
                <Header isBurgerMenu={false} />
                <Premium />
              </>
            }
          />
          <Route
            path="/profile"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Channel userId={"ff98f875-e36b-42a1-848a-9ee173cceacc"} />
              </>
            }
          />
          <Route
            path="/channel/:id"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Channel />
              </>
            }
          />

          <Route
            path="/video"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Video />
              </>
            }
          />
          <Route
            path="*"
            element={
              <>
                <Header isBurgerMenu={true} />
                <Error404 />
              </>
            }
          />
        </Routes>
        <Footer />
      </Router>
    </div>
  );
}

export default App;
