# Project Shortcut 
#### By koon64 
Easily create projects from the command line

### What it does

#### Base project command
The base project command creates a project regardless of what language you are choosing to use

1. Creates and enters the specified directory given
2. Creates a new README from the folder name
3. Creates a license
4. Creates a Github repo
3. Initialize a repo, add files, commit, & push
4. Opens VS code 

### Setup

If you are on windows clone this repo in your user's account
`C:\Users\koon>git clone https://github.com/koon64/project_shortcut.git`

Install dependencies
`pip install -r requirements.txt`

Create a file called `.env` and enter options
```txt
AUTHOR=<Your Name>
GITHUB_ACCESS_TOKEN=<YOUR TOKEN HERE>
```

Copy `project.bat` into `C:\Windows\System32\`

### Usage

Create a project in the current directory
```cmd
> project .
```

Create a project in a new directory
```cmd
> project dir_name
```

