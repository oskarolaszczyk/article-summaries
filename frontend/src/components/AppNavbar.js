import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import { NavLink } from 'react-router-dom';
import "../styles/AppNavbar.css";
import logo from "../resources/logo.svg";
import generateLogo from "../resources/generate.svg";
import profileLogo from "../resources/profile.svg";
import logiInLogo from "../resources/logIn.svg";

export default function AppNavbar() {
  return (
    <>
      <Navbar className="navbar">
        <Navbar.Brand className="mx-4" href="/">
          <div className="d-flex align-items-center">
            <img
              alt="article paper"
              src={logo}
              width="58"
              height="58"
              className="d-inline-block"
            />
            <Nav.Link to="/" as={NavLink} className="nav-link" activeClassName="active" style={{ marginLeft: '5px' }}>
              <span className="nav-link-text">Article Summaries</span>
            </Nav.Link>
          </div>
        </Navbar.Brand>
        <Nav className="container-fluid mx-3">
          <Nav.Link className="mx-4 nav-link" to="/article_panel" as={NavLink} activeClassName="active">
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
          <Nav.Link className="mx-4 nav-link" to="/profile" as={NavLink} activeClassName="active">
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
          <Nav.Link className="ms-auto nav-link d-flex align-items-center" to="/login" as={NavLink} activeClassName="active">
            <div className="d-flex align-items-center">
              <span className="mx-3 nav-link-text">Log In</span>
              <img
                alt="article paper"
                src={logiInLogo}
                width="58"
                height="58"
                className="d-inline-block icon-container"
              />
            </div>
          </Nav.Link>
        </Nav>
      </Navbar>
    </>
  )
}
