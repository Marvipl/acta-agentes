@echo off
REM Abre o Chrome com depuracao remota, num perfil separado so para o FINEP.
REM O perfil dedicado evita expor seu navegador normal e evita o conflito com
REM uma janela do Chrome ja aberta (que faria a flag ser ignorada).
setlocal
set PORTA=9222
set PERFIL=%USERPROFILE%\.finep-chrome
set "PF=%ProgramFiles%"
set "PF86=%ProgramFiles(x86)%"
set "CHROME=%PF%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME%" set "CHROME=%PF86%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME%" set "CHROME=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME%" goto semchrome
if not exist "%PERFIL%" mkdir "%PERFIL%"
echo Abrindo o Chrome na porta %PORTA% com o perfil %PERFIL%
echo Faca login no FINEP nesta janela e deixe-a aberta.
start "" "%CHROME%" --remote-debugging-port=%PORTA% --user-data-dir="%PERFIL%" "https://credito.finep.gov.br/"
goto fim
:semchrome
echo Nao encontrei o chrome.exe nos caminhos padrao.
echo Ajuste a variavel CHROME neste arquivo com o caminho correto.
pause
:fim
