
# �t�@�C���ړ�
#
# @param    toFolder    �ړI�p�X
# @param    fromFile    �ړ��Ώ�
#
Param (
    [parameter(mandatory = $true)][string] $toFolder,
    [parameter(mandatory = $true)][array] $fromFile
)

$current = $PSScriptRoot
Set-Location $current

if (!$toFolder.Contains($current)) {
    Write-Output $toFolder "���O�ł�"
    break
}
$fromFile | ForEach-Object {
    if (!(Test-Path $_)) {
        Write-Output $_ "�����݂��܂���B"
    } elseif (!$_.Contains($current)) {
        Write-Output $_ "���O�ł�"
    } else {
        if(!(Test-Path $toFolder))
        {
            Write-Output $toFolder "���쐬���܂����B"
            New-Item -Path $toFolder -ItemType Directory -Force | Out-Null
        }

        Write-Output $toFolder "�ֈړ����܂����B"
        Move-Item $_ $toFolder
    }
}

python .\pictureList.py