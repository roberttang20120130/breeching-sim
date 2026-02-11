# CQB Simulator

A top-down perspective Close Quarters Battle (CQB) simulator built for tactical map simulation. This is an open-source project—feel free to modify, contribute, or create your own maps!

## Table of Contents

[Overview](#overview)

[Features](#features)

[Roadmap](#Roadmap)

[Installation](#installation)

[Building the Project and dev info](#building-the-project)

[Contributing](#contributing)

[Contact](#contact)

## Overview

This simulator allows you to create and view tactical maps for CQB scenarios. Maps are defined in a custom .thmap file format and rendered in a 20x20 grid. The project includes a viewer executable for opening and interacting with maps.

Important Resources: All key assets (e.g., icons, documentation) are in the devresources folder.

Builds: Pre-built executables are in the game folder.

## Features

Top-down grid-based simulation of CQB environments.
Custom .thmap file format for easy map creation and sharing.
Windows registry integration for file associations (e.g., double-click to open maps in the viewer).
Open-source: Modify the code, fix bugs, or add features on your own machine.

## Roadmap
This project is actively evolving. Here's a high-level plan for upcoming updates:

Prerelease 0.2: Increased max map size (expanding beyond the current 20x20 grid limit).

Prerelease 0.3: Better AI strategy (improved enemy behavior and decision-making).

Prerelease 0.4: Better hitboxes (refined collision detection for more accurate interactions).

Prerelease 0.5: Cosmetic update (visual enhancements, such as improved graphics or UI elements).

Release 1.0: Polishing the release (final bug fixes, optimizations, documentation updates, and overall refinement for a stable launch).
If you'd like to contribute to any of these features (e.g., code, testing, or ideas), check out the Contributing section!

## Installation

1. Download or clone the repository.
2. Place the entire project folder in your desired location (e.g., C:\cqb-sim).

**note**

For Windows users: To make the .reg file work without any modifications, place directly in the C: directory:
If placing the folder on C:, run the provided .reg file directly.

If placing on another drive (e.g., D:), edit the .reg file first. Here's an example for D:\cqb-sim:

```
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
@="D:\\cqb-sim\\devresources\\map.ico,0"

; Define how it opens
[HKEY_CLASSES_ROOT\THMapFile\shell\open\command]
@="\"D:\\cqb-sim\\game\\viewer.exe\" \"%1\""
```

4. Double-click the .reg file to apply changes. Restart your file explorer if needed.

Note: Maps must be exactly 20x20 grids, or the game will break.

## Building the Project

The project is built using pygame and python 3.11.9. Builds for Windows are already in the game folder.
macOS Build Request: I don't have access to a Mac or the $100 Apple Developer certificate. If anyone can build and test an Apple (macOS) version, please contribute it! Submit via pull request or email (see Contact).
Map File Format (.thmap)
Maps use a custom .thmap filetype, which is a simple JSON-like array format representing a 20x20 grid.

**Grid Values:**

0: Floor (walkable space).
1: Wall (obstacle).
2: Enemy operator.
Format Rules:

The file starts with [ and ends with ].
Each row is inside its own [], separated by commas.
Values within a row are separated by commas (no commas at the start or end of a row).
The grid must be exactly 20x20—anything else will break the simulator.
Here's a sample map file:

```
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
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
```
You can create maps manually in a text editor or use the provided map editor.

## Contributing

This project is open-source! If you encounter issues, have suggestions, or want to improve it:

Modify the code on your own computer.
Send bug fixes, mods, or new features to roberttang20120130@gmail.com.
If sharing maps online, please include a link back to this original project.
Mods to enhance the simulator (e.g., new features, better UI, or platform support) are strongly encouraged. Pull requests are welcome!

## Contact

For questions, contributions, or feedback, email roberttang20120130@gmail.com.

### note
sorry about the tons of edits to the readme, I havn't got the hang of github readmes yet.
