import { useState } from 'react';
import "../styles/ArticlePanel.css";
import { Button, ButtonGroup, Card, Col, Container, Form, Row } from 'react-bootstrap';
import { AiFillLike } from "react-icons/ai";
import { AiFillDislike } from "react-icons/ai";
import { IoIosRefresh } from "react-icons/io";



const ArticlePanel = () => {
    const [articleUrl, setArticleUrl] = useState('');
    const [selectedModel, setSelectedModel] = useState('');
    const [generatedSummary, setGeneratedSummary] = useState('');
    const [numSentences, setNumSentences] = useState(10);

    const handleRating = (rating) => {
        // Logic to handle summary rating (good/bad)
        // Optionally, regenerate the summary
    };

    const handleNumSentences = (event) => {
        const val = event.target.value;
        if (/^[0-9]*$/.test(val)) setNumSentences(val);
    };

    const handleUrlChange = (event) => {
        setArticleUrl(event.target.value);
    };

    const fetchArticle = async () => {
        try {
            console.log(articleUrl);
            const response = await fetch(articleUrl, {
                method: 'GET',
                headers: {
                    'Origin': 'http://localhost:3000',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            console.log(response);
            const data = await response.text();
            console.log(data);
            return data;
        } catch (error) {
            console.error('Error fetching article: ', error);
        }
    };

    const generateSummary = async (articleText) => {
        const formdata = new FormData();
        formdata.append("key", "6ab8b38872f2bdf4f12b0c9476ffbe8c");
        formdata.append("txt", articleText);
        formdata.append("sentences", numSentences);

        const requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow'
        };

        try {
            const response = await fetch("https://api.meaningcloud.com/summarization-1.0", requestOptions);
            const json = await response.json();
            setGeneratedSummary(json.summary);
        } catch (error) {
            console.log('error', error);
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        const articleText = await fetchArticle();
        if (articleText) {
            const parser = new DOMParser();
            const doc = parser.parseFromString(articleText, "text/html");
            const text = doc.querySelector('main').textContent;
            await generateSummary(text.replace(/<[^>]+>/gi, '').replace(/[^\ ]+:\/\/[^\ ]+/gi, ''));
        }
    };

    return (
        <>
            <Container fluid className="d-flex mx-0">
                <Row className="container-fluid py-4" >
                    <Col lg={4}>
                        <Form onSubmit={handleSubmit}>
                            <Form.Group className="my-4">
                                <Form.Label>Article URL: </Form.Label>
                                <Form.Control
                                    type="url"
                                    placeholder="URL"
                                    value={articleUrl}
                                    onChange={handleUrlChange}
                                />
                            </Form.Group>
                            <Form.Group className="my-4">
                                <Form.Label>Select AI model: </Form.Label>
                                <Form.Select aria-label="Default select example">
                                    <option>Open this select menu</option>
                                    <option value="1">Option 1</option>
                                    <option value="2">Option 2</option>
                                </Form.Select>
                            </Form.Group>
                            <Form.Group className="my-4">
                                <Form.Label>Number of sentences: </Form.Label>
                                <Form.Control
                                    type="text"
                                    placeholder="e.g. 5"
                                    value={numSentences}
                                    onChange={handleNumSentences}
                                />
                            </Form.Group>
                            <Button type="submit" className="my-4">Generate summary</Button>
                        </Form>
                    </Col>
                    <Col lg={8}>
                        <Container>
                            <Card>
                                <Card.Title className="display-5 mx-3">Summary</Card.Title>
                                <hr />
                                <Card.Text className="summary-box px-3 my-3 fs-5">
                                    {generatedSummary}
                                </Card.Text>
                            </Card>
                        </Container>
                        <Container className="my-3">
                            <Form.Label className="my-0 me-3 fs-4">Rate summary: </Form.Label>
                            <ButtonGroup>
                                <Button className="me-1"><AiFillLike /></Button>
                                <Button className="me-1"><AiFillDislike /></Button>
                                <Button className="me-1"><IoIosRefresh /></Button>
                            </ButtonGroup>
                        </Container>

                    </Col>
                </Row>
            </Container>
            {/* {generatedSummary && (
                <div className="summary">
                    <h3>Generated Summary:</h3>
                    <p>{generatedSummary}</p>
                    <div className="rating-buttons">
                        <button onClick={() => handleRating('good')}>Good</button>
                        <button onClick={() => handleRating('bad')}>Bad</button>
                    </div>
                    <button onClick={handleSubmit}>Regenerate Summary</button>
                </div>
            )} */}
        </>

    );
};

export default ArticlePanel;
