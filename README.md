# Prompt Formatter

A tool that helps format text by dynamically including file contents from a specified folder or URLs. Perfect for creating prompts or documentation that need to reference multiple files or web resources for GPT/Claude/Gemini or other LLM.

## Features

- Dynamic file content insertion using @file_path syntax
- URL content fetching using @url syntax
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
- TypeScript React files (.tsx)
- Log files (.log)
- Rich Text Format files (.rtf)
- TeX files (.tex)
- AsciiDoc files (.asciidoc, .adoc)
- C/C++ files (.c, .cpp, .cc, .cxx, .h, .hpp, .hxx)
- Java files (.java)
- Ruby files (.rb)
- PHP files (.php)
- Go files (.go)
- Swift files (.swift)
- Rust files (.rs)
- Kotlin files (.kt, .kts)
- TOML files (.toml)
- Environment files (.env)
- TSV files (.tsv)
- SQL files (.sql)
- Z shell scripts (.zsh)
- Fish shell scripts (.fish)
- Perl scripts (.pl)
- AWK scripts (.awk)
- SASS/SCSS files (.scss, .sass)
- LESS files (.less)
- JSX files (.jsx)
- Vue.js files (.vue)

## Prerequisites

- Python 3.7+
- Modern web browser with JavaScript enabled

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Troyanovsky/prompt_formatter.git
cd prompt_formatter
```

2. Install required Python packages:
```bash
pip install fastapi uvicorn
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

### To reference folder structure:
```
@folder_structure
```

The formatter will replace this with:
```
<folder_structure>
[list of all files in the folder and subfolders]
</folder_structure>
```

### To reference a local file:
```
@filename.ext
```

The formatter will replace this with:
```
<file>#filename.ext
[file contents here]
</file>
```

### To reference a URL:
```
@https://example.com/path/to/resource
```

The formatter will replace this with:
```
<web_page>#https://example.com/path/to/resource
[content from URL here]
</web_page>
```

## Example

Input:
```
Here is my Python script: @script.py
Here is a web resource: @https://raw.githubusercontent.com/user/repo/main/example.txt
And here is my config: @config.json
```

Output:
```
Here is my Python script: 
<file>#script.py
def hello():
    print("Hello, World!")
</file>
Here is a web resource:
<web_page>#https://raw.githubusercontent.com/user/repo/main/example.txt
[Content fetched from URL]
</web_page>
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
