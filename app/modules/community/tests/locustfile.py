from locust import HttpUser, TaskSet, task, between
from core.environment.host import get_host_for_locust_testing


class CommunityBehavior(TaskSet):
    def on_start(self):
        self.client.post("/login", data={
            "email": "user@example.com",
            "password": "test1234"
        })

    @task(1)
    def index(self):
        response = self.client.get("/community")
        if response.status_code != 200:
            print(f"Community index failed: {response.status_code}")

    @task(2)
    def create_community(self):
        response = self.client.post("/community/create", data={
            "name": "Test Community",
            "description": "This is a test community",
            "code": "testcode"
        })
        if response.status_code != 200:
            print(f"Create community failed: {response.status_code}")

    @task(3)
    def join_community(self):
        response = self.client.post("/community/join", data={"joinCode": "testcode"})
        if response.status_code != 200:
            print(f"Join community failed: {response.status_code}")

    @task(4)
    def update_community(self):
        community_id = 1  # Replace with a valid community ID
        response = self.client.post(f"/community/update/{community_id}", data={
            "name": "Updated Community",
            "description": "Updated Description",
            "code": "updatedCode"
        })
        if response.status_code != 200:
            print(f"Update community failed: {response.status_code}")

    @task(5)
    def delete_community(self):
        community_id = 1  # Replace with a valid community ID
        response = self.client.post(f"/community/delete/{community_id}")
        if response.status_code != 200:
            print(f"Delete community failed: {response.status_code}")

    @task(6)
    def leave_community(self):
        community_id = 1  # Replace with a valid community ID
        response = self.client.post(f"/community/leave/{community_id}")
        if response.status_code != 200:
            print(f"Leave community failed: {response.status_code}")

    @task(7)
    def view_community(self):
        community_id = 1  # Replace with a valid community ID
        response = self.client.get(f"/community/{community_id}")
        if response.status_code != 200:
            print(f"View community failed: {response.status_code}")

    def on_stop(self):
        # Logout at the end of each simulated user session
        self.client.get("/logout")


class CommunityUser(HttpUser):
    tasks = [CommunityBehavior]
    wait_time = between(1, 3)
    host = get_host_for_locust_testing()
