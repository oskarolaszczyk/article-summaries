import { jsPDF } from "jspdf";
import { Accordion, Button, Col, Container, Form, Row } from 'react-bootstrap'
import { useEffect, useState } from 'react'

import axiosInstance from '../api/axiosInstance';
import "../styles/ProfilePanel.css";

require("../resources/times-normal.js");

export default function ProfilePanel() {
  const [userId, setUserId] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [oldPassword, setOldPassword] = useState('');
  const [articles, setArticles] = useState([]);
  const [summaries, setSummaries] = useState([]);

  useEffect(() => {
    axiosInstance.get('auth/who-am-i').then((res) => {
      const data = res.data
      setUsername(data.username);
      setEmail(data.email);
      setUserId(data.id);
      axiosInstance.get(`http://127.0.0.1:5000/account/${data.id}/articles`)
        .then((res) => {
          setArticles(res.data);
        })
        .catch(error => {
          console.error(error)
        });
    })
    .catch((err) => {
      console.error(err);
    });
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!oldPassword) {
      console.error("Provide old password to update your data");
      return;
    }
    const profile_data = {
      username: username,
      email: email,
      old_password: oldPassword,
      password: newPassword,
    }
    try {
      const response = await axiosInstance.put(`http://127.0.0.1:5000/account/${userId}`, profile_data);
      console.log(response.data.message);
    } catch (error) {
      console.error("Error while updating profile data: ", error);
    }
  };

  const handleAccordionOpen = (articleId) => {
    if(!summaries[articleId]) {
      axiosInstance.get(`http://127.0.0.1:5000/account/summaries/${articleId}`)
        .then((res) => {
        setSummaries(prevSummaries => ({ ...prevSummaries, [articleId]: res.data}));
      })
      .catch(error => {
        console.error(error)
      });
    }
  };

  const saveToPDF = (title, url, content, articleId, summaryId) => {
    const pdf = new jsPDF();
    const margin = 10;
    const contentWidth = 210 - 2 * margin;
    // Title
    pdf.setFontSize(16);
    pdf.setFont("customTimes", "normal");
    pdf.text(title, 105, 20, null, null, 'center');
    // Url
    pdf.setFontSize(10);
    pdf.text("Source URL:", margin, 30);
    pdf.setTextColor(40, 23, 173);
    pdf.textWithLink(url, margin + 25, 30, { url: url });
    // Summary
    pdf.setTextColor(0, 0, 0);
    pdf.setFontSize(12);
    const lines = pdf.splitTextToSize(content, contentWidth);
    pdf.text(lines, margin, 40, { maxWidth: contentWidth, align: "justify" });
    
    pdf.setFontSize(10);
    pdf.text('Page 1', 105, 285, null, null, 'center');
    pdf.save(`summary_a${articleId}_s${summaryId}.pdf`);
  };

  return (
    <Container fluid className="d-flex mx-0">
      <Row className="container-fluid">
        <Col>
          <Container fluid="md" className="d-flex justify-content-center">
            <Form className="profile-box" onSubmit={handleSubmit}>
              <h1 className='title'>Profile settings</h1>
              <Form.Label className="text-start mt-3">Username: </Form.Label>
              <Form.Group className="mb-3 d-flex align-items-center">
                <Form.Control
                  type="text"
                  placeholder="Enter nickname"
                  autoComplete='on'
                  value={username}
                  onChange={(event) => { setUsername(event.target.value) }}
                />
              </Form.Group>
              <Form.Label className="text-start mt-3">Email: </Form.Label>
              <Form.Group className="mb-3 d-flex align-items-center">
                <Form.Control
                  type="email"
                  placeholder="Enter email"
                  autoComplete='on'
                  value={email}
                  onChange={(event) => { setEmail(event.target.value) }}
                />
              </Form.Group>
              <Form.Label className="text-start mt-3">Old Password: </Form.Label>
              <Form.Group className="mb-3 d-flex align-items-center">
                <Form.Control
                  type="password"
                  placeholder="Enter password"
                  autoComplete='off'
                  value={oldPassword}
                  required
                  onChange={(event) => { setOldPassword(event.target.value) }}
                />
              </Form.Group>
              <Form.Label className="text-start mt-3">New Password: </Form.Label>
              <Form.Group className="mb-3 d-flex align-items-center">
                <Form.Control
                  type="password"
                  placeholder="Enter password"
                  autoComplete='off'
                  value={newPassword}
                  onChange={(event) => { setNewPassword(event.target.value) }}
                />
              </Form.Group>
              <div className="text-center">
                <Button type="submit">Save changes</Button>
              </div>
            </Form>
          </Container>
        </Col>
        <Col>
          <Container fluid="md" className="acordeon-box">
            <Accordion className="w-100" defaultActiveKey="0" alwaysOpen>
              {articles.map((article, i) => (
                <Accordion.Item eventKey={i} key={article.id} onClick={() => { handleAccordionOpen(article.id) }}>
                  <Accordion.Header>{article.title}</Accordion.Header>
                  <Accordion.Body className="scrollable-accordion-body">
                    {summaries[article.id] ? (
                      summaries[article.id].map(summary => (
                        <div key={summary.id}>
                          <h5>Summary</h5>
                          <p><strong>Content:</strong> {summary.content}</p>
                          <p><strong>Rating:</strong> {summary.rating ? 'Positive' : 'Negative'}</p>
                          <p><strong>Model:</strong> {summary.model_type}</p>
                          <p><strong>Date Generated:</strong> {new Date(summary.date_generated).toLocaleString()}</p>
                          <Button 
                            onClick={() => saveToPDF(article.title, article.source_url, summary.content, article.id, summary.id)} 
                            className="ms-1"
                          >
                            Save to PDF
                          </Button>
                        </div>
                      ))
                    ) : (
                      <p>Fetching summaries...</p>
                    )}
                  </Accordion.Body>
                </Accordion.Item>
              ))}
            </Accordion>
          </Container>
        </Col>
      </Row>
    </Container>
  )
}