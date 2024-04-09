import { Button, Container, Form, FormGroup, Nav, Col, Row } from 'react-bootstrap'
import { NavLink } from 'react-router-dom'

export default function RegisterPage() {
	return (
		<Container fluid className="d-flex justify-content-center">
			<Form className="px-5 d-flex flex-column my-5 border py-3 justify-content-center">
				<h1 className="text-center mb-5">Register</h1>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">Email:</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control placeholder="Enter email" />
					</Col>
				</FormGroup>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">Nickname:</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control placeholder="Enter nickname" />
					</Col>
				</FormGroup>
				<FormGroup as={Row} className="mb-4">
					<Form.Label column sm={2} className="me-5">Password:</Form.Label>
					<Col xs={12} md={8}>
						<Form.Control type="password" placeholder="Enter password" />
					</Col>
				</FormGroup>
				<Form.Text className="mb-4 text-center">Already have an account?
					<Nav.Link to="/login" as={NavLink}>
						<span type="button" className="text-primary"> Login</span>
					</Nav.Link>
				</Form.Text>
				<Button variant="primary" className="w-auto mx-auto">Submit</Button>
			</Form>
		</Container>
	)
}