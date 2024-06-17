import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { useEffect, useState } from 'react';
import "../styles/ArticlePanel.css";
import { Button, ButtonGroup, Card, Col, Container, Form, Row, Spinner } from 'react-bootstrap';
import { AiFillLike, AiFillDislike } from "react-icons/ai";
import axiosInstance from '../api/axiosInstance.js'

require("../resources/times-normal.js");


const ArticlePanel = () => {
    const [articleUrl, setArticleUrl] = useState('');
    const [selectedModel, setSelectedModel] = useState('2');
    const [articleTitle, setArticleTitle] = useState('Summary');
    const [generatedSummary, setGeneratedSummary] = useState('');
    const [numSentences, setNumSentences] = useState(10);
    const [isGenerating, setIsGenerating] = useState(false);
    const [rating, setRating] = useState(null);
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('accessToken');
        if (token) {
            const decodedToken = jwtDecode(token);
            setUserId(decodedToken.sub);
        }
    }, []);

    const handleNumSentences = (event) => {
        const val = event.target.value;
        if (/^[0-9]*$/.test(val)) setNumSentences(val);
    };

    const handleUrlChange = (event) => {
        setArticleUrl(event.target.value);
    };

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const fetchArticleContent = async () => {
        if (!articleUrl) return;
        try {
            const response = await axios.get('http://127.0.0.1:5000/article/scrape', {
                params: { url: articleUrl }
            });
            const data = response.data
            return data;
        } catch (error) {
            console.error('Error fetching article content: ', error);
        }
    };

    const generateSummary = async (articleText) => {
        try {
            let response;
            if (selectedModel === "1") {
                const formdata = new FormData();
                formdata.append("key", "86794c53debf6b6a67eaf2a93580afd1");
                formdata.append("txt", articleText);
                formdata.append("sentences", numSentences);
                response = await axios.post("https://api.meaningcloud.com/summarization-1.0", formdata, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    txt: articleText,
                    sentences: numSentences
                });
            } else {
                response = await axios.post("http://127.0.0.1:5000/summary/generate", {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    txt: articleText,
                    sentences: numSentences
                });
            }
            const res = await response.data;
            setGeneratedSummary(res.summary || "Summary could not be generated.");

        } catch (error) {
            console.error('Error generating summary:', error);
            setGeneratedSummary("Error generating summary.");
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        setArticleTitle("");
        setGeneratedSummary("");
        setIsGenerating(true);
        const articleData = await fetchArticleContent();
        if (articleData) {
            await generateSummary(articleData.content);
            setArticleTitle(articleData.title);
        }
        setIsGenerating(false);
    };

    const saveSummary = async () => {
        const article = {
            user_id: userId,
            title: articleTitle,
            source_url: articleUrl,
        };

        try {
            const response = await axiosInstance.post('http://127.0.0.1:5000/article/', article);
            console.log(response.data.message);
            const summary = {
                article_id: response.data.article_id,
                content: generatedSummary,
                rating: rating,
                model_type: selectedModel === '1' ? 'MEANINGCLOUD' : 'OUR_MODEL',
            }
            try {
                const res = await axiosInstance.post('http://127.0.0.1:5000/summary/', summary);
                console.log(res.data.message);
            } catch (error) {
                console.error("There was an error while saving the summary!", error);
            }
        } catch (error) {
            console.error("There was an error while saving the article!", error);
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
                                    placeholder="Enter URL"
                                    value={articleUrl}
                                    onChange={handleUrlChange}
                                />
                            </Form.Group>
                            <Form.Group className="my-4">
                                <Form.Label>Select AI model: </Form.Label>
                                <Form.Select 
                                    aria-label="Default select example" 
                                    value={selectedModel}
                                    onChange={handleModelChange}
                                >
                                    <option>Open this select menu</option>
                                    <option value="1">Meaninig Cloud model</option>
                                    <option value="2">Our model</option>
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
                            <div className="text-center">
                                <Button type="submit" className="my-1" disabled={isGenerating}>
                                {isGenerating ? (
                                    <>
                                        <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                                        <span className="ms-3 sr-only">Generating...</span>
                                    </>
                                ) : "Generate summary"}  
                                </Button>
                            </div>
                        </Form>
                    </Col>
                    <Col lg={8}>
                        <Container>
                            <Card>
                                <Card.Title className="display-5 mx-3 text-center">{articleTitle}</Card.Title>
                                <hr />
                                <Card.Text className="summary-box px-3 my-3 fs-5">
                                    {generatedSummary}
                                </Card.Text>
                            </Card>
                        </Container>
                        {userId ?  (
                            <Container className="my-3 d-flex justify-content-between">
                            <ButtonGroup>
                                <Button className="me-1" disabled={generatedSummary === ''} onClick={() => {setRating(true)}}>
                                    <AiFillLike />
                                </Button>
                                <Button className="me-1" disabled={generatedSummary === ''} onClick={() => {setRating(false)}}>
                                    <AiFillDislike />
                                </Button>
                            </ButtonGroup>
                            <Button disabled={rating === null} onClick={saveSummary} className="ms-auto">
                                Save Summary
                            </Button>
                        </Container>
                        ) : <p className="text-center">
                                <strong >Log in to get addidtional features!</strong>
                            </p>}    
                    </Col>
                </Row>
            </Container>
        </>
    );
};

export default ArticlePanel;
