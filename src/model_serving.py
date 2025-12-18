from ray import serve
from transformers import pipeline
import requests

serve.start()

@serve.deployment
class Model:
    def __init__(self):
        self.language_model = pipeline(
            "text-generation", model="gpt2", framework="pt")

    def __call__(self, request):
        query = request.query_params["query"]
        return self.language_model(query, max_length=100)

app = Model.bind()
serve.run(app)

query = "What's the meaning of life?"
response = requests.get(
    f"http://localhost:8000/?query={query}"
)
print(response.text)
