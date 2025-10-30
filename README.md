github repo for ENES100 

instructions for my group members to set it up: 

Download Git from https://git-scm.com/install/

Create a github account

Create a folder on your computer called ENES_100 or something similar

go to your computer's terminal(terminal on macOS, GIT bash/powershell on windows)

find the folder you created, use commands ls and cd to navigate your way

^ls command will list all directories(folders) and files, cd will move into that folder

on terminal, type the following: git clone https://github.com/ArnoLand/ESP32_OTV.git

If all works well, in your ENES_100 folder, this project should be cloned

To test if it works, navigate to yout folder(on file explorer) and create a new python file

Open that file through Thonny, type something simple like hello world print statement

Go back to terminal, navigate to folder, and type: git checkout -b newBranch

then run these commands:

git add .

git commit -m "testing!"

git push -u origin newBranch

let me know once you do this, I'll check if it works 



