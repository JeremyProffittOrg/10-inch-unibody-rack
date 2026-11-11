param([int]$Plate=0)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$source=Join-Path $PSScriptRoot 'acer-dgx-enclosure-v13-separate-plates.3mf'
$inputProject=Join-Path $PSScriptRoot 'support-audit-input.3mf'
Copy-Item -LiteralPath $source -Destination $inputProject -Force
$archive=[System.IO.Compression.ZipFile]::Open($inputProject,[System.IO.Compression.ZipArchiveMode]::Update)
try {
    $entry=$archive.GetEntry('Metadata/project_settings.config')
    $reader=[System.IO.StreamReader]::new($entry.Open())
    $profile=$reader.ReadToEnd() | ConvertFrom-Json
    $reader.Dispose()
    $profile.enable_support='1'
    $profile.support_type='normal(auto)'
    $profile.support_threshold_angle='45'
    $profile.support_on_build_plate_only='0'
    $profile.support_critical_regions_only='0'
    # Permit short, anchored bridges; larger spans still trigger support.
    $profile.bridge_no_support='1'
    $profile.max_bridge_length='10'
    $entry.Delete()
    $writer=[System.IO.StreamWriter]::new($archive.CreateEntry('Metadata/project_settings.config').Open())
    $writer.Write(($profile | ConvertTo-Json -Depth 30))
    $writer.Dispose()
} finally { $archive.Dispose() }
$arguments='--slice '+$Plate+' --debug 2 --outputdir "'+$PSScriptRoot+'" --export-3mf support-audit-sliced.3mf "'+$inputProject+'"'
$process=Start-Process -FilePath 'C:\Program Files\Bambu Studio\bambu-studio.exe' -ArgumentList $arguments -PassThru -WindowStyle Hidden -Wait
Write-Output ('Slicer exit code: '+$process.ExitCode)
if($process.ExitCode -ne 0){exit $process.ExitCode}
