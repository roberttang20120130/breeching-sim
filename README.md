this is a top down perspective CQB simulator
please, anyone make a apple build, I do not have a mac, and I do not have the 100$ for the apple developer certificate
It uses a custom filetype called .thmap for the map
all the important rescources are in devrescources 
the app builds are in game
put this folder into disk C: for native .reg running, 
if you put the folder in D:, modify the .reg so it looks like this:

Windows Registry Editor Version 5.00

; Remove bad association
[-HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.thmap]

; Define extension → filetype
[HKEY_CLASSES_ROOT\.thmap]
@="THMapFile"
"PerceivedType"="text"

; Define the filetype itself
[HKEY_CLASSES_ROOT\THMapFile]
@="CQB Tactical Map File"

; Set CUSTOM ICON (this is the important part)
[HKEY_CLASSES_ROOT\THMapFile\DefaultIcon]
@="D:\\cqb sim\\devrescources\\map.ico,0"

; Define how it opens
[HKEY_CLASSES_ROOT\THMapFile\shell\open\command]
@="\"D:\\cqb sim\\game\\viewer.exe\" \"%1\""

the map files are in thmap format which documentation is below:
the maps are always 20x20 or the game breaks

here is a sample:

[
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,0,1],
[1,0,1,0,0,1,0,1,2,0,1,0,1,0,0,1,0,1,0,1],
[1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1],
[1,0,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1],
[1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1],
[1,0,2,0,0,1,0,1,1,1,1,1,0,1,0,0,2,0,0,1],
[1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1],
[1,1,1,1,0,1,0,1,0,2,0,1,0,1,0,1,1,1,1,1],
[1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
[1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,0,1],
[1,0,1,0,0,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1],
[1,0,1,0,0,1,0,1,2,0,1,0,0,1,0,0,0,1,0,1],
[1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

1 is wall, 2 is enemy operators, 0 is floor

there is always a [ at the start and a ] at the end, 
each line is seperated by a comma and inside [], 
each point is seperated by commas
there is no commas at the start or end of each line inside []

if there is any issues or sugestions, this is open sourced so mod it on your computer
please send any mods or bugfixes to roberttang20120130@gmail.com

any maps can be posted online with a link to the original project

any mods to make this better are strongly supported
