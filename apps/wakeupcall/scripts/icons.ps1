# icons.ps1 - generate resized android notification icons
$ErrorActionPreference = 'Stop'
$OutputEncoding = [System.Text.Encoding]::UTF8

Add-Type -AssemblyName System.Drawing

# source image path
$inputPath = "ic_notification.png"

# validate source image
if (-not (Test-Path $inputPath)) {
    Write-Host "❌ source image not found at $inputPath"
    exit 1
}

try {
    $sourceImage = [System.Drawing.Image]::FromFile($inputPath)
} catch {
    Write-Host "❌ failed to load source image: $_"
    exit 1
}

# define output resolutions
$sizes = @{
    "mdpi"   = 24
    "hdpi"   = 36
    "xhdpi"  = 48
    "xxhdpi" = 72
    "xxxhdpi"= 96
}

foreach ($dpi in $sizes.Keys) {
    $size = $sizes[$dpi]
    $outputPath = "app\src\main\res\drawable-$dpi\ic_notification.png"

    # ensure output directory exists
    $outputDir = Split-Path $outputPath
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    }

    Write-Host "📦 saving $outputPath"

    try {
        # resize image
        $resized = New-Object System.Drawing.Bitmap $size, $size
        $graphics = [System.Drawing.Graphics]::FromImage($resized)
        $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $graphics.DrawImage($sourceImage, 0, 0, $size, $size)
        $graphics.Dispose()

        # save image
        $resized.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $resized.Dispose()
    } catch {
        Write-Host ("❌ failed to save $outputPath:`n" + $_)
    }
}

$sourceImage.Dispose()
Write-Host "✅ done generating icons."
