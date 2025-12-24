; --- SCRIPT DE INSTALACIÓN EZLIFE TOOL ---

#define MyAppName "EZLife Tool"
#define MyAppVersion "1.0"
#define MyAppPublisher "RodriGGod"
#define MyAppExeName "EZLife_Config.exe"
#define MyBrowserExe "EZLife_Browser.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; GUARDARÁ EL INSTALADOR EN LA CARPETA "Output" DENTRO DE TU CARPETA BUILD
OutputDir=Output 
OutputBaseFilename=EZLifeInstaller
; Icono del instalador
SetupIconFile=src\resources\EZlifeLogo.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
; Evitar que pida reiniciar
RestartIfNeededByRun=no
; Cerrar automáticamente las aplicaciones que están en uso
CloseApplications=yes
CloseApplicationsFilter=*.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart"; Description: "Ejecutar controlador al inicio de Windows"; GroupDescription: "Opciones adicionales:"

[Files]
; Archivos compilados desde src\dist
Source: "src\dist\EZLife_Config.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace
Source: "src\dist\controlador.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace
Source: "src\dist\EZLife_Browser.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace
; Incluir el icono en la instalación
Source: "src\resources\EZlifeLogo.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\EZlifeLogo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\EZlifeLogo.ico"; Tasks: desktopicon

[Registry]
; REGISTRO DEL NAVEGADOR PARA WINDOWS
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool"; ValueType: string; ValueName: ""; ValueData: "EZLife Tool"
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities"; ValueType: string; ValueName: "ApplicationDescription"; ValueData: "EZLife Tool - Context Switching"
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities"; ValueType: string; ValueName: "ApplicationIcon"; ValueData: "{app}\{#MyBrowserExe},0"
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities"; ValueType: string; ValueName: "ApplicationName"; ValueData: "EZLife Tool"

; Asociaciones URL
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities\URLAssociations"; ValueType: string; ValueName: "http"; ValueData: "EZLifeToolHTML"
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities\URLAssociations"; ValueType: string; ValueName: "https"; ValueData: "EZLifeToolHTML"
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities\StartMenu"; ValueType: string; ValueName: "StartMenuInternet"; ValueData: "EZLifeTool"

; Comandos de ejecución
Root: HKLM; Subkey: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyBrowserExe}"" ""%1"""
Root: HKLM; Subkey: "SOFTWARE\Classes\EZLifeToolHTML"; ValueType: string; ValueName: ""; ValueData: "EZLife Tool Link"
Root: HKLM; Subkey: "SOFTWARE\Classes\EZLifeToolHTML\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyBrowserExe},0"
Root: HKLM; Subkey: "SOFTWARE\Classes\EZLifeToolHTML\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyBrowserExe}"" ""%1"""

; Registrar App
Root: HKLM; Subkey: "SOFTWARE\RegisteredApplications"; ValueType: string; ValueName: "EZLifeTool"; ValueData: "SOFTWARE\Clients\StartMenuInternet\EZLifeTool\Capabilities"

[Run]
; Ejecutar controlador en segundo plano después de la instalación
Filename: "{app}\controlador.exe"; Flags: nowait postinstall skipifsilent runhidden
; Opcional: Abrir la configuración
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[Registry]
; Ejecutar controlador.exe al inicio de Windows (si el usuario marcó la opción)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "EZLifeController"; ValueData: """{app}\controlador.exe"""; Tasks: autostart