@echo off

if "%GITHUB_USERNAME%"=="" (
    echo "You must have the GITHUB_USERNAME variable set"
    exit 1
)

set dir=%1
:: set the first arg to . if not set
if "%dir%"=="" (
    set dir=.
)

:: check if the dir exists
if not exist %dir% (
    echo Creating directory "%dir%"
    md %dir%
    cd %dir%
)
:: set the project name to the dir
set project_name=%dir%

:: set the project name to the current folder if it is .
if "%project_name%"=="." (
    for %%I in (.) do set project_name=%%~nxI
)
:: use powershell to capitalize the first letter of each word of a string
for /f "delims=" %%a in (' powershell "echo (Get-Culture).TextInfo.ToTitleCase('%project_name%'.replace('_', ' '))" ') do set "display_name=%%a"

:: create the readme if not exist
if not exist README.md (
    echo # %display_name% > README.md
    echo #### By %GITHUB_USERNAME% >> README.md
)

:: initialize the git repo
git init
git remote add origin git@github.com:%GITHUB_USERNAME%/%project_name%.git
git add .
git commit -m "Initial Commit"
git push -u origin master

:: open in vs code
code .
