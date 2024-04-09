import { Container, Row, Col, Button, Card } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import '../styles/MainPage.css';

const MainPage = () => {
  return (
    <Container fluid className="main-page">
      <Row className="justify-content-center">
        <Col xs={12} className="p-0">
            <div className="banner-image">
              <h1 className="p-5 text-img">Welcome to Article Summaries</h1>
            </div>
        </Col>
      </Row>
      <Row className="justify-content-center main-part">
        <Col xs={12} md={7}>
          <p>
            Our platform helps you to save time by generating summaries of your articles. Whether you're a student, researcher, or professional, our AI-powered tool can assist you in quickly extracting the main points from lengthy texts.
          </p>
        </Col>
      </Row>
      <Row className="picture-section">
        <Col cs={12} md={5} className="p-0">
          <div className="picture-container"></div>
        </Col>
        <Col xs={12} md={7} className="d-flex align-items-center">
          <div className="text-container">
            <Card className="mb-4" style={{ backgroundColor: '#f6fafe' }}>
              <Card.Body className="text-center">
                <p>
                  Save your time by creating a summary of your article!
                </p>
                <Button variant="primary" as={NavLink} to="/article_panel" className="mr-2">Generate Summary</Button>
              </Card.Body>
            </Card>
            <Card style={{ backgroundColor: '#f6fafe' }}>
              <Card.Body className="text-center">
                <p>
                  Don't miss out on the latest updates! Register now and unlock exclusive features.
                </p>
                <Button variant="info" as={NavLink} to="/register" className="mr-2">Register</Button>
              </Card.Body>
            </Card>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default MainPage;