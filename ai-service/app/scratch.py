class DemoProvider:
    def __init__(self, value="test"):
        self.name = value

    def investigate(self, title):
        return {
            "title": title,
            "name": self.name
        }


class DemoService:
    def __init__(self, provider: DemoProvider):
        self.provider = provider

    def run(self, title):
        return self.provider.investigate(title)
