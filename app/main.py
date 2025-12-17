import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import HTTPException
from app.assistant import Assistant

# Set up logging
log = logging.getLogger("uvicorn.error")

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class AppServer:
    def __init__(self):
        self.app = FastAPI()
        self.images_dir = "static/images"
        self.templates = Jinja2Templates(directory="app/templates")
        self.assistant = Assistant()
        self.setup_routes()

    def setup_routes(self):

        @self.app.get("/", response_class=HTMLResponse)
        async def read_index(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.app.get("/images/favicon.png")
        async def get_favicon():
            favicon_path = os.path.join(os.path.dirname(__file__), f"{self.images_dir}/favicon-32x32.png")
            if os.path.isfile(favicon_path):
                return FileResponse(favicon_path, media_type="image/png")
            return {"error": "Favicon not found"}

        @self.app.post("/process")
        async def process_request(request: Request):
            try:
                body = await request.json()
                prompt = body.get('prompt')
                if not prompt:
                    raise HTTPException(status_code=400, detail="Prompt is required.")
                response = await self.process(prompt)
                return {"response": response}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e)) from e

    async def process(self, prompt: str) -> str:
        return await self.assistant.chat(prompt)

# Create an instance of the AppServer class to run the app
app_server = AppServer()
app = app_server.app  # Expose the FastAPI app for running
