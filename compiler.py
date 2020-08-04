import PyInstaller.__main__
import os
import shutil
import sys
import time

# ------------------------------------------------------------------------------------------------------------

filepath = __file__
relative = ""
cut = 0
executable = True
for i in range(0, len(filepath)):
    if filepath[i] == "/" or filepath[i] == "\\":
        relative += "\\"
        cut = i + 1
        executable = False
    else:
        relative += filepath[i]
if executable:
    filepath = sys.executable
    relative = ""
    cut = 0
    for i in range(0, len(filepath)):
        if filepath[i] == "/" or filepath[i] == "\\":
            relative += "\\"
            cut = i + 1
        else:
            relative += filepath[i]

relative = relative[0:cut]

# ------------------------------------------------------------------------------------------------------------

PyInstaller.__main__.run(["-w", "-F", relative + "streamline.py"])

os.remove("G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\monopoly.exe")
os.rename("G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\dist\\streamline.exe", "G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\monopoly.exe")

shutil.rmtree("G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\dist")
shutil.rmtree("G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\__pycache__")
shutil.rmtree("G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\build")
os.remove("G:\\Code\\Python Stuff\\Games\\Monopoly\\actual game\\streamline.spec")
