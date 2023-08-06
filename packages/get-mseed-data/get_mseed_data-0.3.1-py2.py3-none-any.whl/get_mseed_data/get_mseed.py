

from pathlib import Path
"""Workaround due to arclink deprecation"""
try:
    from obspy.clients.arclink import Client as clientArclink
    arclink_client = True
except Exception as e:
    arclink_client = False
    print("WARNING. CLIENT ARCLINK NO AVAILABLE")

from obspy.clients.seedlink import Client as clientSeedlink
from obspy.clients.filesystem.sds import Client as clientArchive
from obspy.clients.fdsn import Client as clientFDSN 


import logging
logger=logging.getLogger('get_mseed')

SECONDS_IN_DAY = 86400

def choose_service(server_parameter_dict):
    '''
    Funtion that connects to a mseed data server (ARCLINK|SEEDLINK|ARCHIVE) and returns a client
    
    :type server_parameter_dict: dict
    :param server_parameter_dict: dictionary with the parameters of the MSEED server
    
    :return: obspy.client object    
    '''
    logger.info("start choose_service")
    if server_parameter_dict['name'] == 'ARCLINK':
        if arclink_client:
            try:
                logger.info("Trying  Arclink : %s %s %s" %(server_parameter_dict['user'],server_parameter_dict['server_ip'],server_parameter_dict['port']) )
                return clientArclink(server_parameter_dict['user'],server_parameter_dict['server_ip'],int(server_parameter_dict['port']), timeout=66 )
            except Exception as e:
                exception_message = "Error Arclink %s -- %s %s %s" %(str(e), server_parameter_dict['user'],server_parameter_dict['server_ip'],server_parameter_dict['port'])
                logger.fatal(exception_message)
                raise Exception(exception_message )
        else:
            logger.fatal("ARCLINK DEPRECATED IN LATEST OBSPY VERSION. !!USE FDSN OR ARCHIVE!!")
            raise Exception("ARCLINK DEPRECATED IN LATEST OBSPY VERSION. !!USE FDSN OR ARCHIVE!!")

    elif server_parameter_dict['name'] == 'SEEDLINK':
        try:
            logger.info("Trying  Seedlink : %s %s" %(server_parameter_dict['server_ip'],server_parameter_dict['port']) )
            return clientSeedlink(server_parameter_dict['server_ip'],int(server_parameter_dict['port']),timeout=5 )
        except Exception as e:
            exception_message = "Error Seedlink :%s -- %s %s" %(str(e),server_parameter_dict['server_ip'],server_parameter_dict['port'])
            logger.fatal( exception_message)
            raise Exception( exception_message)
            
    elif server_parameter_dict['name'] == 'ARCHIVE':
        
        try:
            archive_path = Path(server_parameter_dict['archive_path'])
            logger.info("Trying  Archive : %s " %(archive_path) )
            return clientArchive(archive_path)

        except Exception as e:
            exception_message = "Error Archive : %s -- %s" %(str(e),server_parameter_dict['archive_path'])
            logger.fatal(exception_message)
            raise Exception(exception_message)

    elif server_parameter_dict['name'] == 'FDSN':
        try:
            logger.info("Trying FDSN : %s %s" %(server_parameter_dict['server_ip'],server_parameter_dict['port']))
            return clientFDSN("http://%s:%s" %(server_parameter_dict['server_ip'],server_parameter_dict['port']))
        except Exception as e:  
            exception_message = "Error FDSN: %s -- %s" %(server_parameter_dict['server_ip'],server_parameter_dict['port'])
            logger.fatal(exception_message)
            raise Exception(exception_message)

def get_stream(service,chosen_client,network,station,location,channel,start_time,end_time=None,window_size=None):
    '''
    This function ask for data to a mseed data server and returns a mseed stream 
    The parameter of the stream are called explicitly to enhace the readability of the code. 
    
    :type service: string
    :parameter service: name of the service to use
    :type chosen_client: obspy.client
    :parameter chosen_client: Obspy client object to connect to a data server
    :type network: string
    :parameter network: Network of the data, e.g. EC, CO, GE
    :type station: string
    :parameter station: Name of the station, e.g. BMAS, ZUMB
    :type location: string
    :parameter location: Location of the station, usually this is an empty value '' or 00, 01, etc.
    :type channel: string
    :parameter channel: Channel of the station, e.g. BHZ, HHZ, BLZ
    :type start_time: obspy.UTCDateTime
    :parameter start_time: obspy datetime object. Indicates the start datetime of the requested data   
    :return: obspy stream object. 
    '''
    


    if end_time == None and window_size == None:
        end_time = start_time + SECONDS_IN_DAY
    elif window_size != None:
        end_time = start_time + window_size
        
    station_info =  "%s %s %s %s %s" %(network,station,location,channel,start_time)
    logger.info('Starting station: %s' %(station_info))
    if service=='ARCLINK':
        try:
            return chosen_client.get_waveforms(network,station,location,channel,start_time ,end_time,route=False,compressed=False)
        except Exception as e:
            logger.fatal("Error getting stream_station: %s : %s" %(str(e), station_info))
    else:
        try:
            return chosen_client.get_waveforms(network,station,location,channel,start_time ,end_time)
        except Exception as e:
            logger.fatal("Error getting stream_station: %s : %s" %(str(e), station_info))

