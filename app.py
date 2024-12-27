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

def get_ignored_patterns(folder_path: Path) -> set:
    """Get patterns to ignore from .gitignore and add common ignore patterns."""
    ignore_patterns = {
        '.git/', '__pycache__/', 'node_modules/',  # Common VCS and cache dirs
        '*.pyc', '*.pyo', '*.pyd',                 # Python cache files
        '.env/', 'venv/', '.venv/',                # Python virtual environments
        '.DS_Store', 'Thumbs.db',                  # OS-specific files
        '.idea/', '.vscode/',                      # IDE directories
        'target/', 'build/', 'dist/',              # Build directories
        '*.class', '*.jar',                        # Java
        'bin/', 'obj/',                            # C#/.NET
        'vendor/',                                 # PHP/Ruby
    }
    
    gitignore_path = folder_path / '.gitignore'
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    ignore_patterns.add(line)
    
    return ignore_patterns

def should_ignore_path(path: str, ignore_patterns: set) -> bool:
    """Check if a path should be ignored based on ignore patterns."""
    path_parts = Path(path).parts
    
    for pattern in ignore_patterns:
        # Remove trailing slash if present
        pattern = pattern.rstrip('/')
        
        if pattern.startswith('*'):
            # Handle patterns like *.pyc
            if path.endswith(pattern[1:]):
                return True
        elif pattern.endswith('*'):
            # Handle patterns like .idea/*
            prefix = pattern[:-1]
            if any(str(Path(*path_parts[:i])) == prefix 
                  for i in range(1, len(path_parts) + 1)):
                return True
        else:
            # Handle exact matches and directory patterns
            if pattern in path_parts or pattern == path:
                return True
    
    return False

def get_folder_structure(folder_path: Path) -> str:
    """Generate a formatted string of all files in the given folder, excluding ignored files."""
    ignore_patterns = get_ignored_patterns(folder_path)
    files = []
    
    for root, dirs, filenames in os.walk(folder_path):
        # Remove ignored directories to prevent walking into them
        dirs[:] = [d for d in dirs if not should_ignore_path(d, ignore_patterns)]
        
        for filename in filenames:
            file_path = Path(root) / filename
            rel_path = str(file_path.relative_to(folder_path))
            
            if not should_ignore_path(rel_path, ignore_patterns):
                files.append(rel_path)
    
    content = "\n".join(sorted(files))
    return f"\n<folder_structure>\n{content}\n</folder_structure>\n"

def fetch_url_content(url: str) -> str:
    """Fetch and format content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return f"\n<web_page>#{url}\n{response.text}\n</web_page>\n"
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL {url}: {str(e)}")

def read_local_file(folder_path: Path, file_path: str) -> str:
    """Read and format content from a local file."""
    full_path = folder_path / file_path
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return f"\n<file>#{file_path}\n{content}\n</file>\n"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file {file_path}: {str(e)}")

def process_target(folder_path: Path, target: str) -> str:
    """Process a target (folder_structure, URL, or local file) and return formatted content."""
    if target == "folder_structure":
        return get_folder_structure(folder_path)
    
    if target.startswith(('http://', 'https://')):
        return fetch_url_content(target)
    
    return read_local_file(folder_path, target)

@app.post("/format-prompt")
async def format_prompt(request: FormatRequest):
    folder_path = Path(request.folder_path)
    input_text = request.input_text
    
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=400, detail="Invalid folder path")
    
    words = input_text.split()
    for i, word in enumerate(words):
        if word.startswith("@"):
            target = word[1:]  # Remove @ symbol
            words[i] = process_target(folder_path, target)
    
    return {"formatted_text": " ".join(words)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000) 