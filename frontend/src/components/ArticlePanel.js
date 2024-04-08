import { useState } from 'react';
import "../styles/ArticlePanel.css";
import { Button, ButtonGroup, Card, Col, Container, Form, Row } from 'react-bootstrap';
import { AiFillLike } from "react-icons/ai";
import { AiFillDislike } from "react-icons/ai";



const ArticlePanel = () => {
    const [articleUrl, setArticleUrl] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [generatedSummary, setGeneratedSummary] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // Perform summary generation logic based on articleUrl and selectedModel
        // Update generatedSummary state
    };

    const handleRating = (rating) => {
        // Logic to handle summary rating (good/bad)
        // Optionally, regenerate the summary
    };

    return (
        <>
            <Container fluid className="d-flex mx-0">
                <Row className="container-fluid py-4" >
                    <Col lg={4}>
                        <Form>
                            <Form.Group className="my-4">
                                <Form.Label>Article URL: </Form.Label>
                                <Form.Control placeholder="URL" />
                            </Form.Group>
                            <Form.Group className="my-4">
                                <Form.Label>Select AI model: </Form.Label>
                                <Form.Select aria-label="Default select example">
                                    <option>Open this select menu</option>
                                    <option value="1">Option 1</option>
                                    <option value="2">Option 2</option>
                                </Form.Select>
                            </Form.Group>
                            <Button className="my-4">Generate summary</Button>
                        </Form>
                    </Col>
                    <Col lg={8}>
                        <Container>
                            <Card>
                                <Card.Title className="display-5 mx-3">Summary</Card.Title>
                                <hr />
                                <Card.Text className="summary-box px-3 my-3 fs-5">
                                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                                    eiusmod tempor incididunt ut labore et dolore magna aliqua.
                                </Card.Text>

                            </Card>
                        </Container>
                        <Container className="my-3">
                            <Form.Label className="my-0 me-3 fs-4">Rate summary: </Form.Label>
                            <ButtonGroup>
                                <Button><AiFillLike /></Button>
                                <Button><AiFillDislike /></Button>
                            </ButtonGroup>
                        </Container>

                    </Col>
                </Row>
            </Container>
            {generatedSummary && (
                <div className="summary">
                    <h3>Generated Summary:</h3>
                    <p>{generatedSummary}</p>
                    <div className="rating-buttons">
                        <button onClick={() => handleRating('good')}>Good</button>
                        <button onClick={() => handleRating('bad')}>Bad</button>
                    </div>
                    <button onClick={handleSubmit}>Regenerate Summary</button>
                </div>
            )}
        </>

    );
};

export default ArticlePanel;
