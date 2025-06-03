import pytest

from ultrafastrss.ultrafastrss import atom_parser
from importlib.resources import files

expected_result = [
    {
        "title": "Radical Open Innovation News week 47-2024",
        "date": "2024-11-22",
        "link": "https://www.bm-support.org/roi-news-week27-2024/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 1-2024",
        "date": "2024-01-05",
        "link": "https://www.bm-support.org/radical-open-innovation-news-week-1-2024/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 26-2023",
        "date": "2023-06-30",
        "link": "https://www.bm-support.org/roi-news-week26-2023/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 41-2022",
        "date": "2022-10-09",
        "link": "https://www.bm-support.org/roi-news-week41-2021/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 16-2021",
        "date": "2021-04-25",
        "link": "https://www.bm-support.org/roi-news-week16-2021/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 14-2021",
        "date": "2021-04-10",
        "link": "https://www.bm-support.org/roi-news-week14-2021/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 12-2021",
        "date": "2021-03-27",
        "link": "https://www.bm-support.org/roi-news-week12-2021/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 10-2021",
        "date": "2021-03-12",
        "link": "https://www.bm-support.org/roi-news-week10-2021/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 8-2021",
        "date": "2021-02-26",
        "link": "https://www.bm-support.org/roi-news-week8-2021/",
        "tags": ["Blogs", "Innovation News"]
    },
    {
        "title": "Radical Open Innovation News week 6-2021",
        "date": "2021-02-15",
        "link": "https://www.bm-support.org/roi-news-week6-2021/",
        "tags": ["Blogs", "Innovation News"]
    }
]


def test_rss_parser():    
    xml_file_path = files("tests.resources") / "roi.atom"
    with xml_file_path.open("r", encoding="utf-8") as f:
        xml_content = f.read()
        result = atom_parser(xml_content)
        assert result == expected_result