import axios from 'axios';
import React, { useContext, useState } from 'react';
import { Button, Col, Container, Form, FormGroup, Nav, Row } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';
import { AuthContext } from './AuthContext';

export default function RegisterPage() {
	const { login } = useContext(AuthContext);
	const [username, setUsername] = useState('');
	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');

	const handleRegister = async (event) => {
		event.preventDefault();
		try {
			const response = await axios.post('http://127.0.0.1:8000/auth/register', {
				username,
				email,
				password
			});

			const { access_token, refresh_token, user } = response.data;
			login(user, access_token, refresh_token);
			window.location.href = "/";
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<Container fluid className="d-flex justify-content-center">
			<Form className="px-5 d-flex flex-column my-5 border py-3 justify-content-center" onSubmit={handleRegister}>
				<h1 className="text-center mb-5">Register</h1>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">Email:</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control placeholder="Enter email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
					</Col>
				</FormGroup>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">Nickname:</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control placeholder="Enter nickname" type="text" value={username} onChange={e => setUsername(e.target.value)} />
					</Col>
				</FormGroup>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">Password:</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control type="password" placeholder="Enter password" value={password} onChange={e => setPassword(e.target.value)} />
					</Col>
				</FormGroup>
				<Form.Text className="mb-4 text-center">Already have an account?
					<Nav.Link to="/login" as={NavLink}>
						<span type="button" className="text-primary"> Login</span>
					</Nav.Link>
				</Form.Text>
				<Button type="submit" variant="primary" className="w-auto mx-auto">Submit</Button>
			</Form>
		</Container>
	)
}