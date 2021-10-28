
# Author : @jimmg35

class UrlBundler():
    """
        Url library for the project.
    """
    base_url = r"https://iot.epa.gov.tw"
    getProjects: str = base_url + r"/iot/v1/project"
    getDevicesOfProj: str = base_url + r"/iot/v1/device"
    getSensorOfDev: str = base_url + r"/iot/v1/device/{}/sensor"
    
    getIntervalData: str = base_url + r"/iot/v1/device/{}/sensor/{}/rawdata/statistic?start={}&end={}&interval={}&raw=false&option=strict"

    getMinuteData: str = base_url + r"/iot/v1/device/{}/sensor/pm2_5,voc,temperature,humidity/rawdata?start={}&end={}"

    getRealTime: str = base_url + r"/iot/v1/sensor/{}/rawdata"

class Key():
    """
        key class for api authentication.
    """
    key: str = 'AK39R4UXH52FXA9CPA'