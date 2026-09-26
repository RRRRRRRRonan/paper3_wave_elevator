$ErrorActionPreference = 'Stop'
$sourcePath = 'F:\Paper 3\Problem formulation.docx'
$reviewPath = 'F:\Paper 3\.codex_review\2026-09-14-finalcheck'
$snapshotPath = Join-Path $reviewPath 'source-snapshot.docx'
$pdfPath = Join-Path $reviewPath 'word-render.pdf'
$inputStream = [System.IO.File]::Open($sourcePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
try {
    $outputStream = [System.IO.File]::Open($snapshotPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write)
    try { $inputStream.CopyTo($outputStream) } finally { $outputStream.Dispose() }
} finally { $inputStream.Dispose() }
$wordReviewApp = $null
$reviewDoc = $null
try {
    $wordReviewApp = New-Object -ComObject Word.Application
    $wordReviewApp.Visible = $false
    $wordReviewApp.DisplayAlerts = 0
    $wordReviewApp.AutomationSecurity = 3
    $wordReviewApp.Options.UpdateLinksAtOpen = $false
    $reviewDoc = $wordReviewApp.Documents.Open($snapshotPath, $false, $true, $false)
    $reviewDoc.Repaginate()
    Write-Output ('PAGE_COUNT=' + $reviewDoc.ComputeStatistics(2))
    $reviewDoc.ExportAsFixedFormat($pdfPath, 17)
    Write-Output ('PDF=' + $pdfPath)
} finally {
    if ($null -ne $reviewDoc) { $reviewDoc.Close(0); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($reviewDoc) }
    if ($null -ne $wordReviewApp) { $wordReviewApp.Quit(0); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordReviewApp) }
}
Get-FileHash -Algorithm SHA256 -LiteralPath $snapshotPath | Select-Object Hash
