import { Container, Row, Col, Button } from 'react-bootstrap';
import '../styles/MainPage.css';

const MainPage = () => {
  return (
    <Container className="main-page">
      <Row className="justify-content-center">
        <Col xs={12} className="p-0">
            <div className="banner-image">
            </div>
        </Col>
      </Row>
      <Row className="justify-content-center">
        <Col xs={12} md={8}>
          <h1>Welcome to Article Summaries</h1>
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vel
            risus eget mauris dignissim consectetur. Integer aliquet tellus
            eget feugiat ullamcorper.
          </p>
          <Button variant="primary">Get Started</Button>
        </Col>
      </Row>
    </Container>
  );
};

export default MainPage;