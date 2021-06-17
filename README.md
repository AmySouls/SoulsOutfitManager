# SoulsOutfitManager
 
SoulsOutfitManager is a work in progress python program for easy managing of Souls part mods such as ones that change the apperance of your armor or weapons.
It will allow you to easily manage replacements, and revert those changes without needing to repack with UXM or sort them yourself.
There will also be a feature to change the model masks of armor pieces while the game is running, and save the preferences to a file.
 
## Support
Currently, it only supports DARK SOULS III, and will be intended to be used with [UXM](https://www.nexusmods.com/sekiro/mods/26)!, and later Mod Engine and ModEngine2. Support for other games such as DARK SOULS: REMASTERED may be considered after.

## How to use

### Getting Started
1: Download SoulsOufitManager under Releases, extract the zip and run the exe. Do not remove it from the folder it was extracted into.
2: Use the browse button to show the program where your game folder containing ```DarkSoulsIII.exe``` is located. 

### Replacing a part file
1: Place any DS3 part mods(Files ending with ".dcx") you wish to install in the mods folder next to ```SoulsOutfitManager.exe``` and click refresh.
2: Highlight the file under "Your Prepared Mods" you want to replace another file with, search in "Parts in your Game" and double click the file you wish to replace.
3: Press "Ok" on the confirmation window.
4: Reequip the armor piece or weapon ingame.

### Replacing a part file with nothing
1: Highlight the file you want to replace with nothing under "Parts in your Game", then click "Delete" on your keyboard.
2: Press "Ok" on the confirmation window

### Restoring a replaced or deleted part file
1: Select the file in the "Installed Modded Parts" window and click "Backspace" on your keyboard.
2: Press "Ok" on the confirmation window

### Editing model Masks
Incase an armor replacement hides a certain body part or does not when it should, you can use the edit model masks pane to
edit the model masks of currently replaced parts.

1: Select the part you wish to edit the model masks under "Installed Modded Parts"
2: Check on or off model masks under "Edit Model Masks".
3: Click "Save & Update Model Mask Changes" to confirm your changes.
4: Open DS3 or if you have DS3 already open, reequip the armor you edited the masks of.

As long as a part is replaced under "Installed Modded Parts", the model mask changes will apply when you click
save & update model mask changes while the game is running or when you launch the program while the game is running.
To restore the original model masks of an armor piece, either restore the part or delete the ```.modelmaskpreset.json``` file in the mods folder.

### Updating manual changes
Incase you went ahead yourself and manaully messed with the game part files, click refresh to update those changes.
