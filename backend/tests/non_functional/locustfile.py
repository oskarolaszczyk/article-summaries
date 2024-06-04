from locust import HttpUser, TaskSet, task, between
import json
import string
import random

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class AuthBehavior(TaskSet):

    def on_start(self):
        self.username = f"user_{random_string()}"
        self.email = f"{self.username}@example.com"
        self.password = "password123"
        self.register_user()
        self.login()
        
    def on_stop(self):
        super().on_stop()
        self.logout()

    def register_user(self):
        response = self.client.post("/api/auth/register", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })
        assert response.status_code == 201

    def login(self):
        response = self.client.post("/api/auth/login", json={
            "username": self.username,
            "password": self.password
        })
        assert response.status_code == 200
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]

    @task(1)
    def view_protected(self):
        self.client.get("/api/auth/protected", headers={"Authorization": f"Bearer {self.access_token}"})

    def logout(self):
        self.client.post("/api/auth/logout", headers={"Authorization": f"Bearer {self.access_token}"})

class WebsiteUser(HttpUser):
    tasks = [AuthBehavior]
    wait_time = between(1, 5)
