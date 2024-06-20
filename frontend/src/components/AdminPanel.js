import { Card, Col, Container, Row, Table } from 'react-bootstrap';
import { useContext, useEffect, useState } from 'react';
import axiosInstance from '../api/axiosInstance';
import { AuthContext } from "./AuthContext";

const AdminPanel = () => {
  const { isAdmin } = useContext(AuthContext);
  const [manageUsers, setManageUsers] = useState(false);
  const [showArticles, setShowArticles] = useState(false);
  const [showSummaries, setShowSummaries] = useState(false);
  const [users, setUsers] = useState([]);
  const [articles, setArticles] = useState([]);
  const [summaries, setSummaries] = useState([]);


  const handleSwitch = (choice) => {
    if (choice === 'users') {
      setManageUsers(true);
      setShowArticles(false);
      setShowSummaries(false);
    } else if (choice === 'articles') {
      setShowArticles(true);
      setManageUsers(false);
      setShowSummaries(false);
    } else {
      setShowSummaries(true);
      setShowArticles(false);
      setManageUsers(false);
    }
  }

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const response = await axiosInstance.get('http://127.0.0.1:5000/admin/users', {
          params: { isAdmin: isAdmin }
        });
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users: ', error);
      }
      try {
        const response = await axiosInstance.get('http://127.0.0.1:5000/admin/articles', {
          params: { isAdmin: isAdmin }
        });
        setArticles(response.data);
      } catch (error) {
        console.error('Error fetching articles: ', error);
      }
      try {
        const response = await axiosInstance.get('http://127.0.0.1:5000/admin/summaries', {
          params: { isAdmin: isAdmin }
        });
        setSummaries(response.data);
      } catch (error) {
        console.error('Error fetching summaries: ', error);
      }
    };
    fetchAllData();
  }, [isAdmin]);

  return (
    <Container fluid className="d-flex mx-0">
      <Row className="container-fluid">
        <Col md={2}>
          <Card className="profile-box" style={{ padding: 0 }}>
            <Card.Body>
              <Card.Text onClick={() => handleSwitch('users')} style={{ cursor: 'pointer' }}>Manage users</Card.Text>
              <Card.Text onClick={() => handleSwitch('articles')} style={{ cursor: 'pointer' }}>Show articles</Card.Text>
              <Card.Text onClick={() => handleSwitch('summaries')} style={{ cursor: 'pointer' }}>Show summaries</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={10}>
          {manageUsers && users.length > 0 && (
            <div>
              <h3 style={{ marginTop: 10 }}>Users List</h3>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Type</th>
                    <th>Created On</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(user => (
                    <tr key={user.id}>
                      <td>{user.id}</td>
                      <td>{user.username}</td>
                      <td>{user.email}</td>
                      <td>{user.type}</td>
                      <td>{new Date(user.created_on).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}

          {showArticles && articles.length > 0 && (
            <div>
              <h3 style={{ marginTop: 10 }}>Articles List</h3>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>User ID</th>
                    <th>Title</th>
                    <th>Source URL</th>
                    <th>Date Added</th>
                  </tr>
                </thead>
                <tbody>
                  {articles.map(article => (
                    <tr key={article.id}>
                      <td>{article.id}</td>
                      <td>{article.user_id}</td>
                      <td>{article.title}</td>
                      <td><a href={article.source_url} target="_blank" rel="noopener noreferrer">{article.source_url}</a></td>
                      <td>{new Date(article.date_added).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}

          {showSummaries && summaries.length > 0 && (
            <div>
              <h3 style={{ marginTop: 10 }}>Summaries List</h3>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Article ID</th>
                    <th>Content</th>
                    <th>Rating</th>
                    <th>Model</th>
                    <th>Date Generated</th>
                  </tr>
                </thead>
                <tbody>
                  {summaries.map(summary => (
                    <tr key={summary.id}>
                      <td>{summary.id}</td>
                      <td>{summary.article_id}</td>
                      <td>{summary.content}</td>
                      <td>{summary.rating ? 'Positive' : 'Negative'}</td>
                      <td>{summary.model_type}</td>
                      <td>{new Date(summary.date_generated).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </div>
          )}
        </Col>
      </Row>
    </Container>
  )
}

export default AdminPanel;
