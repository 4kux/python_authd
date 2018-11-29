#!/usr/bin/python

import sys, os, re, pexpect
from cgi import escape

email = 'a.boulayd@eca-assurances.com'

def register(ip):

  c = pexpect.spawn('sudo /var/ossec/bin/manage_agents')

  #Add Agent
  c.expect('Choose your action: A,E,L,R or Q:')
  c.sendline('a')

  #Set Name
  c.expect('A name for the new agent:')
  c.sendline(ip)

  #Set IP
  c.expect('The IP Address of the new agent:')
  c.sendline(ip)

 c.expect('The IP Address of the new agent:')
  c.sendline(ip)

  #Parse ID + Confirm default value
  c.expect('\[\d+\]:')
  id = re.search('(\d+)',c.after).group(1)
  c.sendline('')

  #Confirm
  c.expect(':')
  c.sendline('y')

  #Extract Key
  c.expect('Choose your action: A,E,L,R or Q:')
  c.sendline('e')

  #Call ID
  c.expect(':')
  c.sendline(id)

  #Read Agent Key
  c.expect('\S{108}') #key is 108 character
  return c.after

def main():

  #Set up the response for html readable text
  print "Content-type: text/html"
  print
  print "<pre>"

  #grab the IP from the request header
  ip = escape(os.environ['REMOTE_ADDR'])

  #Ensure it looks like an IP.
  item =  re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',ip)

  if item:
    try:
      #register the IP and send the key string
      key = register(ip)
      print key

    # oops
    except:
      print('Error: Could not register.  Contact '+email)
      exit(1)

  #close out the html text
  print "</pre>"

if __name__ == '__main__':
    main()
