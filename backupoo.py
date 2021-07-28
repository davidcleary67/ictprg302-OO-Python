#!/usr/bin/python3

# import modules
import sys, os, pathlib, shutil, smtplib
from datetime import datetime
# from backupcfg import jobs, logfile, usage_msg, job_msg, recipient, email_user, email_pwd, server, port

class EmailConfig(object):
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

class Backup(object):
    '''
    Backup a file system object.
    '''

    def __init__(self, *args):
        '''
        class Backup constructor

        Set class attributes to initial values.

        Parameters:
            args[0]: formatted datetime string
            args[1]: number errors
            args[2]: messages
        '''
        
        self.job = args[0]
        self.logfile = args[1]
        self.email_config = args[2]

class BackupFile(Backup):
    '''
    Backup a file system file.
    '''

    def do_backup(self):
        '''
        Backup source file to destination.
        '''

        # Local variables to shorten code
        src = self.job.src
        dst = self.job.dst
        
        # Construct source and destination paths
        src_path = pathlib.Path(src)
        src_path_only = pathlib.PurePath(src)
        dst_path = dst + "/" + src_path_only.name + "-" + self.job.datestring

        # Copy source file to destination
        try:
            shutil.copy2(src, dst_path)
            self.job.message.append("Backup of file " + src + " -> SUCCEED")
        except:
            self.job.message.append("Backup of file " + src + " -> FAIL")
            self.job.errors += 1

class BackupDirectory(Backup):
    '''
    Backup a file system .
    '''

    def do_backup(self):
        '''
        Backup source directory to destination.
        '''

        # Local variables to shorten code
        src = self.job.src
        dst = self.job.dst
        
        # Construct source and destination paths
        src_path = pathlib.Path(src)
        src_path_only = pathlib.PurePath(src)
        dst_path = dst + "/" + src_path_only.name + "-" + self.job.datestring

        # Copy source directory to destination
        try:
            shutil.copytree(src, dst_path)
            self.job.message.append("Backup of directory " + src + " -> SUCCEED")
        except:
            self.job.message.append("Backup of directory " + src + " -> FAIL")
            self.job.errors += 1

#  main routine
if __name__ == '__main__':

    email_config = EmailConfig('dcleary@sunitafe.edu.au',
                               'dcleary@sunitafe.edu.au',
                               'xxxxxxxx',
                               'mail.example.com',
                               587)

    jobs = [Job('job1', '/home/ec2-user/environment/backupoo/test/dir1', '/home/ec2-user/environment/backupoo/backup'),
            Job('job2', '/home/ec2-user/environment/backupoo/test/file1','/home/ec2-user/environment/backupoo/backup'),
            Job('job3', '/home/ec2-user/environment/backupoo/test/fileX','/home/ec2-user/environment/backupoo/backup'),
            Job('job4', '/home/ec2-user/environment/backupoo/test/file1','/home/ec2-user/environment/backupoo/backupX')]

    usage_msg = 'Usage: python backup.py <job_name>'
    
    job_msg = 'Invalid job number.  Job number not in list of jobs.'
    
    logfile = '/home/ec2-user/environment/backupoo/backupoo.log'

    if len(sys.argv) != 2:

        print(usage_msg)

    else:

        job_name = sys.argv[1]

        # if valid job then backup job
        if job_name not in jobs:

            print(job_msg)

        else:

            job = jobs[jobs.index(job_name)]

            if job.is_file_job:
            
                backup = BackupFile(job, logfile, email_config)

            elif job.is_dir_job:

                backup = BackupDirectory(job, logfile, email_config)

            if not job.errors:
                backup.do_backup()

            if job.errors:
                pass
            # job.do_email(email_config)

            job.do_logfile(logfile)
