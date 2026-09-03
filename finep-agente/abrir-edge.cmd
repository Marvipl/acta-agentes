@echo off
REM Abre o Microsoft Edge com depuracao remota, num perfil separado para o FINEP.
REM Edge e Chromium: a porta de depuracao funciona igual a do Chrome.
setlocal
set PORTA=9222
set PERFIL=%USERPROFILE%\.finep-edge
set "PF=%ProgramFiles%"
set "PF86=%ProgramFiles(x86)%"
set "EDGE=%PF86%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" set "EDGE=%PF%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" set "EDGE=%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" goto semedge
if not exist "%PERFIL%" mkdir "%PERFIL%"
echo Abrindo o Edge na porta %PORTA% com o perfil %PERFIL%
echo Faca login no FINEP nesta janela e deixe-a aberta.
start "" "%EDGE%" --remote-debugging-port=%PORTA% --user-data-dir="%PERFIL%" "https://credito.finep.gov.br/"
goto fim
:semedge
echo Nao encontrei o msedge.exe nos caminhos padrao.
echo Ajuste a variavel EDGE neste arquivo com o caminho correto.
pause
:fim
