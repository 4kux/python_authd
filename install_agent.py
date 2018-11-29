#!/usr/bin/python

import sys, os, re, pexpect
from cgi import escape

email = 'a.boulayd@eca-assurances.com'

def installBinary(binaryfile,server):
  c = pexpect.spawn(binaryfile)

  #Language selection
  c.expect(r'\[en\]:')
  print('Setting language to '+re.match('\[(\w+)\]',c.after).group(1))
  c.sendline('')

  #Run Install
  c.expect(r'-- Press ENTER to continue or Ctrl-C to abort. --')
  c.sendline('')

  #Select install type
  c.expect(r' What kind of installation do you want \(server, agent, local, hybrid or help\)\?')
  c.sendline('agent')

  #Select install lcoation
  c.expect(r'Choose where to install the OSSEC HIDS \[/var/ossec\]:')
  c.sendline('')

  #Enter Server Hostname
  c.expect(r'What\'s the IP Address or hostname of the OSSEC HIDS server\?:')
  c.sendline(server)

  #Integrity Check Daemon
  c.expect(r' Do you want to run the integrity check daemon\? \(y/n\) \[y\]:')
  c.sendline('')

  #Rootkit Detection
  c.expect(r' Do you want to run the rootkit detection engine\? \(y/n\) \[y\]:')
  c.sendline('')

  #Active Response
  print('Setting Active Response to false')
  c.expect(r' Do you want to enable active response\? \(y/n\) \[y\]:')
  c.sendline('n')

  #Continue
  c.expect(r'--- Press ENTER to continue ---')
  c.sendline('')
  c.expect(r'---  Press ENTER to finish \(maybe more information below\)\. ---')
  c.sendline('')

def main():
  #Install binary file - use an argv
  #Run through install script - use pexpect

  args = sys.argv[:]

  if len(args) <= 2:
    print('Usage: install_agent.py <</path/to/unzipped/binary/install.sh>> <<Hids Server hostname>>')
    sys.exit(1)
  else:
    binaryfile = args[1]
    server = args[2]

  print('Running /bin/bash '+binaryfile+' ...')
  try:
    installBinary(binaryfile,server)
    print('Successfully installed agent')
  except:
    print("Error installing OSSEC binary.  Error in reg_agent.")
    print('Contact: '+email)
    sys.exit(1)
  #Exit Safely
  #print('OSSEC HIDS Agent Registered Successfully')
  sys.exit(0)

if __name__ == '__main__':
    main()
