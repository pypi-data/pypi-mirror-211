#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class cInfluxDbClient:

    def __init__(self,
                 a_sUrl: str = "",
                 a_sOrg: str = "",
                 a_sToken: str = "",
                 a_sBucket: str = "",
                 a_nTimeout: int = 10000,
                 a_tLogger = logging.getLogger('InfluxDb')):

        self.sUrl     = a_sUrl
        self.sOrg     = a_sOrg
        self.sToken   = a_sToken
        self.sBucket  = a_sBucket
        self.nTimeout = a_nTimeout

        self.logger = a_tLogger

        self.client = None
        self.write_api = None
        self.client = InfluxDBClient(url=self.sUrl, token=self.sToken, org=self.sOrg)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)

    def idstr(self, a_sMsg: str) -> str:
        return "[" + self.sUrl + "] " + a_sMsg

    def writedb(self, a_tFields: dict, a_tTags: dict, a_sMeasurement: str) -> bool:
        if not (self.client and self.write_api):
            self.logger.warning (self.idstr("Could not write to db: client or write_api not available"))
            return False
        try:
            entry = {"measurement": a_sMeasurement,
                     "tags": a_tTags,
                     "fields": a_tFields}
            self.write_api.write(bucket=self.sBucket, org=self.sOrg, record=entry)
        except Exception as e:
            self.logger.error (self.idstr("Could not write to db: " + str(e)))
            return False
        self.logger.debug(self.idstr("Wrote new entry with tags: " + str(a_tTags) + " to " + a_sMeasurement))
