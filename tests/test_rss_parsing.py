import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from dateutil.parser import parse

from ultrafastrss.ultrafastrss import rss_parser

from importlib.resources import files

expected_result = [{'title': 'Shift left: \xa0from complex and reactive to simple and proactive', 'link': 'https://nocomplexity.com/shift-left/', 'date': '2025-04-18', 'tags': ['Security', 'architecture']}, {'title': 'Open ML/AI News week 13-2025', 'link': 'https://nocomplexity.com/open-ai-news-week-13-2025/', 'date': '2025-03-29', 'tags': ['Machine Learning News', 'machine learning']}, {'title': 'Open Security News week 12-2025', 'link': 'https://nocomplexity.com/security-news-week-12-2025/', 'date': '2025-03-23', 'tags': ['Security News', 'Security']}, {'title': 'Open Security News week 10-2025', 'link': 'https://nocomplexity.com/security-news-week-10-2025/', 'date': '2025-03-02', 'tags': ['Security', 'Security News']}, {'title': 'Open Security News week 8-2025', 'link': 'https://nocomplexity.com/security-news-week-8-2025/', 'date': '2025-02-18', 'tags': ['Security News', 'Security']}, {'title': 'Open ML/AI News week 7-2025', 'link': 'https://nocomplexity.com/open-ml-news-week-7-2025/', 'date': '2025-02-15', 'tags': ['Machine Learning News', 'machine learning']}, {'title': 'Simplify Python', 'link': 'https://nocomplexity.com/simplifypython/', 'date': '2025-01-21', 'tags': ['Information Technology', 'Python']}, {'title': 'Pushing complexity to users', 'link': 'https://nocomplexity.com/pushing-complexity-to-users/', 'date': '2025-01-17', 'tags': ['Business', 'Information Technology', 'architecture', 'Complexity', 'Simple']}, {'title': 'Simplify IT', 'link': 'https://nocomplexity.com/simplifyit/', 'date': '2025-01-17', 'tags': ['Business', 'Information Technology', 'architecture', 'Simple', 'Software']}, {'title': 'Finding duplicates in a collection: A solved problem!', 'link': 'https://nocomplexity.com/finding-duplicates/', 'date': '2025-01-10', 'tags': ['Information Technology', 'architecture', 'Simple']}]


def test_rss_parser():    
    xml_file_path = files("tests.resources") / "nocxrss.xml"
    with xml_file_path.open("r", encoding="utf-8") as f:
        xml_content = f.read()
        result = rss_parser(xml_content)
        assert result == expected_result