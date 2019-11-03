PORT := 5000

open:
	sudo iptables -A INPUT -p tcp -m tcp --dport $(PORT) -j ACCEPT
	sudo systemctl restart iptables

close:
	sudo iptables -A INPUT -p tcp -m tcp --dport $(PORT) -j REJECT
	sudo systemctl restart iptables

mocket: # mock of socket
	socat -d -d pty,raw,echo=0 pty,raw,echo=0
