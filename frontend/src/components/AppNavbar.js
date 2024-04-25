import React, { useContext } from "react";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import { NavLink } from 'react-router-dom';
import generateLogo from "../resources/generate.svg";
import logiInLogo from "../resources/logIn.svg";
import logo from "../resources/logo.svg";
import profileLogo from "../resources/profile.svg";
import "../styles/AppNavbar.css";
import { AuthContext } from "./AuthContext";

export default function AppNavbar() {
  const { isLoggedIn } = useContext(AuthContext);

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
                  alt="article paper"
                  src={generateLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
                <span className="mx-3 nav-link-text">Generate Summary</span>
              </div>
            </Nav.Link>
            <Nav.Link className="mx-4 nav-link" to="/profile" as={NavLink} activeclassname="active">
              <div className="d-flex align-items-center">
                <img
                  alt="article paper"
                  src={profileLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
              <span className="mx-3 nav-link-text">Profile</span>
              </div>
            </Nav.Link>
            <Nav.Link className="mx-4 nav-link" to="/admin" as={NavLink} activeclassname="active">
              <div className="d-flex align-items-center">
                <img
                  alt="article paper"
                  src={profileLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
              <span className="mx-3 nav-link-text">Admin</span>
              </div>
            </Nav.Link>
            <Nav.Link className="mx-4 nav-link" to="/login" as={NavLink} activeclassname="active">
              <div className="d-flex align-items-center">
                <img
                  alt="article paper"
                  src={logiInLogo}
                  width="58"
                  height="58"
                  className="d-inline-block icon-container"
                />
                {isLoggedIn ? (
                  <span className="mx-3 nav-link-text">Log Out</span>
                ) : (
                  <span className="mx-3 nav-link-text">Log In</span>
                )}
              </div>
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
  )
}
