
import requests as _req
from _consts import *

def AM_SendDataSameDevice(id, data):
    id_url = k_AM_localNodeURL + str(id)    
    
    hConfigurations={
        'Content-Type': k_AM_contentType
    }

    response  = _req.request(k_AM_SEND, id_url, headers=hConfigurations, data = str(data))
    if(response.status_code == 200) :
        return K_AM_success
    else :
        return k_AM_failure


def AM_GetDataSameDevice(id):
    id_url = k_AM_localNodeURL + str(id)   

    hConfigurations={
        'Content-Type': k_AM_contentType
    }

    response  = _req.request(k_AM_GET, id_url, headers=hConfigurations)
    return response.text


def AM_SendData(id, node_red_url, data):
    id_url = ""
    
    if(str(node_red_url).endswith('/')):
        id_url = str(node_red_url) + str(id)
    else :
        id_url = str(node_red_url) + "/" + str(id)

    hConfigurations={
        'Content-Type': k_AM_contentType
    }

    response  = _req.request(k_AM_SEND, id_url, headers=hConfigurations, data = str(data))
    if(response.status_code == 200) :
        return K_AM_success
    else :
        return k_AM_failure


def AM_GetData(id, node_red_url):
    id_url = ""
    
    if(str(node_red_url).endswith('/')):
        id_url = str(node_red_url) + str(id)
    else :
        id_url = str(node_red_url) + "/" + str(id)

    hConfigurations={
        'Content-Type': k_AM_contentType
    }

    response  = _req.request(k_AM_GET, id_url, headers=hConfigurations)
    return response.text
