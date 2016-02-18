INSTALL
=======

To install, set up a plivo account, run the servers via start-algo.sh
and then send the servers commands via init.py

Sample control files are in algobroker/test

This installation does a simple scan of the quotes from yahoo and
sends out an sms message if it hits certain limits.

-------
servers are init by sending control messages

init.py.example contains a example setup configuration.  In order to
interface with bitmex replace control message with bitmex API key.
