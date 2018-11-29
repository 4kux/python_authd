#!/usr/bin/python

import sys, os, re, pexpect, httplib
from cgi import escape

email = 'a.boulayd@eca-assurances.com'

def register(key):
  #Some of this expect code looks odd.
  #It's design is to make sure it waits for the last line that looks
  #like a prompt.  Some of the other text contains the ':' prompt
  #in the manage_agents binary.

  #Launch registration binary
  print('Launching manage_agents')
  try:
    c = pexpect.spawn('sudo /var/ossec/bin/manage_agents')

    #Select "import"
    c.expect('Choose your action: I or Q:')
    c.sendline('i')

    #Enter key
    c.expect(':')
    c.sendline(key)

    #Confirm key addition
    c.expect(':')
    c.sendline('y')

    #Newline required
    c.sendline('')
    
    #Exit binary
    c.expect(':')
    c.sendline('q')
  except:
    print('Error in local registration.')
    print('Contact '+email)
    sys.exit(1)

  print('Local registration complete.')

  return 0

def getKey(server):
  key = 'no key found.'
  try:
    c = httplib.HTTPSConnection(server)
    c.request("GET", "/cgi-bin/register.py")
    print('Connecting to: https://'+server+'/cgi-bin/register.py')
    response = c.getresponse()
    data = response.read()
    key = re.match('<pre>\\n(\S+)\\n</pre>',str(data)).group(1)
  except:
    print('Error: Connection failed or Registration Error')
    print('Contact '+email)
    sys.exit(1)
  #Success  
  print('Received key from '+server)
  return key

def restartServices():
  print("Restarting OSSEC services")
  os.system('/var/ossec/bin/ossec-control restart')
    
def main():

  if len(sys.argv) == 1:
    print('Usage:  reg_agent.py <<serverip>>')
    sys.exit(1)

  else:
    #Get key from server
    server = sys.argv[1]
    print('Registering with: '+server)
    key = getKey(server)
    
    #Register key locally
    print('Registering Agent Key with local system...')
    register(key)
    
    #Restart Services
    restartServices()
    
    #Exit Safely
    print('OSSEC HIDS Agent Registered Successfully')
    sys.exit(0)

if __name__ == '__main__':
    main()

