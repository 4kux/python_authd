Provided free of charge.  Feel free to use, plagiarize, and claim geek cred. - Sam Shores


The sections below are shell commands for admin functions of the HIDS agent install of OSSEC.
OSSEC is available at http://www.ossec.net.


#OSSEC Server Setup
***************************************************************************************
Configure cgi support for your Apache server. That is covered elsewhere on the internet.
Place the register.py file in the cgi-bin for your server.
Make sure you configure your sudoers file to allow your web server to run manage_agents.  I recommend limiting the permissions to allowing only manage_agents with no arguments.

#Build Server (reference system used to build the ossec binary.)  
This is important if you don't want to compile on every single system.  

Build instructions came from: http://www.ossec.net/doc/manual/installation/installation-binary.html  (I've made some changes below, in the Agent Binary Build section)

Required Software:
python 2.7
pip (install pip from http://www.pip-installer.org/en/latest/installing.html)

Linux commands for installing the necessary python modules
#pip install pexpect

***************************************************************************************


Agent Binary Build
***************************************************************************************
Before you begin...
Required Software:
  python 2.7
  pip (install pip from http://www.pip-installer.org/en/latest/installing.html)

Linux commands for installing the necessary python modules
  #pip install pexpect
  #pip install pyinstaller

Copy pyinstaller.py(located in the pyinstaller directory after the install), install.sh, install_agent.py, and register.py into a directory and run the agent build code below.

You'll need to copy pyinstaller.py into the same directory you are using as your base for the binary compilation.
***************************************************************************************

#Shell code
python pyinstaller.py install_agent.py
python pyinstaller.py reg_agent.py

wget http://www.ossec.net/files/ossec-hids-latest.tar.gz
tar -zxvf ossec-hids-latest.tar.gz
rm ossec-hids-latest.tar.gz

cd ossec-hids-*/src
make setagent
sudo make all
make build
cd ..
echo "USER_BINARYINSTALL=\"y\"" >> etc/preloaded-vars.conf
mv install.sh config.sh
cd ..
cp dist/install_agent/*  ossec-hids*/
cp dist/reg_agent/* ossec-hids*/
cp install.sh ossec-hids*/
cd ossec-hids*/
cd ..
tar -cvzf ossec-binary.tgz ossec-hids*

***************************************************************************************


Agent Installation
***************************************************************************************
#Copy the tarball to the target system and run install.sh as root (or sudo)
tar xfvz ossec-binary.tgz
cd ossec-hids*/
./install.sh

***************************************************************************************


Troubleshooting
***************************************************************************************

#  Check that DNS is configured for hostname resolution.  hosts file is a last resort, and can be flaky
#  If you didn't change the email address in the python files before running pyinstaller, you'll have some odd error messages
#  If you didn't modify the install.sh file with your serverip/hostname, it will fail completely.

#  Remove previous installation if you mess up:
   /var/bin/ossec/ossec-control stop
   rm -rf /var/ossec /etc/ossec-init.conf /etc/init.d/*ossec*
