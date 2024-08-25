from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def get_request(self):
        self.client.get("/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Adjust the wait time between requests

