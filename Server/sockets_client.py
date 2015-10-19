import sys, os, socket, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.137.98', 5000))
while True:
    cmd = raw_input('$ ')
    s.send(cmd) 
    result = s.recv(1024)
    print result
    if result == "**END**":
        print "Ending"
        break
