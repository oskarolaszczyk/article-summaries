import axios from 'axios';
import { useState } from 'react';
import "../styles/ArticlePanel.css";
import { Button, ButtonGroup, Card, Col, Container, Form, Row, Spinner } from 'react-bootstrap';
import { jsPDF } from "jspdf";
import { AiFillLike, AiFillDislike } from "react-icons/ai";

require("../resources/times-normal.js");


const ArticlePanel = () => {
    const [articleUrl, setArticleUrl] = useState('');
    const [selectedModel, setSelectedModel] = useState('2');
    const [articleTitle, setArticleTitle] = useState('Summary');
    const [generatedSummary, setGeneratedSummary] = useState('');
    const [numSentences, setNumSentences] = useState(10);
    const [isGenerating, setIsGenerating] = useState(false);

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

    const handleModelChange = (event) => {
        setSelectedModel(event.target.value);
    };

    const saveToPDF = () => {
        const pdf = new jsPDF();
        const margin = 10;
        const contentWidth = 210 - 2 * margin;
        // Title
        pdf.setFontSize(16);
        pdf.setFont("times", "bold");
        pdf.text("Generated Summary", 105, 20, null, null, 'center');
        // Url
        pdf.setFontSize(10);
        pdf.setFont("customTimes", "normal");
        pdf.text("Source URL:", margin, 30);
        pdf.setTextColor(40, 23, 173);
        pdf.textWithLink(articleUrl, margin + 25, 30, { url: articleUrl });
        // Summary
        pdf.setTextColor(0, 0, 0);
        pdf.setFontSize(12);
        const lines = pdf.splitTextToSize(generatedSummary, contentWidth);
        pdf.text(lines, margin, 40, { maxWidth: contentWidth, align: "justify" });
        
        pdf.setFontSize(10);
        pdf.text('Page 1', 105, 285, null, null, 'center');
        pdf.save("summary.pdf");
    };

    const fetchArticleContent = async () => {
        if (!articleUrl) return;
        try {
            const response = await axios.get('http://127.0.0.1:8000/article/scrape', {
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
                response = await axios.post("http://127.0.0.1:8000/summary/", {
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
                        <Container className="my-3 d-flex justify-content-between">
                            <ButtonGroup>
                                <Button className="me-1"><AiFillLike /></Button>
                                <Button className="me-1"><AiFillDislike /></Button>
                            </ButtonGroup>
                            <Button onClick={saveToPDF} className="ms-auto">
                                Save to PDF
                            </Button>
                        </Container>

                    </Col>
                </Row>
            </Container>
        </>
    );
};

export default ArticlePanel;
