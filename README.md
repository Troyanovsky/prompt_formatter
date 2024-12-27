# Prompt Formatter

A tool that helps format text by dynamically including file contents from a specified folder. Perfect for creating templates or documentation that need to reference multiple files for GPT/Claude/Gemini or other LLM.

## Features

- Dynamic file content insertion using @file_path syntax
- Auto-completion dropdown for file selection
- Support for multiple text-based file formats
- Preview of formatted output

## Supported File Types

- Text files (.txt)
- Markdown files (.md)
- JSON files (.json)
- CSV files (.csv)
- Python files (.py)
- JavaScript files (.js)
- CSS files (.css)
- HTML files (.html)
- YAML files (.yml, .yaml)
- XML files (.xml)
- Configuration files (.ini, .conf)
- Shell scripts (.sh, .bat)

## Prerequisites

- Python 3.7+
- Modern web browser with JavaScript enabled

## Installation

1. Install required Python packages:
```bash
pip install fastapi uvicorn
```

2. Create the project structure:
```bash
mkdir prompt-formatter
cd prompt-formatter
mkdir static
# Copy app.py and index.html into this directory
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:8000
```

The application will now be available directly through the FastAPI server - no need to open the HTML file separately.

## Syntax

To reference a file in your input:
```
@filename.ext
```

The formatter will replace this with:
```
<file>#filename.ext
[file contents here]
</file>
```

## Example

Input:
```
Here is my Python script: @script.py
And here is my config: @config.json
```

Output:
```
Here is my Python script: 
<file>#script.py
def hello():
    print("Hello, World!")
</file>
And here is my config: 
<file>#config.json
{
    "name": "example",
    "version": "1.0.0"
}
</file>
```

## Security Notes

- The tool only reads files, it does not write or modify any files
- Access is limited to the specified folder and its subfolders
- Only supported file types can be accessed
- File operations are handled server-side with proper error handling

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for any purpose.
