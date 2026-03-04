@echo off
rem Start the agent company in a SEPARATE window. Output is captured to Saved\Logs\automation_terminal_capture.log.
rem The agent window stays open until YOU close it (so you can always see errors or success).

cd /d "%~dp0"
start "HomeWorld Agents" cmd /k "cd /d %~dp0 && powershell -NoProfile -ExecutionPolicy Bypass -File .\Tools\Run-AutomationWithCapture.ps1 -ProjectRoot %~dp0"
echo Started agents in a new window. Output captured to Saved\Logs\automation_terminal_capture.log; only you can close that window.
pause
