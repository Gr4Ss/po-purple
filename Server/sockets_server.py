import sys, os, socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5000))
print("Server started")
s.listen(10)
global Busy
global Proces
while True:
    print "Accepting"
    conn, addr = s.accept()
    print 'New connection from ', addr
    while True:
        try:
            rc = conn.recv(1024)
            rc=rc.strip()
            if rc.strip() == 'END':
                print "Close"
                conn.send("**END**")
                conn.close()
                break
            else:
                rc = os.system(rc);
                conn.send("This is the result of command: ", rc)
        except Exception:
            conn.close()
            sys.exit()
