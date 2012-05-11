#!/usr/bin/env python2

import sys
import urllib
import pynotify
import os
import time

from ConfigParser import ConfigParser
from os import getenv
from os.path import join


def parse_credentials(cred_file):
    cred_file = os.path.expanduser(cred_file)
    if not os.path.isfile(cred_file):
        print "ERROR: %s not found" % cred_file
        sys.exit(1)

    with open(cred_file) as f:
        login = f.read()

    login.strip()
    login = login.split("\n")
    # remove empty elements
    login = filter(lambda x: len(x) > 0, login)

    if len(login) != 2:
        print "ERROR: invalid credentials"
        sys.exit(1)

    return login




def mail_count(msg):
    begin = msg.find("<fullcount>")
    end = msg.find("</fullcount>")
    return msg[begin+12:end]


def titles(msg):
    begin = msg.find("<title>")
    end = msg.find("</title>")

    t = []

    while begin > 0:
        t.append(msg[begin+len("<title>"):end])
        begin = msg.find("<title>", begin + len("<title>"))
        end = msg.find("</title>", end + len("</title>"))

    return t

def run(config, boxes):
    sleep = config.getint("options", "sleep")
    while True:
        for box in boxes:
            box.update()
        time.sleep(sleep * 60)


class Inbox(object):
    def __init__(self, name, config, urgency=pynotify.URGENCY_NORMAL, sound = None):
        self.name = name
        self.config = config
        self.urgency = urgency
        self.sound = sound
        self.known_mails = []

    def get_feed(self):
        user = self.config.get('credentials', 'username')
        password = self.config.get('credentials', 'password')
        url = "https://%s:%s@mail.google.com/mail/feed/atom/%s" % (user,
                password, self.name)
        msg = urllib.urlopen(url).read()
        return msg

    def update(self):
        msg = self.get_feed()
        summaries = titles(msg)[1:]
        new = []

        for s in summaries:
            if s not in self.known_mails:
                self.known_mails.append(s)
                new.append(s)

        # remove mails from self.known_mails after
        # they aren't in the feed anymore
        # otherwise replies with the same subject won't begin
        # recognized as new mail
        for s in self.known_mails:
            if s not in summaries:
                self.known_mails.remove(s)


        for s in new:
            n = pynotify.Notification("New Mail (%s) " % self.name, s)
            n.set_urgency(self.urgency)
            n.show()

        if len(new) > 0 and self.sound:
            com = "aplay %s" % self.sound
            os.popen(com)

def prompt_password(config):
    import Tkinter as tk

    root = tk.Tk()

    def set_pw():
        pw = pw_entry.get()
        config.set('credentials', 'password', pw)
        root.destroy()


    label1 = tk.Label(root, text="Enter password for %s: " %
            config.get('credentials', 'username'))
    pw_entry = tk.Entry(root, show="*")
    pw_entry.focus_set()
    button = tk.Button(root, text='OK', command=set_pw)

    # simple widget layout, stack vertical
    label1.pack(pady=2)
    pw_entry.pack(pady=5)
    button.pack(pady=5)

    # start the event loop
    root.mainloop()
    return config


def main():
    pynotify.init("gmailnotify.py")

    urgencies = {}
    urgencies['low'] = pynotify.URGENCY_CRITICAL
    urgencies['normal'] = pynotify.URGENCY_NORMAL
    urgencies['critical'] = pynotify.URGENCY_CRITICAL

    config = ConfigParser()
    files = (join(getenv("XDG_CONFIG_HOME"), "gmailnotify.conf"),
             join(getenv("HOME"), "gmailnotify.conf"))
    config.read(files)

    if config.has_option('credentials', 'file'):
        user, password = parse_credentials(config.get('credentials',
            'file'))
        config.set('credentials', 'username', user)
        config.set('credentials', 'password', password)

    if config.get('credentials', 'password') == 'prompt':
        config = prompt_password(config)


    boxes = []

    for section in config.sections():
        if section != 'credentials' and section != 'options':
            if config.has_option(section, 'sound'):
                sound = config.get(section, 'sound')
            else:
                sound = None

            if config.has_option(section, 'urgency'):
                urgency = urgencies[config.get(section, 'urgency')]
            else:
                urgency = urgencies['normal']

            boxes.append(Inbox(section, config, urgency, sound))

    run(config, boxes)

if __name__ == '__main__':
    main()
