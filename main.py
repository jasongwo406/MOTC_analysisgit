# import essential modules
import os 
import sys
import json
import requests
import pandas as pd
from os import listdir, stat
from typing import List, Dict
from colorama import init, Fore, Back, Style
import datetime
import schedule
init(convert=True)

# 一分鐘

# import main functionality
from src.Parser import GeoJsonParser
from src.dbcontext import Dbcontext
from src.requester import Requester
from src.utils import UrlBundler, Key


if __name__ == "__main__":

    # initialize dbcontext
    myDBcontext = Dbcontext({"user": "postgres", 
                            "password": "r2tadmiadc", 
                            "host": "localhost", 
                            "port": "5432"}, "motcdev")

    data = myDBcontext.fetchMSOData("2021-08-10 00:00:00", "2021-08-10 23:59:59")
    
    
    
   

