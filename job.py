#!/usr/bin/python3

# import modules
import pathlib
import smtplib
import os
from datetime import datetime

class Job(object):
    '''
    Individual job details.
    '''

    def __init__(self, *args):
        '''
        class Job constructor

        Set class attributes to initial values.

        Parameters:
            args[0]: job name
            args[1]: source file or directory
            args[2]: destination directory
        '''

        self.name = args[0]
        self.src = args[1]
        self.dst = args[2]

        self.errors = 0
        self.message = []
        self.datestring = datetime.now().strftime("%Y%m%d-%H%M%S")

        # Determine type of backup job
        self.is_file_job = pathlib.Path(self.src).is_file()
        self.is_dir_job = pathlib.Path(self.src).is_dir()

        # Check job source and destination paths exist
        if not os.path.exists(self.src):
            self.message.append("Source " + self.src + " does not exist -> FAIL")
            self.errors += 1

        if not os.path.exists(self.dst):
            self.message.append("Destination directory " + self.dst + " does not exist -> FAIL")
            self.errors += 1

    def __eq__(self, other):
        '''
        Return:
            True when other is name
        '''

        return other == self.name

    def do_logfile(self, logfile):
        '''
        Output all log messages to logfile.
        '''

        file = open(logfile, "a")
        for msg in self.message:
            logmsg = self.datestring + " " + self.name + " " + msg
            file.write(logmsg + "\n")
        file.close()

    def do_email(self, email_config):
        '''
        Output all log message as email.
        '''
        
        header = 'To: ' + email_config.recipient + '\n' + 'From: ' + email_config.user + '\n' + 'Subject: Backup Error ' + self.name + '\n'
        msg = header + '\n'
        
        for item in self.message:
            msg = msg + item + '\n'
        msg = msg + '\n\n'

        smtpserver = smtplib.SMTP(email_config.server, email_config.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(email_config.user, email_config.pwd)
        smtpserver.sendmail(email_config.user, email_config.recipient, msg)
        smtpserver.quit()

    def do_backup(self, backup):
        '''
        Backup file system object to destination.
        '''

        # Construct source and destination paths
        #src_path = pathlib.Path(self.src)
        src_path_only = pathlib.PurePath(self.src)
        dst_path = self.dst + "/" + src_path_only.name + "-" + self.datestring

        # Copy file system object to destination
        try:
            backup.do_backup(self.src, dst_path)
            self.message.append(backup.prompt + self.src + " -> SUCCEED")
        except:
            self.message.append(backup.prompt + self.src + " -> FAIL")
            self.errors += 1
