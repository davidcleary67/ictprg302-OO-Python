#!/usr/bin/python3

# import modules
import sys, os, pathlib, shutil, smtplib
from datetime import datetime
# from backupcfg import jobs, logfile, usage_msg, job_msg, recipient, email_user, email_pwd, server, port

class EmailConfig:
'''
Individual Email configuration details.
'''
    def __init__(self, *args):
        '''
        class EmailConfig constructor

        Set class attributes to initial values.

        Parameters:
            args[0]: email address of recipient
            args[1]: email address of user
            args[2]: pwd
            args[3]: server
            args[4]: port
        '''
        
        self.recipient  = args[0] 
        self.user = args[1] 
        self.pwd = args[2] 
        self.server = args[3]
        self.port = args[4] 

class Job(object):

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

    def __eq__(self, other):
        '''
        Return:
            True when other is name
        '''

        return other == self.name

class Backup:

    def __init__(self, *args):
        '''
        class Backup constructor

        Set class attributes to initial values.

        Parameter count:
            0: set attributes to defaults
            3: set attributes to args[]

        Parameters:
            args[0]: formatted datetime string
            args[1]: number errors
            args[2]: messages
        '''
        
        self.datestring = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.errors = 0
        self.message = []
        self.backed_up = False

        if len(args) == 0:
            self.job = 0
            self.logfile = "./backup.log"
            self.email_config = None

        elif len(args) == 3:
            self.job = args[0]
            self.logfile = args[1]
            self.email_config = args[2]

    def do_logfile(self):
        '''
        Output all log messages to logfile.
        '''

        file = open(self.logfile,"a")
        for msg in self.message:
            logmsg = self.datestring + " " + self.job + " " + msg
            file.write(logmsg + "\n")
        file.close()

    def do_email(self):
        '''
        Output all log message as email.
        '''
        
        header = 'To: ' + self.email_config.recipient + '\n' + 'From: ' + self.email_config.user + '\n' + 'Subject: Backup Error ' + self.job + '\n'
        msg = header + '\n'
        
        for item in message:
            msg = msg + item + '\n'
        msg = msg + '\n\n'

        smtpserver = smtplib.SMTP(self.email_config.server, self.email_config.port)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(self.email_config.user, self.email_config.pwd)
        smtpserver.sendmail(self.email_config.user, self.email_config.recipient, msg)
        smtpserver.quit()
        
email_config = EmailConfig('mhall@sunitafe.edu.au',
                           'mhall@sunitafe.edu.au',
                           'xxxxxxxx',
                           'mail.example.com',
                           587)

jobs = [Job('job1', '/home/ec2-user/environment/ictnwk409-class/data/dir1', '/home/ec2-user/environment/ictnwk409-class/data/dir2'),
        Job('job2', '/home/ec2-user/environment/ictnwk409-class/data/file1','/home/ec2-user/environment/ictnwk409-class/data/dir2'),
        Job('job3', '/home/ec2-user/environment/backup/dir5','/home/ec2-user/environment/backup/dir6')]

usage_msg = 'Usage: python backup.py <job_name>'

logfile = '/home/ec2-user/environment/ictnwk409-class/backup.log'

'''
b = Backup(34, "./NewLog.log", email_config);
c = Backup();

print(b.datestring)
print(b.job)
print(b.logfile)
print(b.email_config.recipient)
print(c.datestring)
print(c.job)
print(c.logfile)
print(jobs[0].name)
print('job6' in jobs)
print(jobs.index('job3'))
'''

backup = Backup(jobs[jobs.index('job2')], logfile, email_config)
print(backup.job.name)
print(backup.job.src)
print(backup.job.dst)


if __name__ == '__main__':

    if len(sys.argv) != 2:

        print(usage_msg)

    else:

        job_name = sys.argv[1]

        # check if a job named job_name is in the list of jobs
        if job_name not in jobs:

            print(job_msg)

        else:
            
            backup = Backup(jobs.index(job_name), logfile, email_config)

            print(backup.job.name)
            
            #backup.do_backup()

            if backup.errors != 0:
                pass
                # backup.do_email()

            # backup.do_logfile(job)
