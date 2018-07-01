## Multiple processes on dash

This repository contains a simple Dash app that run multi-processes. A random number is generated and then saved to local pickle file. Another process of live updating is reading from the local pickle file and output result to dash html layout. 

It works fine on local host. A random number is generated and saved to a local file. In parrallel, the dash app is reading latest result from that local pickle file and live updateing that to a html text. 

When deployed onto on-premise server, no error is shown but the number is not being updated. 
