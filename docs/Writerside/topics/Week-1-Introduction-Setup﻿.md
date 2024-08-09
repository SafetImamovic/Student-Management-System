# Week 1: Introduction & Setup

## Description

Set up the development environment. Introduction to FastAPI, PostgreSQL, Alembic, and Pydantic.

## Initial Repository Setup

1. Created a new repository on GitHub:

[](https://github.com/SafetImamovic/Student-Management-System)

2. JetBrains Writerside will be used for project documentation.

Writerside generates a static site from markdown files.

This process can be automated using GitHub Actions.

For that, a `.github/workflows` directory was created in the repository root.

Within it a `build-docs.yml` file was created based on [Writersides official docs](https://www.jetbrains.com/help/writerside/deploy-docs-to-github-pages.html) with the following content:

<code-block lang="yaml" collapsible="true" collapsed-title="build-docs.yml" src="https://raw.githubusercontent.com/SafetImamovic/Student-Management-System/main/.github/workflows/build-docs.yml">

</code-block>

This YAML file builds the documentation using Writerside and deploys it to GitHub Pages.
It also runs tests on the documentation to ensure it is correct.

3. Write the initial project `README.md` and `README.bs.md` files.

This is the resulting repository structure:

```
student-management-system (root)
├── .gitignore
├── README.bs.md
├── README.md
├── .github/
│   └── workflows/
│       └── build-docs.yml
└── docs/
    └── Writerside/
```

## FastAPI Project Setup

### Virtual Environment

First, a virtual environment was created using `venv` at project root:

```Bash
python -m venv venv
```

> `venv/` is added to `.gitignore` as we do not want to version control the virtual environment

<procedure>
<step>
To activate the virtual environment from project root:

<tabs>
    <tab id="windows-install" title="Windows">
        <code-block lang="bash">
            venv\Scripts\activate
        </code-block>
    </tab>
    <tab id="macos-install" title="macOS">
        <code-block lang="bash">
            source venv/bin/activate
        </code-block>
    </tab>
</tabs>
</step>
<step>
To deactivate the virtual environment:
<code-block lang="bash">
    deactivate
</code-block>
</step>
</procedure>

### FastAPI Installation

Firstly a new directory called `app/` was created in the project root for a cleaner structure.

```Bash
mkdir app
```

After activating the virtual environment, FastAPI was installed using `pip`:

The process is outlined in the [official FastAPI docs.](https://fastapi.tiangolo.com/#installation)

```Bash
   pip install fastapi[standard]
```

Then running `pip list`:

<code-block lang="bash" collapsible="true" collapsed-title="pip list output">
Package           Version
----------------- --------
annotated-types   0.7.0
anyio             4.4.0
certifi           2024.7.4
click             8.1.7
colorama          0.4.6
dnspython         2.6.1
email_validator   2.2.0
fastapi           0.112.0
fastapi-cli       0.0.5
h11               0.14.0
httpcore          1.0.5
httptools         0.6.1
httpx             0.27.0
idna              3.7
Jinja2            3.1.4
markdown-it-py    3.0.0
MarkupSafe        2.1.5
mdurl             0.1.2
pip               24.0
pydantic          2.8.2
pydantic_core     2.20.1
Pygments          2.18.0
python-dotenv     1.0.1
python-multipart  0.0.9
PyYAML            6.0.2
rich              13.7.1
shellingham       1.5.4
sniffio           1.3.1
starlette         0.37.2
typer             0.12.3
typing_extensions 4.12.2
uvicorn           0.30.5
watchfiles        0.23.0
websockets        12.0
</code-block>

Afterward the requirements are exported to a `requirements.txt` file in the project root:

```Bash
pip freeze > requirements.txt
```

To install the defined requirements run:

```Bash
pip install -r requirements.txt
```

The resulting file structure:

```
student-management-system (root)
├── requirements.txt    # + new file
├── app/                # + new dir
├── .gitignore
├── README.bs.md
├── README.md
├── .github/
│   └── workflows/
│       └── build-docs.yml
└── docs/
    └── Writerside/
```

### Simple 'Hello World' API

Before creating the API, the FastAPI development server was installed the correct `venv` interpreter has to be set:

Because I'm using JetBrains PyCharm, the interpreter was set in the project settings:

<procedure title="" id="">
<step><shortcut>CTRL</shortcut>+<shortcut>ALT</shortcut>+<shortcut>S</shortcut> to open the settings</step>
<step>Under <code>Project Settings</code> then under <code>Project Interpreter</code></step>
<step>There's an option <code>Add Interpreter</code></step>
<step>Under that option press <code>Add Existing</code> and then PyCharm should be able to detect the venv interpreter,
if not it can be manually found:
<code>
venv/Scripts/python.exe
</code></step>
</procedure>

A simple 'Hello World' API was created in `app/main.py` following the [FastAPI docs](https://fastapi.tiangolo.com/#create-it):

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

To run the server the following command is run from project root:

```Bash
fastapi dev app/main.py
```

The console output should have the address and port on which the server is listening:

```Bash
http://127.0.0.1:8000/
```

After visiting this address:

<img src="1.png" />

With that, the simple 'Hello World' API is up and running.

## Issues Encountered

One issue I encountered was accidentally running multiple instances of the server.

This is not an issue with FastAPI but rather my user error.

That would be reflected as the server not restarting after changes were made to the code.

To figure out if this is the case, there's a cmd command that can be run:

```Bash
netstat -ano | findstr :8000
```

This command will show all processes running on port 8000.

If there are multiple instances, the `PID` can be used to kill the process:

```Bash
taskkill /PID <PID> /F
```

Afterward, the server should restart correctly.