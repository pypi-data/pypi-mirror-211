#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import List, Dict
from .systeminfocache import cMetricsCache as systeminfocache_cMetricsCache
from .influxdbclient import cInfluxDbClient as influxdbclient_cInfluxDbClient
from .mqttclient import cMqttClient as mqttclient_cMqttClient
from .observerbase import cObserverBase as observerbase_cObserverBase

class cMqtt(mqttclient_cMqttClient, observerbase_cObserverBase):
    def __init__(self, a_nQoS, **kw):
        super(cMqtt, self).__init__(**kw)
        self.nQoS = a_nQoS

    def Update(self, caller, data):
        try:
            (key, entry) = data
        except Exception as e:
            self.logger.error (self.idstr("Could not fetch new data: " + str(e)))
            return
        self.publish(key,
                     json.dumps(entry),
                     self.nQoS)

class cInfluxDb(influxdbclient_cInfluxDbClient, observerbase_cObserverBase):
    def __init__(self, a_sMeasurement, **kw):
        super(cInfluxDb, self).__init__(**kw)
        self.sMeasurement = a_sMeasurement

    def Update(self, caller, data):
        try:
            (key, entry) = data
        except Exception as e:
            self.logger.error(self.idstr("Could not fetch new data: " + str(e)))
            return
        self.writedb(entry,
                    {"Location": key},
                    self.sMeasurement)

class cWebMetricsCache(systeminfocache_cMetricsCache, observerbase_cObserverBase):
    def __init__(self, **kw):
        super(cWebMetricsCache, self).__init__(**kw)

    def Update(self, caller, data):
        try:
            (key, entry) = data
            self.SetMetrics(key, entry)
        except Exception as e:
            self.logger.error("Could not fetch new data: " + str(e))
            return
