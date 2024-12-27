from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import os
import requests

app = FastAPI()

# Remove CORS since we're serving frontend from same origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (if you have any CSS/JS files, put them in a 'static' directory)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at root
@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    '.txt', '.md', '.json', '.csv', '.py', '.js', '.css', '.html', 
    '.yml', '.yaml', '.xml', '.ini', '.conf', '.sh', '.bat'
}

class FolderRequest(BaseModel):
    path: str

class FormatRequest(BaseModel):
    input_text: str
    folder_path: str

@app.post("/load-folder")
async def load_folder(request: FolderRequest):
    folder_path = Path(request.path)
    
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="Invalid folder path")
    
    files = []
    for root, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = Path(root) / filename
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(str(file_path.relative_to(folder_path)))
    
    return {"files": sorted(files)}

@app.post("/format-prompt")
async def format_prompt(request: FormatRequest):
    folder_path = Path(request.folder_path)
    input_text = request.input_text
    
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="Invalid folder path")
    
    # Find all @file_path or @url patterns and replace with contents
    words = input_text.split()
    for i, word in enumerate(words):
        if word.startswith("@"):
            target = word[1:]  # Remove @ symbol
            
            # Check if it's a URL
            if target.startswith(('http://', 'https://')):
                try:
                    response = requests.get(target, timeout=10)
                    response.raise_for_status()  # Raise exception for bad status codes
                    content = response.text
                    words[i] = f"\n<web_page>#{target}\n{content}\n</web_page>\n"
                except requests.RequestException as e:
                    raise HTTPException(status_code=400, detail=f"Error fetching URL {target}: {str(e)}")
            else:
                # Handle local file (existing functionality)
                full_path = folder_path / target
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        words[i] = f"\n<file>#{target}\n{content}\n</file>\n"
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Error reading file {target}: {str(e)}")
    
    return {"formatted_text": " ".join(words)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 