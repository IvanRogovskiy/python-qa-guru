class Server:
    def __init__(self, env):
        self.users_app = {
            "local": "http://localhost:8080"
        }[env]
