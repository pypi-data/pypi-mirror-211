#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys
import getpass

class cConfig:
    tSSHIdentityDefaultEntry = { "sPassword"            : "",
                                 "sPasswordFromEnv"     : "",
                                 "sPasswordFromTTY"     : False,
                                 "sKeyFile"             : "" }

    # default values for optional host entry key/value pairs
    tHostDefaultEntry = { "bActive"           : True,
                          "nPort"             : int(22),
                          "nScrapeSeconds"    : int(5),
                          "fMemWarnPct"       : float(0.1), # 10%
                          "fSwapWarnPct"      : float(0.1), # 10%
                          "fRootFsWarnPct"    : float(0.1), # 10%
                          "sCustomCmd"        : "",
                          "sCustomCmdLabel"   : "" }

    tWebServerDefaults = { "sLocalAddress"      : "0.0.0.0",
                           "nLocalPort"         : int(8080),
                           "bRestAPIActive"     : False,
                           "bWebsiteActive"     : True,
                           "bLogHttpRequests"   : True,
                           "sDetailsTemplate"   : "details.html",
                           "sOverviewTemplate"  : "overview.html",
                           "nEventLogSize"      : 30,
                           "tEventLogKeys"      : [ ] }

    tMqttDefaults = { "bActive"      : False,
                      "sBroker"      : "",
                      "nPort"        : int(1883),
                      "sUser"        : "",
                      "sPassword"    : "",
                      "sCa_certs"    : "",
                      "sCertfile"    : "",
                      "sKeyfile"     : "",
                      "sTopicPrefx"  : "/ssh-dashboard/hosts/",
                      "nQoS"         : int(0) }

    tInfluxDbDefaults = { "bActive"             : False,
                          "sUrl"                : "",
                          "sOrganization"       : "",
                          "sToken"              : "",
                          "sBucket"             : "",
                          "nTimeout_ms"         : int(10000),
                          "sMeasurement"        : "ssh-dashboard-metrics"
                         }

    def __init__(self):
        # Webserver
        self.tWebserver = cConfig.tWebServerDefaults

        # Mqtt client
        self.tMqtt = cConfig.tMqttDefaults

        # InfluxDb client
        self.tInfluxDbClient = cConfig.tInfluxDbDefaults

        # SSH identities
        self.tIdentities =  {} # dictionary of dictionaries: name -> entry

        # Host list
        self.tHostList = [] # list of dictionaries, one dict per hosts entry

    def ReadFromFile(self, a_sFilename: str):
        self.tIdentities = {}
        self.tHostList = []
        try:
            with open(a_sFilename, "r") as f:
                configfile = json.load(f)

            # Webserver
            if "webserver" in configfile:
                if "localaddress"       in configfile["webserver"]                  : self.tWebserver["sLocalAddress"]    = configfile["webserver"]["localaddress"]
                if "localport"          in configfile["webserver"]                  : self.tWebserver["nLocalPort"]       = int(configfile["webserver"]["localport"])
                if "restapi_active"     in configfile["webserver"]                  : self.tWebserver["bRestAPIActive"]   = bool(configfile["webserver"]["restapi_active"])
                if "website_active"     in configfile["webserver"]                  : self.tWebserver["bWebsiteActive"]   = bool(configfile["webserver"]["website_active"])
                if "log_http_requests"  in configfile["webserver"]                  : self.tWebserver["bLogHttpRequests"] = bool(configfile["webserver"]["log_http_requests"])
                if "html_templates"     in configfile["webserver"]:
                    if "details_template"   in configfile["webserver"]["html_templates"]: self.tWebserver["sDetailsTemplate"]  = configfile["webserver"]["html_templates"]["details_template"]
                    if "overview_template"  in configfile["webserver"]["html_templates"]: self.tWebserver["sOverviewTemplate"] = configfile["webserver"]["html_templates"]["overview_template"]
                if "eventlog"           in configfile["webserver"]:
                    if "logsize"            in configfile["webserver"]["eventlog"]:  self.tWebserver["nEventLogSize"] = int(configfile["webserver"]["eventlog"]["logsize"])
                    if "keys"               in configfile["webserver"]["eventlog"]:  self.tWebserver["tEventLogKeys"] =     configfile["webserver"]["eventlog"]["keys"]
                if not isinstance(self.tWebserver["tEventLogKeys"], list): raise TypeError("eventlog keys needs to be a list of strings")

            # Mqtt client
            if "mqttclient" in configfile:
                if "active"        in configfile["mqttclient"]: self.tMqtt["bActive"]      = bool(configfile["mqttclient"]["active"])
                if "broker"        in configfile["mqttclient"]: self.tMqtt["sBroker"]      = configfile["mqttclient"]["broker"]
                if "port"          in configfile["mqttclient"]: self.tMqtt["nPort"]        = int(configfile["mqttclient"]["port"])
                if "user"          in configfile["mqttclient"]: self.tMqtt["sUser"]        = configfile["mqttclient"]["user"]
                if "password"      in configfile["mqttclient"]: self.tMqtt["sPassword"]    = configfile["mqttclient"]["password"]
                if "ca_certs"      in configfile["mqttclient"]: self.tMqtt["sCa_certs"]    = configfile["mqttclient"]["ca_certs"]
                if "certfile"      in configfile["mqttclient"]: self.tMqtt["sCertfile"]    = configfile["mqttclient"]["certfile"]
                if "keyfile"       in configfile["mqttclient"]: self.tMqtt["sKeyfile"]     = configfile["mqttclient"]["keyfile"]
                if "topicprefix"   in configfile["mqttclient"]: self.tMqtt["sTopicPrefix"] = configfile["mqttclient"]["topicprefix"]
                if "qos"           in configfile["mqttclient"]: self.tMqtt["nQoS"]         = int(configfile["mqttclient"]["qos"])

            # InfluxDb client
            if "influxdbclient" in configfile:
                if "active"             in configfile["influxdbclient"]: self.tInfluxDbClient["bActive"]       = bool(configfile["influxdbclient"]["active"])
                if "url"                in configfile["influxdbclient"]: self.tInfluxDbClient["sUrl"]          = configfile["influxdbclient"]["url"]
                if "organization"       in configfile["influxdbclient"]: self.tInfluxDbClient["sOrganization"] = configfile["influxdbclient"]["organization"]
                if "token"              in configfile["influxdbclient"]: self.tInfluxDbClient["sToken"]        = configfile["influxdbclient"]["token"]
                if "bucket"             in configfile["influxdbclient"]: self.tInfluxDbClient["sBucket"]       = configfile["influxdbclient"]["bucket"]
                if "timeout_ms"         in configfile["influxdbclient"]: self.tInfluxDbClient["nTimeout_ms"]   = int(configfile["influxdbclient"]["timeout_ms"])
                if "measurement_name"   in configfile["influxdbclient"]: self.tInfluxDbClient["sMeasurement"]  = configfile["influxdbclient"]["measurement_name"]

            # TODO: provide default values for non-necessary settings
            # only name, host, password and/or private key should always be there

            # Identity list
            identities = configfile["identities"]

            # check for duplicate identities
            identitynames = []
            for i in identities: identitynames.append(i["name"])
            if len(identitynames) != len(set(identitynames)): raise ValueError("No duplicate identity names allowed")

            # fill identity dict
            for i in identities:
                tNewEntry = { "sName"       : i["name"], # TODO: remove name? already used as key...
                              "sUser"       : i["ssh_user"] }
                # optional values - set default values first, then overwrite with values from configuration file, if present
                tNewEntry.update(cConfig.tSSHIdentityDefaultEntry)
                if "ssh_password"                   in i: tNewEntry["sPassword"]        = i["ssh_password"]
                if "ssh_read_password_from_env"     in i: tNewEntry["sPasswordFromEnv"] = i["ssh_read_password_from_env"]
                if "ssh_read_password_from_tty"     in i: tNewEntry["sPasswordFromTTY"] = bool(i["ssh_read_password_from_tty"])
                if "ssh_privatekeyfile"             in i: tNewEntry["sKeyFile"]         = i["ssh_privatekeyfile"]

                #  check if password should be BOTH read from environment and console - raise error in case, only one should be set
                if len(tNewEntry["sPasswordFromEnv"]) and (tNewEntry["sPasswordFromTTY"] == True): raise KeyError(f"Identity {tNewEntry['sName']} requests reading password from environment AND from tty - only one can be chosen")

                # read password from environment variable if variable name is non-empty
                if tNewEntry["sPasswordFromEnv"] and (not tNewEntry["sPasswordFromEnv"] in os.environ): raise KeyError(f"Requested reading password from environment ({tNewEntry['sPasswordFromEnv']}), but variable is not set.")
                if tNewEntry["sPasswordFromEnv"]: tNewEntry["sPassword"] = os.environ.get(tNewEntry["sPasswordFromEnv"])

                # read password from console if needed
                try:
                    if tNewEntry["sPasswordFromTTY"]:
                        if not sys.stdin.isatty(): raise Exception("Reading password from tty requested, but stdin is not attached to a tty")
                        tNewEntry["sPassword"] = getpass.getpass(prompt=f'Input SSH password for identity \"{tNewEntry["sName"]}\": ')
                except getpass.GetPassWarning as e:
                    raise

                # add entry
                self.tIdentities[tNewEntry["sName"]] = tNewEntry

            # Host list
            hostlist = configfile["hosts"]

            # check for duplicate host names
            thostnames = []
            for i in hostlist: thostnames.append(i["name"])
            if len(thostnames) != len(set(thostnames)): raise ValueError("No duplicate hostnames allowed")

            # fill list
            for i in hostlist:
                # mandatory values
                tNewEntry = { "sName"             : i["name"],
                              "sIdentity"         : i["identity"],
                              "sHost"             : i["host"] }
                # check if chosen identity exists
                if not tNewEntry["sIdentity"] in self.tIdentities: raise ValueError("Unknown identity: " + tNewEntry["sIdentity"])

                # optional values - set default values first, then overwrite with values from configuration file, if present
                tNewEntry.update(cConfig.tHostDefaultEntry)
                if "active" in i:                   tNewEntry["bActive"]          = bool(i["active"])
                if "ssh_port" in i:                 tNewEntry["nPort"]            = int (i["ssh_port"])
                if "scrape_interval_s" in i:        tNewEntry["nScrapeSeconds"]   = int(i["scrape_interval_s"])
                if "memory_warning_percent" in i:   tNewEntry["fMemWarnPct"]      = float(i["memory_warning_percent"])
                if "swap_warning_percent" in i:     tNewEntry["fSwapWarnPct"]     = float(i["swap_warning_percent"])
                if "rootfs_warning_percent" in i:   tNewEntry["fRootFsWarnPct"]   = float(i["rootfs_warning_percent"])
                if "customcmd" in i:                tNewEntry["sCustomCmd"]       = i["customcmd"]
                if "customcmdlabel" in i:           tNewEntry["sCustomCmdLabel"]  = i["customcmdlabel"]
                # add entry
                self.tHostList.append(tNewEntry)

        except Exception as e:
            self.tIdentities = {}
            self.tHostList = []
            raise
            #if hasattr(e, "message"): return (False, "Error reading " + a_sFilename + ": " + e.message)
            #else:                     return (False, e.__str__())
