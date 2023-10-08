nuitka agent-wd-svc.py --standalone --onefile --remove-output --jobs=6 ^
 --include-package=win32timezone ^
 --include-data-files=api-ms-win-core-path-l1-1-0.dll=api-ms-win-core-path-l1-1-0.dll ^
 --windows-service ^
 --windows-service-name=glpi-agent-wd ^
 --windows-service-display-name="GLPI-Agent-WD" ^
 --windows-service-description="GLPI Agent Watchdog service" ^
 --windows-icon-from-ico=logo.ico
