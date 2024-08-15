# Minimize Requirements

## Introduction

The goal of this topic is to minimize the requirements of the project.

This is important because the more requirements a project has, the more time and resources it will take up.

Because `pip install fastapi[standard]` was used to install FastAPI, the project has a lot of dependencies that are not needed for the project.

Current dependencies:
<code-block lang="shell" collapsible="true" collapsed-title="requirements.txt">
alembic==1.13.2
annotated-types==0.7.0
anyio==4.4.0
certifi==2024.7.4
click==8.1.7
colorama==0.4.6
dnspython==2.6.1
email_validator==2.2.0
fastapi==0.112.0
fastapi-cli==0.0.5
greenlet==3.0.3
h11==0.14.0
httpcore==1.0.5
httptools==0.6.1
httpx==0.27.0
idna==3.7
Jinja2==3.1.4
Mako==1.3.5
markdown-it-py==3.0.0
MarkupSafe==2.1.5
mdurl==0.1.2
psycopg2-binary==2.9.9
pydantic==2.8.2
pydantic_core==2.20.1
Pygments==2.18.0
python-dotenv==1.0.1
python-multipart==0.0.9
PyYAML==6.0.2
rich==13.7.1
shellingham==1.5.4
sniffio==1.3.1
SQLAlchemy==2.0.32
starlette==0.37.2
typer==0.12.3
typing_extensions==4.12.2
uvicorn==0.30.5
watchfiles==0.23.0
websockets==12.0
</code-block>   

## Steps

1. **Identify Core Functionality**:
   - Identify the core functionality of the project that is essential for its success.
   - Focus on the features that are necessary for the project to meet its objectives.

   As listed on the [official FastAPI docs](https://fastapi.tiangolo.com/#standard-dependencies),
   the standard dependencies include:
    Used by Pydantic:

    `email_validator` - for email validation.
    
    Used by Starlette:
    
    `httpx` - Required if you want to use the TestClient.
    `jinja2` - Required if you want to use the default template configuration.
    `python-multipart` - Required if you want to support form "parsing", with request.form().
    
    Used by FastAPI / Starlette:
    
    `uvicorn` - for the server that loads and serves your application. This includes uvicorn[standard], which includes some dependencies (e.g. uvloop) needed for high performance serving.
    `fastapi-cli` - to provide the fastapi command.

    To remove all of the dependencies run:
    ```Bash
    pip uninstall -r requirements.txt -y
    ```
    This will remove all the dependencies listed in the `requirements.txt` file.
   
   There is a package called `pip install pipdeptree` that shows the dependency tree of the installed packages and can help identify which packages are not required by others.
   Then running `pipdeptree` will show the dependency tree of the installed packages:

   <code-block lang="bash" collapsed-title="pipdeptree" collapsible="true">
   <![CDATA[
   alembic==1.13.2
   ├── Mako [required: Any, installed: 1.3.5]
   │   └── MarkupSafe [required: >=0.9.2, installed: 2.1.5]
   ├── SQLAlchemy [required: >=1.3.0, installed: 2.0.32]
   │   ├── greenlet [required: !=0.4.17, installed: 3.0.3]
   │   └── typing_extensions [required: >=4.6.0, installed: 4.12.2]
   └── typing_extensions [required: >=4, installed: 4.12.2]
   email_validator==2.2.0
   ├── dnspython [required: >=2.0.0, installed: 2.6.1]
   └── idna [required: >=2.0.0, installed: 3.7]
   fastapi==0.112.0
   ├── pydantic [required: >=1.7.4,<3.0.0,!=2.1.0,!=2.0.1,!=2.0.0,!=1.8.1,!=1.8, installed: 2.8.2]
   │   ├── annotated-types [required: >=0.4.0, installed: 0.7.0]
   │   ├── pydantic_core [required: ==2.20.1, installed: 2.20.1]
   │   │   └── typing_extensions [required: >=4.6.0,!=4.7.0, installed: 4.12.2]
   │   └── typing_extensions [required: >=4.6.1, installed: 4.12.2]
   ├── starlette [required: >=0.37.2,<0.38.0, installed: 0.37.2]
   │   └── anyio [required: >=3.4.0,<5, installed: 4.4.0]
   │       ├── idna [required: >=2.8, installed: 3.7]
   │       └── sniffio [required: >=1.1, installed: 1.3.1]
   └── typing_extensions [required: >=4.8.0, installed: 4.12.2]
   fastapi-cli==0.0.5
   ├── typer [required: >=0.12.3, installed: 0.12.3]
   │   ├── click [required: >=8.0.0, installed: 8.1.7]
   │   │   └── colorama [required: Any, installed: 0.4.6]
   │   ├── rich [required: >=10.11.0, installed: 13.7.1]
   │   │   ├── markdown-it-py [required: >=2.2.0, installed: 3.0.0]
   │   │   │   └── mdurl [required: ~=0.1, installed: 0.1.2]
   │   │   └── Pygments [required: >=2.13.0,<3.0.0, installed: 2.18.0]
   │   ├── shellingham [required: >=1.3.0, installed: 1.5.4]
   │   └── typing_extensions [required: >=3.7.4.3, installed: 4.12.2]
   └── uvicorn [required: >=0.15.0, installed: 0.30.5]
   ├── click [required: >=7.0, installed: 8.1.7]
   │   └── colorama [required: Any, installed: 0.4.6]
   └── h11 [required: >=0.8, installed: 0.14.0]
   httptools==0.6.1
   httpx==0.27.0
   ├── anyio [required: Any, installed: 4.4.0]
   │   ├── idna [required: >=2.8, installed: 3.7]
   │   └── sniffio [required: >=1.1, installed: 1.3.1]
   ├── certifi [required: Any, installed: 2024.7.4]
   ├── httpcore [required: ==1.*, installed: 1.0.5]
   │   ├── certifi [required: Any, installed: 2024.7.4]
   │   └── h11 [required: >=0.13,<0.15, installed: 0.14.0]
   ├── idna [required: Any, installed: 3.7]
   └── sniffio [required: Any, installed: 1.3.1]
   Jinja2==3.1.4
   └── MarkupSafe [required: >=2.0, installed: 2.1.5]
   pipdeptree==2.23.1
   ├── packaging [required: >=23.1, installed: 24.1]
   └── pip [required: >=23.1.2, installed: 24.2]
   psycopg2-binary==2.9.9
   python-dotenv==1.0.1
   python-multipart==0.0.9
   PyYAML==6.0.2
   watchfiles==0.23.0
   └── anyio [required: >=3.0.0, installed: 4.4.0]
   ├── idna [required: >=2.8, installed: 3.7]
   └── sniffio [required: >=1.1, installed: 1.3.1]
   websockets==12.0
   ]]>
   </code-block>

2. By running:
   1. `pip install fastapi`
   2. `pip install fastapi-cli`
   3. `pip install alembic`
   4. `pip install psycopg2-binary`
   
   the project will only have the necessary dependencies for FastAPI to work:

   <code-block lang="shell" collapsible="true" collapsed-title="requirements.txt">
   <![CDATA[
   alembic==1.13.2
   ├── Mako [required: Any, installed: 1.3.5]
   │   └── MarkupSafe [required: >=0.9.2, installed: 2.1.5]
   ├── SQLAlchemy [required: >=1.3.0, installed: 2.0.32]
   │   ├── greenlet [required: !=0.4.17, installed: 3.0.3]
   │   └── typing_extensions [required: >=4.6.0, installed: 4.12.2]
   └── typing_extensions [required: >=4, installed: 4.12.2]
   fastapi==0.112.0
   ├── pydantic [required: >=1.7.4,<3.0.0,!=2.1.0,!=2.0.1,!=2.0.0,!=1.8.1,!=1.8, installed: 2.8.2]
   │   ├── annotated-types [required: >=0.4.0, installed: 0.7.0]
   │   ├── pydantic_core [required: ==2.20.1, installed: 2.20.1]
   │   │   └── typing_extensions [required: >=4.6.0,!=4.7.0, installed: 4.12.2]
   │   └── typing_extensions [required: >=4.6.1, installed: 4.12.2]
   ├── starlette [required: >=0.37.2,<0.38.0, installed: 0.37.2]
   │   └── anyio [required: >=3.4.0,<5, installed: 4.4.0]
   │       ├── idna [required: >=2.8, installed: 3.7]
   │       └── sniffio [required: >=1.1, installed: 1.3.1]
   └── typing_extensions [required: >=4.8.0, installed: 4.12.2]
   fastapi-cli==0.0.5
   ├── typer [required: >=0.12.3, installed: 0.12.3]
   │   ├── click [required: >=8.0.0, installed: 8.1.7]
   │   │   └── colorama [required: Any, installed: 0.4.6]
   │   ├── rich [required: >=10.11.0, installed: 13.7.1]
   │   │   ├── markdown-it-py [required: >=2.2.0, installed: 3.0.0]
   │   │   │   └── mdurl [required: ~=0.1, installed: 0.1.2]
   │   │   └── Pygments [required: >=2.13.0,<3.0.0, installed: 2.18.0]
   │   ├── shellingham [required: >=1.3.0, installed: 1.5.4]
   │   └── typing_extensions [required: >=3.7.4.3, installed: 4.12.2]
   └── uvicorn [required: >=0.15.0, installed: 0.30.6]
   ├── click [required: >=7.0, installed: 8.1.7]
   │   └── colorama [required: Any, installed: 0.4.6]
   └── h11 [required: >=0.8, installed: 0.14.0]
   httptools==0.6.1
   psycopg2-binary==2.9.9
   python-dotenv==1.0.1
   PyYAML==6.0.2
   watchfiles==0.23.0
   └── anyio [required: >=3.0.0, installed: 4.4.0]
   ├── idna [required: >=2.8, installed: 3.7]
   └── sniffio [required: >=1.1, installed: 1.3.1]
   websockets==12.0
   ]]>
   </code-block>
    
   _List after removing pipdeptree_

3. Optimized the project by removing unnecessary dependencies.

   New `requirements.txt` file:

   <code-block lang="shell" collapsible="true" collapsed-title="requirements.txt">
    <![CDATA[
   alembic==1.13.2
   fastapi==0.112.0
   fastapi-cli==0.0.5
   httptools==0.6.1
   psycopg2-binary==2.9.9
   python-dotenv==1.0.1
   PyYAML==6.0.2
   watchfiles==0.23.0
   websockets==12.0
    ]]>
    </code-block>