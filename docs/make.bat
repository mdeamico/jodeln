@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation
REM run in a powershell terminal using the following command:
REM cmd /c make.bat github

if "%SPHINXBUILD%" == "" (
	set "SPHINXBUILD=..\.env\Scripts\sphinx-build.exe"
)
set SOURCEDIR=source
set BUILDDIR=build

REM gh-pages worktree directory
set DOCS=..\..\jodeln-docs

if "%1" == "" goto help
if "%1" == "github" goto github

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:github
rmdir /S /Q "%BUILDDIR%"
%SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
REM Use robocopy to mirror build directory into gh-pages worktree directory
robocopy "%BUILDDIR%\html" "%DOCS%" /MIR /JOB:robocopy.rcj
IF NOT EXIST "%DOCS%\.nojekyll" echo. 2>"%DOCS%\.nojekyll"
goto end

:end
popd
