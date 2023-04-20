#!/usr/bin/python3

# import modules

import sys
from emailconfig import EmailConfig
from job import Job
from backup import Backup, BackupFile, BackupDirectory
from backupcfg import job_msg, usage_msg, logfile, email_config, jobs

# constants
usageMsg = 'Usage: python backup.py <job_name>'
jobMsg = 'Invalid job name.  Job name not in list of jobs.'

def main():
    '''
    Execute backup job from job list with a name matching the first command line argument.
    '''

    # check for correct number of command line arguments
    if len(sys.argv) != 2:

        print(usageMsg)

    else:

        # if job number from command line in jobs list then perform backup job
        job_name = sys.argv[1]

        if job_name not in jobs:

            print(jobMsg)

        else:

            job = jobs[jobs.index(job_name)]

            # determine the type of backup to perform based upon job type
            backup = BackupFile() if job.is_file_job else BackupDirectory() 

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

