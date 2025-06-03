import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from dateutil.parser import parse

from ultrafastrss.ultrafastrss import rss_parser

from importlib.resources import files

expected_result = [{'title': 'TCCing is Believing: Apple finally adds TCC events to Endpoint Security!', 
                    'date': '2025-03-27',
                    'link': 'https://objective-see.org/blog/blog_0x7F.html'},
                    {'title': 'Leaking Passwords (and more!) on macOS',
                     'date': '2025-03-20',
                     'link': 'https://objective-see.org/blog/blog_0x7E.html'}, 
                    {'title': 'The Mac Malware of 2024',
                     'date': '2025-01-01', 
                     'link': 'https://objective-see.org/blog/blog_0x7D.html'},
                    {'title': 'Restoring Reflective Code Loading on macOS', 
                     'date': '2024-12-16',
                      'link': 'https://objective-see.org/blog/blog_0x7C.html'}]


def test_rss_parser():    
    xml_file_path = files("tests.resources") / "objectivec.xml"
    with xml_file_path.open("r", encoding="utf-8") as f:
        xml_content = f.read()
        result = rss_parser(xml_content)
        assert result == expected_result