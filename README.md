# GLPI-Agent-watchdog-service
Check GLPI server and agent and restar agent if no answer.

**Compilation**:
Place api-ms-win-core-path-l1-1-0.dll file to the same dirrectory as agent-svc-wd.py (for Windows 7 support).
Install Python 3.11, nuitka and nuitka-winsvc, configure and run nuitka-compile.bat.

**Installer**:
Install Inno Setup, use agent-wd.iss to make installation file.


Ready to use compiled installer: https://github.com/ra1qcw/GLPI-Agent-watchdog-service/raw/main/awd-setup.exe
Support keys:
/SILENT, /VERYSILENT
Instructs Setup to be silent or very silent. When Setup is silent the wizard and the background window are not displayed but the installation progress window is. When a setup is very silent this installation progress window is not displayed.
