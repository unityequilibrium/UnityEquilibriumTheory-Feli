$root = "research_uet/topics"
Get-ChildItem -Path $root -Directory | ForEach-Object {
    $topicPath = $_.FullName
    $docsPath = Join-Path $topicPath "Docs"
    $docPath = Join-Path $topicPath "Doc"

    if (Test-Path $docsPath) {
        if (-not (Test-Path $docPath)) {
            Write-Host "Creating Doc folder for $($_.Name)"
            New-Item -ItemType Directory -Path $docPath | Out-Null
        }

        Write-Host "Processing $($_.Name)..."
        
        # Move all items from Docs to Doc
        Get-ChildItem -Path $docsPath | ForEach-Object {
            $dest = Join-Path $docPath $_.Name
            if (Test-Path $dest) {
                Write-Warning "File exists in destination: $dest. Skipping move for this file."
            } else {
                Move-Item -Path $_.FullName -Destination $docPath
            }
        }

        # Check if Docs is empty and delete it
        if ((Get-ChildItem -Path $docsPath).Count -eq 0) {
            Remove-Item -Path $docsPath
            Write-Host "Removed empty Docs folder for $($_.Name)" -ForegroundColor Green
        } else {
            Write-Warning "Docs folder for $($_.Name) is NOT empty (likely duplicates skipped). Manual check required."
        }
    }
}
Write-Host "Cleanup Complete."
