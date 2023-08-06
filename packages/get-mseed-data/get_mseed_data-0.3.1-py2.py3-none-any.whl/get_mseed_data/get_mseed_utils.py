import json
import logging
import configparser


def read_config_file(json_file_path):
    """
    Reads a json_file and returns it as a python dict
    
    :param string json_file_path: path to a json file with configuration information
    :returns: dict
    """
    
    json_file=check_file(json_file_path)
    with open(json_file) as json_data:
        return json.load(json_data)
    

def read_parameters(file_path):
    """
    Read a configuration text file
    
    :param string file_path: path to configuration text file
    :returns: dict: dict of a parser object
    """
    parameter_file=check_file(file_path)
    parser=configparser.ConfigParser()
    parser.read(parameter_file)    
    return parser._sections


def check_file(file_path):
    '''
    Check if the file exists
    
    :param string file_path: path to file to check
    :return: file_path
    :raises Exception e: General exception if file doesn't exist. 
    '''
    try:
        
        with open(file_path):
            return file_path

    except Exception as e:
        logging.error("Error in check_file(%s). Error: %s " %(file_path,str(e)))
        raise Exception("Error in check_file(%s). Error: %s " %(file_path,str(e)))

