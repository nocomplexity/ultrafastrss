import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from dateutil.parser import parse

from ultrafastrss.ultrafastrss import rss_parser

from importlib.resources import files

expected_result = [
    {
        "title": "xkcd 1970: Name Dominoes",
        "link": "https://github.com/norvig/pytudes/blob/master/ipynb/xkcd-Name-Dominoes.ipynb",        
        "date": "2018-03-21"
    },
    {
        "title": "Functional Lifestyles Training",
        "link": "https://medium.com/@peternorvig/functional-lifestyles-training-47984a3cd2ba",       
        "date": "2018-04-01"
    },   
    {
        "title": "JScheme",
        "link": "http://norvig.com/jscheme.html",       
        "date": "2005-08-08"
    }
]


def test_rss_parser():    
    xml_file_path = files("tests.resources") / "norvig_rssfeed.xml"
    with xml_file_path.open("r", encoding="utf-8") as f:
        xml_content = f.read()
        result = rss_parser(xml_content)
        assert result == expected_result