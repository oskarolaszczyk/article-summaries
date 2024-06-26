import React, { useContext } from "react";
import { Nav, Navbar } from 'react-bootstrap';
import { NavLink, useNavigate } from 'react-router-dom';
import axiosInstance from '../api/axiosInstance';
import generateLogo from "../resources/generate.svg";
import logiInLogo from "../resources/logIn.svg";
import logo from "../resources/logo.svg";
import profileLogo from "../resources/profile.svg";
import "../styles/AppNavbar.css";
import { AuthContext } from "./AuthContext";
import { useToast } from "./ToastProvider";

export default function AppNavbar() {
  const navigate = useNavigate();
  const showToast = useToast();
  const { isLoggedIn, isAdmin, logout } = useContext(AuthContext);
  const handleLogout = async () => {
    try {
			await axiosInstance.post("/auth/logout");
      logout();
      showToast('Logged out successfully.', 'success');
      navigate('/login');
		} catch (error) {
      showToast(error, 'danger');
			console.error(error);
		}

  };

  return (
      <Navbar expand="lg" className="navbar">
        <Navbar.Brand>
          <Nav.Link to="/" as={NavLink} className="nav-link ms-2" activeclassname="active">
            <div className="d-flex align-items-center">
              <img
                alt="article paper"
                src={logo}
                width="58"
                height="58"
                className="d-inline-block"
              />
              <span className="mx-3 nav-link-text">Article Summaries</span>
            </div>
          </Nav.Link>
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="navbar-nav" />
        <Navbar.Collapse id="navbar-nav">
          <Nav className="container-fluid mx-3">
            <Nav.Link className="mx-4 nav-link" to="/article_panel" as={NavLink} activeclassname="active">
              <div className="d-flex align-items-center">
                <img
                  alt="writing on paper"
                  src={generateLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
                <span className="mx-3 nav-link-text">Generate Summary</span>
              </div>
            </Nav.Link>
            {isLoggedIn &&
            <Nav.Link className="mx-4 nav-link" to="/profile" as={NavLink} activeclassname="active">
              <div className="d-flex align-items-center">
                <img
                  alt="user"
                  src={profileLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
              <span className="mx-3 nav-link-text">Profile</span>
              </div>
            </Nav.Link>
            }
            {isAdmin &&
              <Nav.Link className="mx-4 nav-link" to="/admin" as={NavLink} activeclassname="active">
                <div className="d-flex align-items-center">
                  <img
                    alt="admin"
                    src={profileLogo}
                    width="58"
                    height="58"
                    className="d-inline-block icon-container"
                  />
                <span className="mx-3 nav-link-text">Admin</span>
                </div>
              </Nav.Link>
            }
            <Nav.Link 
              className="mx-4 nav-link" 
              to="/login" 
              as={NavLink} 
              activeclassname="active" 
              onClick={isLoggedIn ? handleLogout : null}
            >
              <div className="d-flex align-items-center">
                <img
                  alt="log in or log out"
                  src={logiInLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
                <span className="mx-3 nav-link-text">
                  {isLoggedIn ? 'Log Out' : 'Log In'}
                </span>
              </div>
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
  )
}
