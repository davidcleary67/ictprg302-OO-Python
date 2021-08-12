#!/usr/bin/python3

# import modules

from emailconfig import EmailConfig
from job import Job

# constants

usage_msg = 'Usage: python backup.py <job_name>'
    
job_msg = 'Invalid job number.  Job number not in list of jobs.'
    
logfile = '/home/ec2-user/environment/backupoo/backupoo.log'

# EmailConfig object
email_config = EmailConfig('dcleary@sunitafe.edu.au',
                           'dcleary@sunitafe.edu.au',
                           'xxxxxxxx',
                           'mail.example.com',
                           587)

# array of Job objects
jobs = [Job('job1', '/home/ec2-user/environment/backupoo/test/dir1', '/home/ec2-user/environment/backupoo/backup'),
        Job('job2', '/home/ec2-user/environment/backupoo/test/file1','/home/ec2-user/environment/backupoo/backup'),
        Job('job3', '/home/ec2-user/environment/backupoo/test/fileX','/home/ec2-user/environment/backupoo/backup'),
        Job('job4', '/home/ec2-user/environment/backupoo/test/file1','/home/ec2-user/environment/backupoo/backupX')]

