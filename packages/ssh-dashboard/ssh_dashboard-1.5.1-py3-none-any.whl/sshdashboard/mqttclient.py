#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
import paho.mqtt.client

class cMqttClient:

    tConResult = { 1 : "incorrect protocol version",
                   2 : "invalid client identifier",
                   3 : "server unavailable",
                   4 : "bad username or password",
                   5 : "not authorized" }

    def __init__(self,
                 a_sBroker: str = "",
                 a_nPort: int = 1883,
                 a_sUser: str = "",
                 a_sPassword: str = "",
                 a_sCa_certs: str = "",
                 a_sCertfile: str = "",
                 a_sKeyfile: str = "",
                 a_sTopicPrefix: str = "",
                 a_tLogger = logging.getLogger('MQTT')):

        self.sBroker = a_sBroker
        self.nPort = a_nPort
        self.sUser = a_sUser
        self.sPassword = a_sPassword
        self.sTopicPrefix = a_sTopicPrefix
        self.sCa_certs = None
        self.sCertfile = None
        self.sKeyfile = None
        if a_sCa_certs: self.sCa_certs = a_sCa_certs
        if a_sCertfile: self.sCertfile = a_sCertfile
        if a_sKeyfile:  self.sKeyfile  = a_sKeyfile

        self.tClient = paho.mqtt.client.Client()
        self.tClient.on_connect = self._on_connect
        self.tClient.on_disconnect = self._on_disconnect

        self.bConnected = False
        self.logger = a_tLogger

    def idstr(self, a_sMsg: str) -> str:
        return "[" + self.sBroker + "] " + a_sMsg

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.bConnected = True
            self.logger.info (self.idstr("Connected"))
        else:
            self.bConnected = False
            if rc in cMqttClient.tConResult:
                self.logger.error (self.idstr("Connection failed: " + cMqttClient.tConResult[rc]))
            else:
                self.logger.error (self.idstr("Connection failed: unkown reason"))

    def _on_disconnect(self, client, userdata, rc):
        self.bConnected = False
        if rc == 0:
            self.logger.info (self.idstr("Cleanly disconnected"))
        else:
            self.logger.warning (self.idstr("Unexpectedly disconnected"))

    def start(self):
        # set tls options
        if self.sCa_certs != None:  # ca certs given
            if self.sCertfile and self.sKeyfile:
                self.tClient.tls_set(ca_certs=self.sCa_certs, certfile=self.sCertfile, keyfile=self.sKeyfile)
            else:
                self.tClient.tls_set(ca_certs=self.sCa_certs)
        else:                       # no ca certs given
            if self.sCertfile and self.sKeyfile:
                self.tClient.tls_set(certfile=self.sCertfile, keyfile=self.sKeyfile)
            else:
                pass
        # set username and password
        self.tClient.username_pw_set(self.sUser, self.sPassword)
        # connect to server
        if self.sBroker:
            self.tClient.connect(self.sBroker, self.nPort)
            self.tClient.loop_start()

    def stop(self):
        self.tClient.disconnect()
        self.tClient.loop_stop()

    def publish(self, a_sTopic: str, a_sMessage: str, a_nQoS: int = 0) -> bool:
        if not self.bConnected: return False
        sTopic = self.sTopicPrefix + a_sTopic
        tMessageInfo = self.tClient.publish(sTopic, a_sMessage, a_nQoS)
        if tMessageInfo.rc == 0:
            self.logger.debug (self.idstr("Published to " + sTopic))
            return True
        else:
            self.logger.error (self.idstr("Error while trying to publish " + sTopic))
            return False

# if __name__ == '__main__':
#     client = cMqttClient(a_sBroker = "localhost", a_sTopicPrefix = "/foo/")
#     client.start()
#     time.sleep(5)
#     if client.publish("bar/", "Hello world") == False: print ("Error publishing")
#     client.stop()
