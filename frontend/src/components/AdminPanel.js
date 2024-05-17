import { Accordion, Button, Card, Col, Container, Form, Row, Table } from 'react-bootstrap';
import { useEffect, useState } from 'react';
import axios from 'axios';

const AdminPanel = () => {
  const [manageUsers, setManageUsers] = useState(false);
  const [showArticles, setShowArticles] = useState(false);
  const [users, setUsers] = useState([]);
  const [articles, setArticles] = useState([]);

  const handleSwitch = (choice) => {
    if (choice === 'users') {
      setManageUsers(true);
      setShowArticles(false);
    } else {
      setShowArticles(true);
      setManageUsers(false);
    }
  }

  const fetchAllData = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/admin/users');
        setUsers(response.data);
    } catch (error) {
        console.error('Error fetching users: ', error);
    }
    try {
        const response = await axios.get('http://127.0.0.1:8000/admin/articles');
        setArticles(response.data);
    } catch (error) {
        console.error('Error fetching articles: ', error);
    }
};

useEffect(() => {
  fetchAllData();
}, []);

  return (
    <Container fluid className="d-flex mx-0">
      <Row className="container-fluid">
        <Col md={2}>
          <Card className="profile-box" style={{ padding: 0 }}>
            <Card.Body>
              <Card.Text onClick={() => handleSwitch('users')} style={{ cursor: 'pointer' }}>Manage users</Card.Text>
              <Card.Text onClick={() => handleSwitch('articles')} style={{ cursor: 'pointer' }}>Show articles</Card.Text>
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
                      <td>{user.created_on}</td>
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
                    <th>Title</th>
                    <th>Source URL</th>
                    <th>Date Added</th>
                  </tr>
                </thead>
                <tbody>
                  {articles.map(article => (
                    <tr key={article.id}>
                      <td>{article.id}</td>
                      <td>{article.title}</td>
                      <td><a href={article.source_url} target="_blank" rel="noopener noreferrer">{article.source_url}</a></td>
                      <td>{article.date_added}</td>
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
