#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import signal
import time
import tracemalloc
import os
import shutil
from .args import GetArgParser as args_GetArgParser
from .connector import ssh as connector_ssh
from .flaskthread import cFlaskThread as flaskthread_cFlaskthread
from .appconfig import cConfig as appconfig_cConfig
from .appversion import GetAppVersion as appversion_GetAppVersion
from .metrics import collectorthread as metrics_collectorthread
from .observer import cWebMetricsCache as observer_cWebMetricsCache
from .observer import cMqtt as observer_cMqtt
from .observer import cInfluxDb as observer_cInfluxDb

# main routine
def run_program():
    signal.signal(signal.SIGINT,  exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    # parse command line arguments
    parser = args_GetArgParser()
    targs = parser.parse_args()
    # prepare logging
    setup_logging(targs.verbose)
    #tracemalloc_start()
    # run main routine
    cfgfile = targs.config

    # If requested: deploy sample configuration file to the current working directory and exit
    if targs.get_default_config:
        config_src = os.path.dirname(os.path.realpath(__file__)) + "/config.json"
        try:
            shutil.copy(config_src, os.getcwd())
        except Exception as e:
            logging.error(f"Error deploying sample configuration: {str(e)}")
            return(1)
        logging.info(f"Deployed sample configuration file to {os.getcwd()}")
        return(0)

    logger = logging.getLogger("RUN")
    try:
        # Read in configuration
        tConfig = appconfig_cConfig()
        tConfig.ReadFromFile(cfgfile)
        logger.debug ("Using configuration:")
        logger.debug ("Local webserver address: "  + tConfig.tWebserver["sLocalAddress"])
        logger.debug ("Local webserver port: "     + str(tConfig.tWebserver["nLocalPort"]))
        logger.debug ("Websites active: "          + str(tConfig.tWebserver["bWebsiteActive"]))
        logger.debug ("REST API active: "          + str(tConfig.tWebserver["bRestAPIActive"]))
        logger.debug ("Mqtt client active: "       + str(tConfig.tMqtt["bActive"]))
        logger.debug ("InfluxDb client active: "   + str(tConfig.tInfluxDbClient["bActive"]))
        logger.debug ("Active hosts: ")
        for i in tConfig.tHostList:
            if i["bActive"]: logger.debug (i["sName"])
    except ValueError as e:
        logger.error (f"Configuration error in {cfgfile}: {str(e)}")
        exit(1)
    except KeyError as e:
        logger.error (f"Missing needed key in {cfgfile}: {str(e)}")
        exit(1)
    except Exception as e:
        logger.error (f"Error reading {cfgfile}: " + str(e))
        exit(1)

    # information flow is as follows:
    # +--------------------+                           +--------------------+                  +--------------------+
    # |  collectorthreads  | ------------------------> |   metrics cache    | <--------------- |  webserver thread  | ---> deliver website on request
    # +--------------------+     |      notify         +--------------------+  read on demand  +--------------------+
    #                            |
    #                            |                     +--------------------+
    #                             -------------------> |    mqtt client     | ---> push to broker
    #                                   notify         +--------------------+
    #                            |
    #                            |                     +--------------------+
    #                             -------------------> |   influxdb client  | ---> write to influxdb
    #                                   notify         +--------------------+
    observers = [] # collect observers as they are created

    # start flask thread if needed
    try:
        if tConfig.tWebserver["bWebsiteActive"] or tConfig.tWebserver["bRestAPIActive"]:
            if tConfig.tWebserver["bWebsiteActive"] and not tConfig.tWebserver["bRestAPIActive"]:
                tConfig.tWebserver["bRestAPIActive"] = True
                logger.warning("Activating REST API automatically for embedded websites")
            twebmetricscache = observer_cWebMetricsCache(a_nLogSize   = tConfig.tWebserver["nEventLogSize"],
                                                         a_tKeysToLog = tConfig.tWebserver["tEventLogKeys"])
            twebserver = flaskthread_cFlaskthread(metrics          = twebmetricscache,
                                                  detailstemplate  = tConfig.tWebserver["sDetailsTemplate"],
                                                  overviewtemplate = tConfig.tWebserver["sOverviewTemplate"],
                                                  host             = tConfig.tWebserver["sLocalAddress"],
                                                  port             = tConfig.tWebserver["nLocalPort"],
                                                  website_active   = tConfig.tWebserver["bWebsiteActive"],
                                                  restapi_active   = tConfig.tWebserver["bRestAPIActive"],
                                                  loghttprequests  = tConfig.tWebserver["bLogHttpRequests"])
            twebserver.daemon = True
            twebserver.start()
            observers.append(twebmetricscache)
        else:
            logger.warning("Neither websites or rest api is active, NOT starting webserver")
    except Exception as e:
        logger.error("Webserver thread start failed")
        print (e)
        exit(1)

    # start mqttclient if needed
    if tConfig.tMqtt["bActive"]:
        logger.info ("Starting Mqtt client")
        try:
            tmqttclient = observer_cMqtt(a_nQoS         = tConfig.tMqtt["nQoS"],
                                         a_sBroker      = tConfig.tMqtt["sBroker"],
                                         a_nPort        = tConfig.tMqtt["nPort"],
                                         a_sUser        = tConfig.tMqtt["sUser"],
                                         a_sPassword    = tConfig.tMqtt["sPassword"],
                                         a_sCa_certs    = tConfig.tMqtt["sCa_certs"],
                                         a_sCertfile    = tConfig.tMqtt["sCertfile"],
                                         a_sKeyfile     = tConfig.tMqtt["sKeyfile"],
                                         a_sTopicPrefix = tConfig.tMqtt["sTopicPrefix"])
            tmqttclient.start()
            observers.append(tmqttclient)
        except Exception as e:
            logger.error ("Mqtt client failed")
            print (e)
            tmqttclient.stop()
            exit(1)

    # prepare influxdbclient if needed
    if tConfig.tInfluxDbClient["bActive"]:
        logger.info ("Preparing InfluxDb client")
        try:
            tinfluxdbclient = observer_cInfluxDb(a_sMeasurement = tConfig.tInfluxDbClient["sMeasurement"],
                                                 a_sUrl         = tConfig.tInfluxDbClient["sUrl"],
                                                 a_sOrg         = tConfig.tInfluxDbClient["sOrganization"],
                                                 a_sToken       = tConfig.tInfluxDbClient["sToken"],
                                                 a_sBucket      = tConfig.tInfluxDbClient["sBucket"],
                                                 a_nTimeout     = tConfig.tInfluxDbClient["nTimeout_ms"])
            observers.append(tinfluxdbclient)
        except Exception as e:
            logger.error ("InfluxDb client failed")
            print (e)
            exit(1)

    # start ssh client threads
    threadlist = []
    for i in tConfig.tHostList:
        try:
            if i["bActive"]:
                # start thread, append to the list of threads and also add all active observers to be notified when new metrics are available
                logger.debug ("Starting thread for " + i["sName"])
                identity = tConfig.tIdentities[i["sIdentity"]]
                newthread = metrics_collectorthread(i, connector_ssh(sName      = i["sName"],
                                                                     sHostname  = i["sHost"],
                                                                     nPort      = i["nPort"],
                                                                     sUser      = identity["sUser"],
                                                                     sPassword  = identity["sPassword"],
                                                                     sKeyfile   = identity["sKeyFile"]))
                threadlist.append(newthread)
                for j in observers: newthread.AddObserver(j)
                newthread.start()
        except Exception as e:
            logger.error ("SSH thread start failed: " + str(e))
            exit(1)

    # main loop
    global bStopMainLoop
    bStopMainLoop = False
    while not bStopMainLoop:
        #tracemalloc_eval()
        time.sleep(1)

    logger.info ("Stopped main loop")

    # stop mqtt client if needed
    if tConfig.tMqtt["bActive"]:
        tmqttclient.stop()

    # wait for ssh threads to finish
    for i in threadlist:
        i.signal_exitthread()
        i.join()

    logger.info ("All SSH threads finished")

def exit_gracefully(signal, frame):
    print ("Caught SIGINT/SIGTERM, shutting down...")
    global bStopMainLoop
    bStopMainLoop = True

def setup_logging(verbose: bool):
    # Set application wide debug level and format
    logging.basicConfig(format='%(asctime)s [%(name)s - %(levelname)s]: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.DEBUG if verbose else logging.INFO)
    # Separatly set paramikos logging level as it can get really talky at info/debug
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    print ("---")
    logging.info(f"ssh-dashboard {appversion_GetAppVersion()}")
    #logging.getLogger('SSH').setLevel(logging.DEBUG)

def tracemalloc_start():
    tracemalloc.start()

def tracemalloc_eval():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('filename')
    print("=== memory consumption top 5 ===")
    for i in top_stats[:5]:
        print(i)
