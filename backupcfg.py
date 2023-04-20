#!/usr/bin/python3

# import modules

from emailconfig import EmailConfig
from job import Job

# log file    
logFile = '/home/ec2-user/environment/backupoo/backupoo.log'

# backup directory
backupDir = 'backup'

# EmailConfig object
emailConfig = EmailConfig('dcleary@sunitafe.edu.au',
                          'dcleary@sunitafe.edu.au',
                          'xxxxxxxx',
                          'mail.example.com',
                          587)

# array of Job objects
jobs = [Job('job1', 'test/dir1', backupDir),
        Job('job2', 'test/file1', backupDir),
        Job('job3', 'test/fileX', backupDir),
        Job('job4', 'test/file1', backupDir)]
