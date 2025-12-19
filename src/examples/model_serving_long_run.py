from ray import serve
from transformers import pipeline
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    max_length: int = 100

@serve.deployment
@serve.ingress(app)
class Model:
    def __init__(self):
        self.pipe = pipeline(
            "text-generation",
            model="gpt2",
            framework="pt",
        )

    @app.post("/")
    async def generate(self, req: GenerateRequest):
        out = self.pipe(req.prompt, max_length=req.max_length)
        return {
            "prompt": req.prompt,
            "output": out[0]["generated_text"],
        }

serve.run(Model.bind(), route_prefix="/generate")
