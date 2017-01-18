
$computer1 = 'qaagiletask1b'

Import-Module PSRemoteRegistry

Get-RegValue -ComputerName $computer1 -Key  -Value PackageVersion 

# Get-RegValue -ComputerName $computer1 -Key SOFTWARE\Veritas\NetBackup\CurrentVersion -Value PackageVersion 

$w32reg = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey('LocalMachine',$computer1)
$keypath = 'SOFTWARE\Veritas\NetBackup\CurrentVersion'
$netbackup = $w32reg.OpenSubKey($keypath)
$NetbackupVersion1 = $netbackup.GetValue('PackageVersion')