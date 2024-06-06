from locust import HttpUser, TaskSet, task, between, SequentialTaskSet
import json
import string
import random

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class AuthBehavior(SequentialTaskSet):

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
        
    @task(2)
    def stop(self):
        self.interrupt()
        
    def logout(self):
        self.client.post("/api/auth/logout", headers={"Authorization": f"Bearer {self.access_token}"})

class SummaryBehavior(SequentialTaskSet):

    @task(1)
    def scrape_article(self):
        url = "https://en.wikipedia.org/wiki/World_War_II"
        with self.client.get(f"/article/scrape?url={url}", catch_response=True) as response:
            if response.status_code == 200 and "title" in response.json() and "content" in response.json():
                response.success()
                self.article_content = response.json().get("content")
            else:
                response.failure("Failed to scrape article")
                
    @task(1)
    def generate_summary(self):
        if not hasattr(self, 'article_content'):
            self.scrape_article()  # Ensure we have the article content

        headers = {"Content-Type": "application/json"}
        data = {
            "txt": self.article_content,
            "sentences": 100
        }
        with self.client.post("/summary/generate", headers=headers, data=json.dumps(data), catch_response=True) as response:
            if response.status_code == 200 and "summary" in response.json():
                response.success()
                self.summary_id = response.json().get("summary_id")
            else:
                response.failure("Failed to generate summary")
    
    @task(2)
    def stop(self):
        self.interrupt()
        
class UserBehaviour(SequentialTaskSet):
    tasks = [AuthBehavior, SummaryBehavior]

class WebsiteUser(HttpUser):
    host = "http://localhost:8000"
    tasks = [UserBehaviour]
    wait_time = between(1, 5)
