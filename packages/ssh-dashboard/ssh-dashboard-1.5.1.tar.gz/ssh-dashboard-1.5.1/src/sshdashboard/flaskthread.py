#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from xmlrpc.client import Boolean
from flask import Flask, render_template, request, make_response, send_from_directory
from flask import abort
from gevent.pywsgi import WSGIServer
import threading
import html
import json
from typing import List, Dict
from abc import ABC, abstractmethod
from .appversion import GetAppVersion

class iMetricsCache(ABC):
    @abstractmethod
    def GetFullMetrics(self, a_sHost: str) -> Dict: pass
    @abstractmethod
    def GetReducedMetrics(self, a_sHost: str) -> Dict: pass
    @abstractmethod
    def Hosts(self) -> List: pass
    @abstractmethod
    def GetEventLog(self, a_sHost) -> List: pass

class cFlaskThread(threading.Thread):
    htmlheader = ""
    htmlfooter = ""
    tSystemInfo = None
    def __init__(self,
                 metrics: iMetricsCache,
                 detailstemplate: str,
                 overviewtemplate: str,
                 host: str = '0.0.0.0',
                 port: int = 80,
                 website_active: bool = False,
                 restapi_active: bool = False,
                 tLogger = logging.getLogger('Webserver'),
                 loghttprequests: bool = True):
       super().__init__()
       cFlaskThread.detailstemplate = detailstemplate
       cFlaskThread.overviewtemplate = overviewtemplate
       self.app = Flask(__name__)
       self.host = host
       self.port = port
       self.website_active = website_active
       self.restapi_active = restapi_active
       self.metrics = metrics

       self.logger = tLogger
       self.loghttprequests = loghttprequests

    def addroutes(self):
        # --- Websites ---
        if (self.website_active):
            @self.app.route("/")
            def mainpage():
                try:
                    overviewdict = { "appversion": html.escape(GetAppVersion()) }
                except Exception as e:
                    self.logger.error(e)
                    abort(500)
                return render_template(cFlaskThread.overviewtemplate, **overviewdict)

            # TODO!
            @self.app.route("/hosts/<id>")
            def hostdetails(id):
                key = self.decodekey(id)
                if not key in self.metrics.Hosts():
                    abort(404)
                try:
                    detailsdict = { "name"      : key,
                                    "id"        : id,
                                    "appversion": html.escape(GetAppVersion()) }
                except Exception as e:
                    self.logger.error(e)
                    abort(500)
                return render_template(cFlaskThread.detailstemplate, **detailsdict)

            # serve static files: stylesheet and javascript functions used by both html templates
            @self.app.route('/css/<path:path>')
            def send_css(path):
                return send_from_directory('css', path)

            @self.app.route('/js/<path:path>')
            def send_js(path):
                return send_from_directory('js', path)

            self.logger.debug ("Added Flask website routes")

        # --- REST API ---
        if (self.restapi_active):
            def cors_preflight():
                tResponse = make_response()
                tResponse.headers.add("Access-Control-Allow-Origin", "*")
                tResponse.headers.add('Access-Control-Allow-Headers', "*")
                tResponse.headers.add('Access-Control-Allow-Methods', "*")
                return tResponse

            @self.app.route("/api/summary")
            def allhosts_json():
                if request.method == "OPTIONS":
                    return cors_preflight()
                combineddict = {}
                hostmetricsdict = {}
                hostids = {}
                try:
                    # Collect shortened metrics summary for all hosts, and hostid table: name -> id
                    for i in self.metrics.Hosts():
                        hostmetricsdict[i] = self.metrics.GetReducedMetrics(i)
                        hostids[i] = self.encodekey(i)
                    # Combine into one dictionary
                    combineddict["hosts"] = hostmetricsdict
                    combineddict["hostids"] = hostids
                except Exception as e:
                    self.logger.error(e)
                    abort(500)
                return json.dumps(combineddict),200,{'content-type':'application/json', 'Access-Control-Allow-Origin' : '*'}

            @self.app.route("/api/hostids")
            def hostlist_json():
                if request.method == "OPTIONS":
                    return cors_preflight()
                else:
                    hostids = {}
                    for i in self.metrics.Hosts(): hostids[i] = self.encodekey(i)
                    return json.dumps(hostids),200,{'content-type':'application/json', 'Access-Control-Allow-Origin' : '*'}

            @self.app.route("/api/hosts/<id>")
            def hostdetails_json(id):
                if request.method == "OPTIONS":
                    return cors_preflight()
                key = self.decodekey(id)
                if not key in self.metrics.Hosts():
                    abort(404)
                try:
                    tInfoDict = self.metrics.GetFullMetrics(key)
                except Exception as e:
                    self.logger.error(e)
                    abort(500)
                return json.dumps(tInfoDict),200,{'content-type':'application/json', 'Access-Control-Allow-Origin' : '*'}

            @self.app.route("/api/hosts/<id>/<metric>")
            def hostdetails_json_singlekey(id, metric):
                if request.method == "OPTIONS":
                    return cors_preflight()
                key = self.decodekey(id)
                if not key in self.metrics.Hosts():
                    abort(404)
                try:
                    tInfoDict = self.metrics.GetFullMetrics(key)
                except Exception as e:
                    self.logger.error(e)
                    abort(500)
                if not metric in tInfoDict.keys():
                    abort(404)
                return json.dumps( {metric : tInfoDict[metric]} ),200,{'content-type':'application/json', 'Access-Control-Allow-Origin' : '*'}

            @self.app.route("/api/logs/hosts/<id>")
            def hosteventlog_json(id):
                if request.method == "OPTIONS":
                    return cors_preflight()
                key = self.decodekey(id)
                try:
                    tLogs = self.metrics.GetEventLog(key)
                except Exception as e:
                    self.logger.error(e)
                    abort(500)
                if not tLogs:
                    abort(404)
                return json.dumps(tLogs),200,{'content-type':'application/json', 'Access-Control-Allow-Origin' : '*'}

            self.logger.debug ("Added Flask rest api routes")

    @staticmethod
    def encodekey(a_sKey: str) -> str:
        return (a_sKey.encode().hex())

    def decodekey(self, a_sKey: str) -> str:
        try:
            return (bytearray.fromhex(a_sKey).decode())
        except ValueError as e:
            self.logger.debug("Invalid key: " + str(e))
            return ""   # silently return empty string, should lead to a http 404 which is the intended behaviour.

    def run(self):
       if not isinstance(self.metrics, iMetricsCache):
            raise TypeError("Invalid metrics provider")
       self.addroutes()
       self.logger.info (f"Starting webserver ({self.host}:{self.port})")
       if not self.loghttprequests: self.logger.info("HTTP request logging off")
       http_server = WSGIServer(listener = (self.host, self.port),
                                application = self.app,
                                log = self.logger if self.loghttprequests else None,
                                error_log = self.logger)
       http_server.serve_forever()
       #self.app.run(host=self.host, port=self.port, debug=False)
