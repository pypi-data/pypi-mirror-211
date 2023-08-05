#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import Dict, List
from abc import ABC, abstractmethod

class iEntry(ABC):
    @abstractmethod
    def ToDict(): pass
    @abstractmethod
    def __str__(): pass

class cEntry(iEntry):
    def __init__(self,
                 a_sHost: str = "",
                 a_fUptime: float = 0.0,
                 a_nTimestamp: int = 0,
                 a_sLastContact: str = "never",
                 a_fSysload_1min : float = 0.0,
                 a_fSysload_5min : float = 0.0,
                 a_fSysload_15min : float = 0.0,
                 a_nMemTotal: int = 0,
                 a_nMemFree: int = 0,
                 a_nMemAvailable: int = 0,
                 a_nSwapTotal: int = 0,
                 a_nSwapFree: int = 0,
                 a_nNumCpu: int = 0,
                 a_sCpuVendor: str = "",
                 a_sCpuModel: str = "",
                 a_fMemWarnPct: float = 0.0,
                 a_fSwapWarnPct: float = 0.0,
                 a_sOsType: str = "",
                 a_sOsVersion: str = "",
                 a_sFsPartition: str = "",
                 a_nFsTotal: int = 0,
                 a_nFsAvailable: int = 0,
                 a_nFsAvailablePct: int = 0,
                 a_fFsWarnPct: float = 0.0,
                 a_sCustomInfo: str = "",
                 a_sCustomLabel: str = ""):
        self.SetHost(a_sHost)
        self.SetUptime(a_fUptime)
        self.SetTimestamp(a_nTimestamp)
        self.SetLastContact(a_sLastContact)
        self.SetSysLoad(a_fSysload_1min, a_fSysload_5min, a_fSysload_15min)
        self.SetMem(a_nMemTotal, a_nMemFree, a_nMemAvailable, a_nSwapTotal, a_nSwapFree)
        self.SetMemWarnPct(a_fMemWarnPct, a_fSwapWarnPct)
        self.SetCPU(a_sCpuVendor, a_sCpuModel, a_nNumCpu)
        self.SetCustom(a_sCustomInfo, a_sCustomLabel)
        self.SetOS(a_sOsType, a_sOsVersion)
        self.SetFsInfo(a_sFsPartition, a_nFsTotal, a_nFsAvailable, a_nFsAvailablePct)
        self.SetFsWarnPct(a_fFsWarnPct)

        self._HostDown              = False
        self._MemLimitWarning       = False
        self._SwapLimitWarning      = False
        self._FsLimitWarning        = False
        self._SysLoadWarning        = False
        self._SysLoadWarning_1min   = False
        self._SysLoadWarning_5min   = False
        self._SysLoadWarning_15min  = False
        self.CheckLimits()

    def SetHost(self, a_sHost: str = ""):
        self._Name = a_sHost.strip('\n')

    def SetUptime(self, a_fUptime: float = 0):
        self._Uptime_s = a_fUptime

    def SetTimestamp(self, a_nTimestamp: int = 0):
        self._Timestamp = a_nTimestamp

    def SetLastContact(self, a_sLastContact: str = "never"):
        self._LastContact = a_sLastContact

    def SetSysLoad(self, a_f1Min: float = 0.0, a_f5Min: float = 0.0, a_f15Min: float = 0.0):
        self._SysLoad_1min  = a_f1Min
        self._SysLoad_5min  = a_f5Min
        self._SysLoad_15min = a_f15Min

    def SetMem(self, a_nMemTotal: int = 0, a_nMemFree: int = 0, a_nMemAvailable: int = 0, a_nSwapTotal: int = 0, a_nSwapFree: int = 0):
        self._MemTotal_kb = a_nMemTotal
        self._MemFree_kb = a_nMemFree
        self._MemAvailable_kb = a_nMemAvailable
        if self._MemTotal_kb == 0:
            self._MemAvailable_pct = 0
        else:
            self._MemAvailable_pct = int (a_nMemAvailable / a_nMemTotal * 100)
        self._SwapTotal_kb = a_nSwapTotal
        self._SwapFree_kb = a_nSwapFree
        if self._SwapTotal_kb == 0:
            self._SwapFree_pct = 0
        else:
            self._SwapFree_pct = int (a_nSwapFree / a_nSwapTotal * 100)

    def SetMemWarnPct(self, a_fMemWarnPct: float = 0.0, a_fSwapWarnPct: float = 0.0):
        self._MemWarnPct = a_fMemWarnPct
        self._SwapWarnPct = a_fSwapWarnPct

    def SetCPU(self, a_sCpuVendor: str = "", a_sCpuModel: str = "", a_nNumCpu: int = 0):
        self._CPUVendor = a_sCpuVendor.strip('\n')
        self._CPUModel = a_sCpuModel.strip('\n')
        self._NumCPU = a_nNumCpu

    def SetOS(self, a_sOsType: str = "", a_sOsVersion: str = ""):
        self._OSType = a_sOsType
        self._OSVersion = a_sOsVersion

    def SetFsInfo(self, a_sFsPartition: str = "", a_nFsTotal: int = 0, a_nFsAvailable: int = 0, a_nFsAvailablePct: int = 0):
        self._FsPartition = a_sFsPartition
        self._FsTotal = a_nFsTotal
        self._FsAvailable = a_nFsAvailable
        self._FsAvailablePct = a_nFsAvailablePct

    def SetFsWarnPct(self, a_fFsWarnPct: float = 0.0):
        self._FsWarnPct = a_fFsWarnPct

    def SetCustom(self, a_sCustomInfo: str = "", a_sCustomLabel: str = ""):
        self._CustomInfo = a_sCustomInfo
        self._CustomLabel = a_sCustomLabel

    def CheckLimits(self):
        if self._Uptime_s == 0: self._HostDown = True
        else:                   self._HostDown = False

        if (self._NumCPU > 0) and (self._SysLoad_1min > self._NumCPU):  self._SysLoadWarning_1min  = True
        else:                                                           self._SysLoadWarning_1min  = False
        if (self._NumCPU > 0) and (self._SysLoad_5min > self._NumCPU):  self._SysLoadWarning_5min  = True
        else:                                                           self._SysLoadWarning_5min  = False
        if (self._NumCPU > 0) and (self._SysLoad_15min > self._NumCPU): self._SysLoadWarning_15min = True
        else:                                                           self._SysLoadWarning_15min = False

        if self._MemAvailable_kb < (self._MemTotal_kb * self._MemWarnPct): self._MemLimitWarning = True
        else:                                                              self._MemLimitWarning = False

        if self._SwapFree_kb < (self._SwapTotal_kb * self._SwapWarnPct): self._SwapLimitWarning = True
        else:                                                            self._SwapLimitWarning = False

        if self._FsAvailable < (self._FsTotal * self._FsWarnPct): self._FsLimitWarning = True
        else:                                                     self._FsLimitWarning = False

    def ToDict(self, a_tSubset: List = None) -> Dict:
        if not a_tSubset:
            # return full dataset as dictionary
            return {
                "Name"                      : self._Name,
                "HostDown"                  : self._HostDown,
                "Uptime_s"                  : self._Uptime_s,
                "Timestamp"                 : self._Timestamp,
                "LastContact"               : self._LastContact,
                "SysLoad_1min"              : self._SysLoad_1min,
                "SysLoad_5min"              : self._SysLoad_5min,
                "SysLoad_15min"             : self._SysLoad_15min,
                "SysLoadWarning"            : self._SysLoadWarning_1min,  # deprecated, but kept for backwards compatibility
                "SysLoadWarning_1min"       : self._SysLoadWarning_1min,
                "SysLoadWarning_5min"       : self._SysLoadWarning_5min,
                "SysLoadWarning_15min"      : self._SysLoadWarning_15min,
                "MemTotal_kb"               : self._MemTotal_kb,
                "MemFree_kb"                : self._MemFree_kb,
                "MemAvailable_kb"           : self._MemAvailable_kb,
                "MemAvailable_percent"      : self._MemAvailable_pct,
                "MemLimitWarning"           : self._MemLimitWarning,
                "SwapTotal_kb"              : self._SwapTotal_kb,
                "SwapFree_kb"               : self._SwapFree_kb,
                "SwapFree_percent"          : self._SwapFree_pct,
                "SwapLimitWarning"          : self._SwapLimitWarning,
                "RootFSPartition"           : self._FsPartition,
                "RootFSTotal_kb"            : self._FsTotal,
                "RootFSAvailable_kb"        : self._FsAvailable,
                "RootFSAvailable_percent"   : self._FsAvailablePct,
                "RootFsLimitWarning"        : self._FsLimitWarning,
                "NumCPU"                    : self._NumCPU,
                "CPUVendor"                 : self._CPUVendor,
                "CPUModel"                  : self._CPUModel,
                "OSType"                    : self._OSType,
                "OSVersion"                 : self._OSVersion,
                "CustomInfo"                : self._CustomInfo,
                "CustomLabel"               : self._CustomLabel
            }
        else:
            # only return the requested subset
            fullmetrics = self.ToDict()
            return dict((k, fullmetrics[k]) for k in a_tSubset if k in fullmetrics)

    def __str__(self):
        return json.dumps(self.ToDict())
