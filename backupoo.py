#!/usr/bin/python3

# import modules
import sys
from emailconfig import EmailConfig
from job import Job
from backup import Backup, BackupFile, BackupDirectory

def main():
    '''
    Execute backup job from job list with a name matching the first command line argument.
    '''
    # Constants
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

    # check for correct number of command line arguments
    if len(sys.argv) != 2:

        print(usage_msg)

    else:

        # if job number from command line in jobs list then perform backup job
        job_name = sys.argv[1]

        if job_name not in jobs:

            print(job_msg)

        else:

            job = jobs[jobs.index(job_name)]


            # determine the job type
            if job.is_file_job:

                backup = BackupFile()

            elif job.is_dir_job:

                backup = BackupDirectory()

            # perform backup
            if not job.errors:
                job.do_backup(backup)

            # send errors as email
            if job.errors:
                pass
                # job.do_email(email_config)

            # record result in logfile
            job.do_logfile(logfile)

if __name__ == '__main__':
    main()

