cd %~dp0
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /f /v Path /t REG_SZ /d "%path%;%~dp0
reg add "HKCR\JSONGFile\shell\open\command" /f /ve /t REG_SZ /d "\"%~dp0jsong-viewer.exe\" \"%%1\""
del %~n0%~x0