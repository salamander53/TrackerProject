import React from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import "./App.css";
import Login from "./component/Login/Login";
import Register from "./component/Register";
import ProtectedRoute from "./component/ProtectedRoutes";
import PasswordReset from "./component/PasswordReset";
import PasswordResetRequest from "./component/PasswordResetRequest";
import SideNavigation from "./component/SideNav/nav";
import Home from "./component/Home/home";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/dist/js/bootstrap.bundle.js";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap-icons/font/bootstrap-icons.css";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import ErrorBoundary from "./component/error";
function App() {
  const location = useLocation();
  const noNavbar =
    location.pathname === "/register" || location.pathname === "/" || location.pathname.includes("password")
  return (
    <>
      <ToastContainer />
      {noNavbar ? 
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/request/password_reset" element={<PasswordResetRequest />} />
          <Route path="/password-reset/:token" element={<PasswordReset />} />
        </Routes>
        : 
        <SideNavigation
          content={
            <Routes>
              <Route element={<ProtectedRoute />}>
                <Route path="/home" element={<Home />} />
              </Route>
            </Routes>
          }
        />
      }
    </>
  );
}

export default App;
