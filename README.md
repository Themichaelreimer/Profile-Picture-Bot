# Profile Bot

Currently tested on Linux, for deployment on linux servers.
Can be modified with little effort to run on other platforms

# What it does

Rotates your profile picture in even, daily steps, such that it will complete one
full rotation per year. 

# Usage:

Ensure requirements are installed: `pip3 install -r requirements.txt`

Ensure the following files exist:

|file|purpose|
|---|---|
|profile.png|Base profile picture image|
|.secrets|Contains the following on two lines: USERNAME=USERNAME_HERE PASSWORD=PASSWORD_HERE|

Afterwards, run `python3 main.py`.
