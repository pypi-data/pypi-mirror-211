#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

# An observer adds itself (or gets added) to a subject. The subject notifies all of its observers when something happens (e.g. new data arrives).

class cObserverBase(ABC):
    @abstractmethod
    # overwrite this in derived classes to perform application-specific processing
    def Update(self, caller, data): # pass reference to caller object, and optionally application specific data
        pass

class cSubjectBase():
    def __init__(self):
        self._tObservers = []

    def AddObserver(self, tObs):
        if isinstance(tObs, cObserverBase):
            self._tObservers.append(tObs)
        else:
            raise ValueError("Observer needs to derive from observerbase.cObserverbase")

    def ClearObservers(self):
        self._tObservers.clear()

    def NotifyObservers(self, data):
        for i in self._tObservers:
            i.Update(self, data)
