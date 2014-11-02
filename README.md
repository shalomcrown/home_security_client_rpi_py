home_security_client_rpi_py
===========================

Python homesec client for Raspberry Pi

This is supposed to be the client side of the Homesec project.

What it currently does:
* Takes still pictures, stores them in /tmp as time-stamped files
* Has TCK login dialog for server

What needs developing:
* Compare pictures using imagemagick (one of the Python bindings if possible) and discard the old one 
  if insufficient change
* If there is a change, send pictures to server - which will alret user etc.

What might be good as an intermediate step:
* If there's a change - mail pictures to user.
* This will require a dialog for user's mail account (which will be used to send from and can 
  be assumed to be same as destination account).
