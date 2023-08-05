#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
import logging
import os
from typing import Tuple, Dict
from .metrics import iconnector as metrics_iconnector

class ssh(metrics_iconnector):
    def __init__(self,
                 sName: str,
                 sHostname: str,
                 nPort: int,
                 sUser: str,
                 sPassword: str,
                 sKeyfile: str,
                 tLogger = logging.getLogger('SSH')):
        super(ssh, self).__init__()

        self.logger = tLogger
        self.sshclient = paramiko.client.SSHClient()
        #self.sshclient.load_system_host_keys()
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sName = sName
        self.sHostname = sHostname
        self.nPort = nPort
        self.sUser = sUser
        self.sPassword = sPassword
        self.sKeyfile = sKeyfile

    def idstr(self, a_sMsg: str) -> str:
        return "[" + self.sName + "] " + a_sMsg

    def Connect(self):
        try:
            if os.access(self.sKeyfile, os.R_OK):
                self.logger.debug (self.idstr(f"Using private key file {self.sKeyfile}"))
                self.sshclient.connect(hostname     = self.sHostname,
                                       port         = self.nPort,
                                       username     = self.sUser,
                                       key_filename = self.sKeyfile)
            else:
                self.logger.debug (self.idstr("Using password"))
                self.sshclient.connect(hostname = self.sHostname,
                                       port     = self.nPort,
                                       username = self.sUser,
                                       password = self.sPassword)
            self.RunConnectedCallbacks()
        except paramiko.ssh_exception.AuthenticationException:
            self.logger.error (self.idstr("Authentication failed"))
            raise
        except paramiko.ssh_exception.BadHostKeyException:
            self.logger.error (self.idstr("Bad host key"))
            raise
        except paramiko.ssh_exception.SSHException:
            self.logger.error (self.idstr("SSH2 protocol error"))
            raise

    def Disconnect(self):
        self.sshclient.close()
        self.RunDisconnectedCallbacks()

    def ExecCmd(self, a_sCommand: str) -> Tuple[bool, str]: # return ( ExitStatus, Command output )
        try:
            stdin, stdout, stderr = self.sshclient.exec_command(a_sCommand)
            return ( True if (stdout.channel.recv_exit_status() == 0) else False, stdout.read().decode(encoding = "utf-8") )
        except paramiko.ssh_exception.SSHException:
            self.logger.error (self.idstr("SSH2 protocol error"))
            self.Disconnect()
            raise
