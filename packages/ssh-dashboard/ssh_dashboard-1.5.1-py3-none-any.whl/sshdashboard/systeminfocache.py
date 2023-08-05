#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading
import time
from typing import List, Dict
from .flaskthread import iMetricsCache as flaskthread_iMetricsCache

class cCircularBuffer:
    def __init__(self, a_nMaxSize: int, a_tData = []):
        self._nIndex = 0
        self._nMaxSize = a_nMaxSize
        self._tData = list(a_tData)[-a_nMaxSize:]
        self._tLock = threading.Lock()
    def AddValue(self, a_tValue):
        with self._tLock:
            if len(self._tData) == self._nMaxSize: self._tData[self._nIndex] = a_tValue
            else:                                  self._tData.append(a_tValue)
            self._nIndex += 1
            self._nIndex %= self._nMaxSize
    # not threadsafe, should not be called directly
    def __GetValue(self, a_nIndex: int):
        if len(self._tData) == self._nMaxSize:
            return self._tData[(self._nIndex + a_nIndex) % self._nMaxSize]
        else:
            return self._tData[a_nIndex]
    def __getitem__(self, a_nIndex: int):
        with self._tLock: return self.__GetValue(a_nIndex)
    # Get sorted list:
    # index 0:      the youngest item (which was added last)
    # index size-1: the oldest item
    # Sorting gets reversed (oldest item first) if a_bReversed is set True
    def GetSortedList(self, a_bReversed = False):
        with self._tLock:
            tList = []
            indexrange = range(len(self._tData))
            if a_bReversed: indexrange = reversed(indexrange)

            for i in indexrange: tList.append(self.__GetValue(i))
            return tList

class cMetricsCache(flaskthread_iMetricsCache):
    def __init__(self, a_nLogSize = 50, a_tKeysToLog = []):
        super(cMetricsCache, self).__init__()
        self.tReducedMetricKeys = ["Name", "HostDown", "Uptime_s", "Timestamp", "SysLoad_1min", "SysLoad_5min", "SysLoad_15min", "SysLoadWarning_1min", "MemAvailable_percent", "MemLimitWarning" ]

        self.tHostMetrics = {}
        self.tHostEventLogs = {}
        self.nHostEventLogSize = a_nLogSize
        self.KeysToLog = a_tKeysToLog
    def GetFullMetrics(self, a_sHost: str) -> Dict:
        return self.tHostMetrics[a_sHost]
    def GetReducedMetrics(self, a_sHost: str) -> Dict:
        tFullMetrics = self.GetFullMetrics(a_sHost)
        return dict((k, tFullMetrics[k]) for k in self.tReducedMetricKeys if k in tFullMetrics)
    def SetMetrics(self, a_sHost, a_tData):
        if not isinstance(a_tData, dict):
            raise TypeError("Invalid metrics type")
        self.LogChanges(a_sHost, a_tData)
        self.tHostMetrics[a_sHost] = a_tData
    def LogChanges(self, a_sHost, a_tData):
        newdata = a_tData
        try:
            if not a_sHost in self.Hosts():
                # very first call for this host: do not check for any changes, but do check for active warnings. Also include host state unconditionally.
                self.LogEvent(a_sHost, "HostDown", newdata["HostDown"])
                if not newdata["HostDown"]:
                    for key in self.KeysToLog: self.LogEvent(a_sHost, key, newdata[key])
            else:
                # compare old and new data, check for changes and generate log events as necessary
                olddata = self.GetFullMetrics(a_sHost)
                if (newdata["HostDown"] != olddata["HostDown"]): self.LogEvent(a_sHost, "HostDown", newdata["HostDown"])
                if not newdata["HostDown"]: # only check other metrics if host is up - there are no meaningful metrics to interpret if host is down
                    for key in self.KeysToLog:
                        if (newdata[key] != olddata[key]): self.LogEvent(a_sHost, key,  newdata[key])
        except KeyError:
            pass    # Ignoring exceptions IS bad, but ignore a missing key at this point since this is "only" eventlogging
    def LogEvent(self, a_sHost, a_sKey, a_tNewValue):
        # Add Log entry to circular buffer. Each host has its own buffer.
        if not a_sHost in self.tHostEventLogs: self.tHostEventLogs[a_sHost] = cCircularBuffer(self.nHostEventLogSize)
        self.tHostEventLogs[a_sHost].AddValue( { "Name": a_sHost, "Key": a_sKey, "Value": a_tNewValue, "Timestamp": int(time.time()) } )
    def Hosts(self) -> List:
        return self.tHostMetrics.keys()
    def GetEventLog(self, a_sHost) -> List:
        # return list of dicts, each dict representing one event
        try:
            return self.tHostEventLogs[a_sHost].GetSortedList(a_bReversed = True)
        except KeyError:
            return None
