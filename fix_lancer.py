content = (
    b"@echo off\r\n"
    b'cd /d "%~dp0"\r\n'
    b'start "" "C:\\Users\\StyveDev-PC\\AppData\\Local\\Programs\\Python\\Python315\\pythonw.exe" "%~dp0download.py"\r\n'
    b"exit\r\n"
)
with open("lancer_app.bat", "wb") as f:
    f.write(content)
print("lancer_app.bat written!")
