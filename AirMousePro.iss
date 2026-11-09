; AirMouse Pro Installer

[Setup]
AppId={{F782115A-462C-4A12-B2B5-D1401BE26DA5}

AppName=AirMouse Pro
AppVersion=1.0.0

AppPublisher=Mano Francis
AppPublisherURL=https://manofrancis-dev.github.io/airmousepro/
AppSupportURL=https://manofrancis-dev.github.io/airmousepro/
AppUpdatesURL=https://manofrancis-dev.github.io/airmousepro/

VersionInfoVersion=1.0.0
VersionInfoCompany=Mano Francis
VersionInfoDescription=AirMouse Pro Setup
VersionInfoProductName=AirMouse Pro
VersionInfoProductVersion=1.0.0
VersionInfoCopyright=Copyright (c) Mano Francis

DefaultDirName={autopf}\AirMouse Pro
DisableDirPage=yes

; Installer icon
SetupIconFile=AirMousePro.ico

; Uninstaller icon
UninstallDisplayIcon={app}\AirMousePro.ico

; 64-bit Windows
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DisableProgramGroupPage=yes

; Installer filename
OutputBaseFilename=AirMousePro_Setup

SolidCompression=yes
WizardStyle=modern dynamic


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked


[Files]

; Main AirMouse Pro executable
Source: "dist\AirMousePro\AirMousePro.exe"; DestDir: "{app}"; Flags: ignoreversion

; PyInstaller internal files
Source: "dist\AirMousePro\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; AirMouse Pro custom icon
Source: "AirMousePro.ico"; DestDir: "{app}"; Flags: ignoreversion


[Icons]

; Start Menu shortcut with custom icon
Name: "{autoprograms}\AirMouse Pro"; Filename: "{app}\AirMousePro.exe"; IconFilename: "{app}\AirMousePro.ico"; IconIndex: 0

; Desktop shortcut with custom icon
Name: "{autodesktop}\AirMouse Pro"; Filename: "{app}\AirMousePro.exe"; IconFilename: "{app}\AirMousePro.ico"; IconIndex: 0; Tasks: desktopicon


[Run]

; Launch AirMouse Pro after installation
Filename: "{app}\AirMousePro.exe"; Description: "{cm:LaunchProgram,AirMouse Pro}"; Flags: nowait postinstall skipifsilent