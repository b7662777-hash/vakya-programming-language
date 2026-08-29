; Inno Setup Script for Vākya Programming Language
#define MyAppName "Vākya"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Vākya Language Team"
#define MyAppURL "https://github.com/vakya-lang/vakya"
#define MyAppExeName "vakya.exe"

[Setup]
AppId={{D3F9E1A2-8B4C-4F71-92A3-E5C7D9B10123}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Vakya
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=..\dist\installer
OutputBaseFilename=Vakya-{#MyAppVersion}-Windows-x64-Setup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ChangesEnvironment=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "envPath"; Description: "Add Vākya to user PATH environment variable"; GroupDescription: "Environment Settings:"; Flags: checkedonce
Name: "fileAssoc"; Description: "Associate .vakya files with Vākya runner"; GroupDescription: "File Associations:"; Flags: unchecked

[Files]
Source: "..\dist\Vakya\bin\vakya.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "..\dist\Vakya\resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\Vakya\std\*"; DestDir: "{app}\std"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\Vakya\runtime\*"; DestDir: "{app}\runtime"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\Vakya\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\Vakya\examples\*"; DestDir: "{app}\examples"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dist\Vakya\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Vākya"; Filename: "{app}\bin\vakya.exe"; IconFilename: "{app}\resources\vakya.ico"; WorkingDir: "{app}"
Name: "{group}\Vākya Documentation"; Filename: "{app}\docs"
Name: "{group}\Vākya Examples"; Filename: "{app}\examples"
Name: "{group}\Vākya Terminal"; Filename: "powershell.exe"; Parameters: "-NoExit -Command ""cd $env:USERPROFILE; Write-Host 'Vākya Environment Active' -ForegroundColor Green; vakya doctor"""
Name: "{group}\Uninstall Vākya"; Filename: "{uninstallexe}"

[Registry]
; File Association
Root: HKCU; Subkey: "Software\Classes\.vakya"; ValueType: string; ValueName: ""; ValueData: "VakyaSourceFile"; Flags: uninsdeletevalue; Tasks: fileAssoc
Root: HKCU; Subkey: "Software\Classes\VakyaSourceFile"; ValueType: string; ValueName: ""; ValueData: "Vākya Source File"; Flags: uninsdeletekey; Tasks: fileAssoc
Root: HKCU; Subkey: "Software\Classes\VakyaSourceFile\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\bin\vakya.exe"" ""%1"""; Flags: uninsdeletekey; Tasks: fileAssoc

[Code]
// PATH environment variable management
const EnvironmentKey = 'Environment';

procedure AddToPath();
var
  BinDir: string;
  Paths: string;
begin
  BinDir := ExpandConstant('{app}\bin');
  if RegQueryStringValue(HKCU, EnvironmentKey, 'PATH', Paths) then
  begin
    if Pos(BinDir, Paths) = 0 then
    begin
      if (Length(Paths) > 0) and (Paths[Length(Paths)] <> ';') then
        Paths := Paths + ';';
      Paths := Paths + BinDir;
      RegWriteStringValue(HKCU, EnvironmentKey, 'PATH', Paths);
    end;
  end
  else
  begin
    RegWriteStringValue(HKCU, EnvironmentKey, 'PATH', BinDir);
  end;
end;

procedure RemoveFromPath();
var
  BinDir: string;
  Paths: string;
  P: Integer;
begin
  BinDir := ExpandConstant('{app}\bin');
  if RegQueryStringValue(HKCU, EnvironmentKey, 'PATH', Paths) then
  begin
    P := Pos(BinDir, Paths);
    if P > 0 then
    begin
      Delete(Paths, P, Length(BinDir));
      // Clean duplicate or trailing semicolons
      StringChangeEx(Paths, ';;', ';', True);
      if (Length(Paths) > 0) and (Paths[Length(Paths)] = ';') then
        Delete(Paths, Length(Paths), 1);
      RegWriteStringValue(HKCU, EnvironmentKey, 'PATH', Paths);
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep = ssPostInstall) and IsTaskSelected('envPath') then
  begin
    AddToPath();
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usPostUninstall then
  begin
    RemoveFromPath();
  end;
end;
