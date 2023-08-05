#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import threading
import time
import datetime
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from .systeminfoentry import cEntry as systeminfoentry_cEntry
from .observerbase import cSubjectBase as observerbase_cSubjectBase

class iconnector(ABC):
    def __init__(self):
        self._ConnectedCallbacks = []
        self._DisconnectedCallbacks = []
    @abstractmethod
    def Connect(self):
        pass
    @abstractmethod
    def Disconnect(self):
        pass
    @abstractmethod
    def ExecCmd(self, a_sCommand: str) -> Tuple[bool, str]: # return ( ExitStatus, Command output )
        pass
    def AddConnectedCallback(self, a_tCallback):
        if (callable(a_tCallback)): self._ConnectedCallbacks.append(a_tCallback)
        else                      : raise TypeError("DisconnectedCallback needs to be a callable")
    def AddDisconnectedCallback(self, a_tCallback):
        if (callable(a_tCallback)): self._DisconnectedCallbacks.append(a_tCallback)
        else                      : raise TypeError("ConnectedCallback needs to be a callable")
    def RunConnectedCallbacks(self):
        for i in self._ConnectedCallbacks: i(self)
    def RunDisconnectedCallbacks(self):
        for i in self._DisconnectedCallbacks: i(self)


class collectorthread(threading.Thread, observerbase_cSubjectBase):
    # These lists are for probing the remote host where the needed executables are located.
    # The first command from each list which succeeds during probing will be used for scraping host metrics.
    cmd_df      = ["/bin/df", "/usr/bin/df", "/usr/bin/env df", "df"]
    cmd_lscpu   = ["/bin/lscpu", "/usr/bin/lscpu", "/usr/bin/env lscpu", "lscpu"]
    cmd_cat     = ["/bin/cat", "/usr/bin/cat", "/usr/bin/env cat", "cat"]

    probe_df = { "name": "df",
                 "probe_arguments": " --version",
                 "probe_cmd_candidates": cmd_df }

    probe_lscpu = { "name": "lscpu",
                    "probe_arguments": " --version",
                    "probe_cmd_candidates": cmd_lscpu }

    probe_cat = { "name": "cat",
                  "probe_arguments": " --version",
                  "probe_cmd_candidates": cmd_cat }

    probelist = [probe_df, probe_lscpu, probe_cat]

    def __init__(self,
                 tHostInfo: Dict,
                 tConnector: iconnector = None,
                 nCyclicReconnect = 1000,
                 nWaitAfterDisconnect = 5,
                 tLogger = logging.getLogger('Collector')):
        #super().__init__()
        threading.Thread.__init__(self)
        observerbase_cSubjectBase.__init__(self)

        self.nCyclicReconnect = nCyclicReconnect
        self.nCyclesSinceConnect = 0
        self.nWaitAfterDisconnect = nWaitAfterDisconnect
        self.tHostInfo = tHostInfo
        self.bExitThread = threading.Event()
        self.bExitThread.clear()
        self.connector = tConnector
        self.lastcontact = "never"
        self.timestamp = 0

        self.onetimeinfoscraped = False
        self.numcpus = 0
        self.ostype = "unknown"
        self.osversion = ""
        self.cpuvendor = "n/a"
        self.cpumodel = "n/a"

        self.logger = tLogger

        self.cmds = { "df":     None,
                      "lscpu":  None,
                      "cat":    None}

    def signal_exitthread(self):
        self.bExitThread.set()

    def handlecyclicreconnect(self):
        # paramiko does not cope well with long-running sessions (slow memory leak)
        # so we reconnect every now and then...
        self.nCyclesSinceConnect += 1
        if self.nCyclesSinceConnect > self.nCyclicReconnect:
            self.logger.debug (self.idstr("Cyclic reconnect..."))
            self.connector.Disconnect()
            self.connectotarget()
            self.nCyclesSinceConnect = 0

    def connectotarget(self):
        self.connector.Connect()
        self.probeallremotecommands()
        self.onetimeinfoscraped = False

    def probeallremotecommands(self):
        for i in collectorthread.probelist: self.probecommand(i)
        self.logger.debug(self.idstr(f"Using remote commands: {self.cmds}"))
        for key, value in self.cmds.items():
            if not value: self.logger.warning(self.idstr(f"Could not find suitable '{key}' command, some metrics will NOT be available"))

    def probecommand(self, cmd: dict):
        try:
            for i in cmd["probe_cmd_candidates"]:
                commandok, out = self.connector.ExecCmd(i + cmd["probe_arguments"])
                if commandok:
                    self.cmds[cmd["name"]] = i
                    break
        except Exception as e:
            self.logger.error(self.idstr("Error while probing: " + str(e)))

    def scrapeuptime(self, infoentry):
        if self.cmds["cat"]:
            commandok, out = self.connector.ExecCmd(self.cmds["cat"] + ' /proc/uptime')
            try:
                uptime_split = out.split(' ')
                infoentry.SetUptime(float(uptime_split[0]))
            except Exception as e:
                self.logger.error(self.idstr("Error evaluating uptime: " + str(e)))

    def scrapeloadavg(self, infoentry):
        if self.cmds["cat"]:
            commandok, out = self.connector.ExecCmd(self.cmds["cat"] + ' /proc/loadavg')
            try:
                loadavg = out.split(' ')
                sysload_1min = float(loadavg[0])
                sysload_5min = float(loadavg[1])
                sysload_15min = float(loadavg[2])
                infoentry.SetSysLoad(sysload_1min, sysload_5min, sysload_15min)
            except Exception as e:
                self.logger.error(self.idstr("Error evaluating loadavg: " + str(e)))

    def scrapefsinfo(self, infoentry):
        if self.cmds["df"]:
            commandok, out = self.connector.ExecCmd(self.cmds["df"])
            fsinfo = out.split('\n')
            for i in fsinfo:
                i_splitted = i.split(' ')
                i_splitted_redu = list(filter(lambda x: len(x) > 0, i_splitted))
                try:
                    if len(i_splitted_redu) >= 6:
                        if (i_splitted_redu[5] == '/'):
                            kbytestotal = int(i_splitted_redu[1])
                            kbytesavailable = int(i_splitted_redu[3])
                            percentavailable = 100 - int(float(i_splitted_redu[4][:-1]))
                            partition = str(i_splitted_redu[0])
                            infoentry.SetFsInfo(partition, kbytestotal, kbytesavailable, percentavailable)
                except Exception as e:
                    self.logger.error(self.idstr("Error evaluating fsinfo: " + str(e)))

    def scrapememoryload(self, infoentry):
        if self.cmds["cat"]:
            commandok, out = self.connector.ExecCmd(self.cmds["cat"] + ' /proc/meminfo')
            meminfo = out.split('\n')
            memtotal = memfree = memavailable = swaptotal = swapfree = 0
            for i in meminfo:
                i_splitted = i.split(' ')
                i_splitted_redu = list(filter(lambda x: len(x) > 0, i_splitted))
                try:
                    if len(i_splitted_redu) > 1:
                        if i_splitted_redu[0] == "MemTotal:":     memtotal = int(i_splitted_redu[1])
                        if i_splitted_redu[0] == "MemFree:":      memfree = int(i_splitted_redu[1])
                        if i_splitted_redu[0] == "MemAvailable:": memavailable = int(i_splitted_redu[1])
                        if i_splitted_redu[0] == "SwapTotal:":    swaptotal = int(i_splitted_redu[1])
                        if i_splitted_redu[0] == "SwapFree:":     swapfree = int(i_splitted_redu[1])
                except Exception as e:
                    self.logger.error(self.idstr("Error evaluating meminfo: " + str(e)))
                infoentry.SetMem(memtotal, memfree, memavailable, swaptotal, swapfree)

    def scrapecustomcmd(self, infoentry):
        if self.tHostInfo["sCustomCmd"]:
            commandok, out = self.connector.ExecCmd(self.tHostInfo["sCustomCmd"])
            infoentry.SetCustom(out, self.tHostInfo["sCustomCmdLabel"])
        else:
            infoentry.SetCustom()

    def scrapeonetimeinfo(self, infoentry):
        if not self.onetimeinfoscraped:
            # os info
            if self.cmds["cat"]:
                commandok, out =self.connector.ExecCmd(self.cmds["cat"] + ' /proc/sys/kernel/ostype')
                self.ostype = out if commandok else ""
                commandok, out = self.connector.ExecCmd(self.cmds["cat"] + ' /proc/sys/kernel/osrelease')
                self.osversion = out if commandok else ""
                # may fail, not always present
                commandok, out = self.connector.ExecCmd(self.cmds["cat"] + ' /etc/os-release')
                osrelease = out.split('\n')
                for i in osrelease:
                    i_splitted = i.split('=')
                    if (len(i_splitted) > 1) and (i_splitted[0] == "PRETTY_NAME"): self.ostype += "(" + i_splitted[1] + ")"

            # cpu info
            if self.cmds["lscpu"]:
                commandok, out = self.connector.ExecCmd('LANG=en_US ' + self.cmds["lscpu"])
                cpuinfo = out.split('\n')
                try:
                    numcpuscraped = cpuvendorscraped = cpumodelscraped = False
                    for i in cpuinfo:
                        i_splitted = i.split(' ')
                        i_splitted_redu = list(filter(lambda x: len(x) > 0, i_splitted))
                        if len(i_splitted_redu) > 1:
                            if (i_splitted_redu[0] == "CPU(s):"):
                                self.numcpus = int(i_splitted_redu[1])
                                numcpuscraped = True
                            elif (i_splitted_redu[0] == "Vendor") and (i_splitted_redu[1] == "ID:"):
                                self.cpuvendor = " ".join(i_splitted_redu[2:]) # collect all list items, except the first two
                                cpuvendorscraped = True
                            elif (i_splitted_redu[0] == "Model") and (i_splitted_redu[1] == "name:"):
                                self.cpumodel = " ".join(i_splitted_redu[2:])
                                cpumodelscraped = True
                    if not (numcpuscraped and cpuvendorscraped and cpumodelscraped): raise ValueError("Could not parse cpuinfo")
                except ValueError as e:
                    self.logger.error(self.idstr(str(e)))
                except Exception as e:
                    self.logger.error(self.idstr("Error evaluating cpu info: " + str(e)))
                    self.logger.debug(self.idstr(cpuinfo))
                finally:
                    self.onetimeinfoscraped = True
        else:
            infoentry.SetCPU(self.cpuvendor, self.cpumodel, self.numcpus)
            infoentry.SetOS(self.ostype, self.osversion)

    def settimestamps(self, infoentry):
        # time of last contact - this is an instance variable (actually two variables - as human-readable string and as unix timestamp),
        # so the last value is preserved if communication fails (which means that the ssh commands fails, and triggers an exception so that these lines here are not executed)
        #tz = datetime.datetime.now().astimezone().tzinfo
        #now = datetime.datetime.now(tz)
        now = datetime.datetime.now(datetime.timezone.utc)
        self.lastcontact = now.strftime("%d.%m.%Y - %H:%M:%S %Z")
        infoentry.SetLastContact(self.lastcontact)
        self.timestamp = int(time.time())
        infoentry.SetTimestamp(self.timestamp)

    def scrapetarget(self):
        tUpdateEntry = systeminfoentry_cEntry()
        tUpdateEntry.SetHost(self.tHostInfo["sName"])
        tUpdateEntry.SetMemWarnPct(self.tHostInfo["fMemWarnPct"], self.tHostInfo["fSwapWarnPct"])
        tUpdateEntry.SetFsWarnPct(self.tHostInfo["fRootFsWarnPct"])

        # uptime
        self.scrapeuptime(tUpdateEntry)
        # load average
        self.scrapeloadavg(tUpdateEntry)
        # main memory load
        self.scrapememoryload(tUpdateEntry)
        #root filesystem info
        self.scrapefsinfo(tUpdateEntry)
        # custom cmd, if specified
        self.scrapecustomcmd(tUpdateEntry)
        # general "one-time-information"
        # (this info does not change during runtime, so we only need to scrape it once)
        self.scrapeonetimeinfo(tUpdateEntry)
        # time of last contact
        self.settimestamps(tUpdateEntry)

        tUpdateEntry.CheckLimits()
        self.NotifyObservers( (self.tHostInfo["sName"], tUpdateEntry.ToDict()) )

    def idstr(self, a_sMsg: str) -> str:
        return "[" + self.tHostInfo["sName"] + "] " + a_sMsg

    def run(self):
        if not isinstance(self.connector, iconnector):
            raise TypeError("Invalid connector")
        while not self.bExitThread.is_set():
            try:
                self.logger.debug (self.idstr("Trying to connect..."))
                self.connectotarget()
                self.logger.info (self.idstr("Connected"))

                self.onetimeinfoscraped = False
                while not self.bExitThread.is_set():
                    self.handlecyclicreconnect()
                    self.scrapetarget()
                    self.bExitThread.wait(float(self.tHostInfo["nScrapeSeconds"] if (self.tHostInfo["nScrapeSeconds"] >= 1) else 1))
            except Exception as e:
                self.logger.error (self.idstr("Exception: " + str(e)))
                time.sleep(1)
            finally:
                self.logger.info (self.idstr("Disconnected"))
                self.connector.Disconnect()
                if not self.bExitThread.is_set():
                    # since this is not a disconnect due to a regular ssh-dashboard shutdown: send "host down" update
                    self.NotifyObservers( (self.tHostInfo["sName"], systeminfoentry_cEntry(a_sHost = self.tHostInfo["sName"],
                                                                                           a_fUptime = 0.0,
                                                                                           a_sLastContact = self.lastcontact,
                                                                                           a_nTimestamp = self.timestamp).ToDict()) )
                    # delay for a short amount of time before attempting to reconnect
                    self.logger.info (self.idstr(f'Attempting re-connect in {self.nWaitAfterDisconnect} seconds'))
                    time.sleep(self.nWaitAfterDisconnect)
