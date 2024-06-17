import React, { useContext, useState } from "react";
import {
	Button,
	Col,
	Container,
	Form,
	FormGroup,
	Nav,
	Row,
} from "react-bootstrap";
import { NavLink } from "react-router-dom";
import axiosInstance from "../api/axiosInstance";
import { AuthContext } from "./AuthContext";

export default function LoginPage() {
	const { login } = useContext(AuthContext);
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");

	const handleLogin = async (event) => {
		event.preventDefault();
		try {
			const response = await axiosInstance.post("/auth/login", {
				username,
				password,
			});
			
			const { access_token, refresh_token , is_admin } = response.data;
			login(access_token, refresh_token, is_admin);
			window.location.href = "/";
		} catch (error) {
			console.error(error);
		}

	};
	

	return (
		<Container fluid className="d-flex justify-content-center">
			<Form
				className="px-5 d-flex flex-column my-5 border py-3 justify-content-center"
				onSubmit={handleLogin}
			>
				<h1 className="text-center mb-5">Log in</h1>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">
						Nickname:
					</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control
							type="text"
							placeholder="Enter nickname"
							value={username}
							onChange={(e) => setUsername(e.target.value)}
						/>
					</Col>
				</FormGroup>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">
						Password:
					</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control
							type="password"
							placeholder="Enter password"
							value={password}
							onChange={(e) => setPassword(e.target.value)}
						/>
					</Col>
				</FormGroup>
				<Form.Text className="mb-4 text-center">
					Don't have an account?
					<Nav.Link to="/register" as={NavLink}>
						<span type="button" className="text-primary">
							Register
						</span>
					</Nav.Link>
				</Form.Text>
				<Button type="submit" variant="primary" className="w-auto mx-auto">
					Submit
				</Button>
			</Form>
		</Container>
	);
}
