class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username, password):
        return self._client.post(
            "/login", json={"username": username, "password": password}
        )

    def logout(self, jwt):
        return self._client.post("/logout", headers={"Authorization": f"Bearer {jwt}"})


class TaskActions(object):
    def __init__(self, client):
        self._client = client

    def create(self, jwt, **kwargs):
        return self._client.post(
            "/tasks/create", json=kwargs, headers={"Authorization": f"Bearer {jwt}"}
        )

    def get_by_id(self, jwt, task_id):
        return self._client.get(
            f"/tasks/{task_id}", headers={"Authorization": f"Bearer {jwt}"}
        )

    def delete_by_id(self, jwt, task_id):
        return self._client.delete(
            f"/tasks/{task_id}", headers={"Authorization": f"Bearer {jwt}"}
        )

    def update_by_id(self, jwt, task_id, **kwargs):
        return self._client.patch(
            f"/tasks/{task_id}", json=kwargs, headers={"Authorization": f"Bearer {jwt}"}
        )

    def select(self, jwt, **kwargs):
        return self._client.get(
            f"/tasks", query_string=kwargs, headers={"Authorization": f"Bearer {jwt}"}
        )
