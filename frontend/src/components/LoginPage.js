import { Button, Container, Form, Nav, Col, Row } from 'react-bootstrap'
import { NavLink } from 'react-router-dom'

export default function LoginPage() {
	return (
		<Container fluid className="d-flex justify-content-center">
			<Form className="px-5 d-flex flex-column my-5 border py-3 justify-content-center">
				<h1 className="text-center mb-5">Log in</h1>
				<Row className="mb-4">
					<Col xs={12} md={3} className="d-flex align-items-center justify-content-end">
						<Form.Label className="me-3 mb-0">Nickname:</Form.Label>
					</Col>
					<Col xs={12} md={9}>
						<Form.Control placeholder="Enter nickname" />
					</Col>
				</Row>
				<Row className="mb-4">
					<Col xs={12} md={3} className="d-flex align-items-center justify-content-end">
						<Form.Label className="me-3 mb-0">Password:</Form.Label>
					</Col>
					<Col xs={12} md={9}>
						<Form.Control type="password" placeholder="Enter password" />
					</Col>
				</Row>
				<Form.Text className="mb-4 text-center">Don't have an account?
					<Nav.Link to="/register" as={NavLink}>
						<span type="button" className="text-primary">Register</span>
					</Nav.Link>
				</Form.Text>
				<Button variant="primary" className="w-auto mx-auto">Submit</Button>
			</Form>
		</Container>
	)
}