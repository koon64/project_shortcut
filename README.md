# Project Shortcut 
#### By koon64 
[![License](https://img.shields.io/github/license/koon64/project_shortcut)](https://github.com/koon64/project_shortcut)
[![Format](https://camo.githubusercontent.com/28a51fe3a2c05048d8ca8ecd039d6b1619037326/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667)](https://github.com/psf/black)

Easily initialize projects from the command line

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

Install dependencies
`pip install -r requirements.txt`

Create a file called `config.yml` and enter options
```txt
author: <Your Name>
github_access_token: <YOUR TOKEN HERE>
security_contact_email: <SOME EMAIL>
hr_contact_email: <OTHER EMAIL>
```

If you are on windows, move the repo in your user's account

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

### Top Level Projects

1. [Python](https://github.com/koon64/project_shortcut/tree/master/create/projects/python)
2. Node (comming soon)
3. PHP (prob not comming soon)
