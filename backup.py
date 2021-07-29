#!/usr/bin/python3

# import modules
import shutil

class Backup(object):
    '''
    Backup a file system object.
    '''

class BackupFile(Backup):
    '''
    Backup a file system file.
    '''

    def __init__(self):
        '''
        class BackupFile constructor

        Set class attributes to initial values.
        '''

        self.prompt = "Backup of file "

    def do_backup(self, src, dst_path):
        '''
        Backup source file to destination.
        '''

        # Copy source file to destination
        shutil.copy2(src, dst_path)

class BackupDirectory(Backup):
    '''
    Backup a file system directory.
    '''

    def __init__(self):
        '''
        class BackupDirectory constructor

        Set class attributes to initial values.
        '''

        self.prompt = "Backup of directory "

    def do_backup(self, src, dst_path):
        '''
        Backup source directory to destination.
        '''

        # Copy source directory to destination
        shutil.copytree(src, dst_path)
