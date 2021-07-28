#!/usr/bin/python3

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
