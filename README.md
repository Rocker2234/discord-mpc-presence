# discord-mpc-presence
This is a small python script that sets your locally running discord's Rich Presence to whatever you are playing on your MPC media player.
You can also run setup.ps1 on powershell as admin (Required for creating startup task).


[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

[Playback Icons by Sumberrejeki](https://www.flaticon.com/authors/sumberrejeki)

### Things to set up before you start using this
#### On MPC-HC
Goto Options (O) -> WebInterface -> ✔ Listen on Port. Default port 13579. Change accordingly on main.py for any other.
#### Python
* Make sure you have Python3 installed.
* Install all the required packages by running this command from project root
```ps1
  pip install -r requirements.txt
  ```
