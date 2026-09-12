[Setup]
AppName=Anti-AFK
AppVersion=1.0.0
DefaultDirName={autopf}\AntiAFK
DefaultGroupName=AntiAFK
Compression=lzma2
SolidCompression=yes
OutputDir=output
OutputBaseFilename=AntiAFK_Installer
SetupIconFile=C:\Users\gabip\OneDrive\Desktop\Anti afk\app.ico

[Files]
Source: "dist\AntiAFK.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Anti-AFK"; Filename: "{app}\AntiAFK.exe"; IconFilename: "{app}\app.ico"
Name: "{autodesktop}\Anti-AFK"; Filename: "{app}\AntiAFK.exe"; IconFilename: "{app}\app.ico"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; Flags: unchecked
