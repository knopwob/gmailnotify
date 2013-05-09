Checkgmail
==========

Checkgmail notifies you about new emails using libnotify.

IMPORTANT
---------

Please note that this project is abandoned. Pull request might still get merged but
there will be no active developement besides that.

running
-------

The easiest way to run this is to add "gmailnotify.py &" to your .xinitrc before
you exec to your window manager.

configuration
-------------

The configuration file has to be saved as "$XDG_CONFIG_HOME/gmailnotify.conf" or
"/home/knopwob/.config/gmailnotify.conf" which on most systems should be the same.

example ::

    [credentials]
    # points to a file containing two lines: username and password
    #file = ./gmaillogin
    #or
    #username = 1337hax0r
    #password = topsecret
    #or to be prompted for the password
    #username = 1337hax0r
    #password = prompt

    [options]
    sleep = 10

    [INBOX]
    sound = ~/.sounds/gotmail00.wav
    urgency = critical

    [Archlinux]
    urgency = normal

    [suckless]
    urgency = normal

    [facebook]
    urgency = normal

credentials
-----------
Your gmail login credentials.

options
-------
-sleep = N
    -check for new emails everey N minutes

mailboxes
---------
Every section that is not 'credentials' or 'options' is
interpreted as a mailbox/label to be checked for new mails.

-urgency = low/normal/critical
    -the urgency of the notification
-sound = file
    play file on new email
