import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from dateutil.parser import parse

from ultrafastrss.ultrafastrss import rss_parser

def test_rss_parser():
    # Mock is_valid_url and parser.parse
    with patch('ultrafastrss.ultrafastrss.is_valid_url') as mock_is_valid_url, \
         patch('ultrafastrss.ultrafastrss.parser.parse') as mock_parse:

        # Mock return values
        mock_is_valid_url.side_effect = lambda url: url == "http://example.com"  # Valid URL check
        mock_parse.return_value = parse("2023-10-01T12:00:00")  # Mock parsed date

        # Test case 1: Valid RSS feed with all elements
        valid_rss = '''
        <rss>
            <channel>
                <item>
                    <title>  Test Title\n  </title>
                    <link>http://example.com</link>
                    <pubDate>Mon, 01 Oct 2023 12:00:00 GMT</pubDate>
                    <category>Tech</category>
                    <category>News</category>
                </item>
            </channel>
        </rss>
        '''
        result = rss_parser(valid_rss)
        expected = [{
            'title': 'Test Title',
            'link': 'http://example.com',
            'date': '2023-10-01',
            'tags': ['Tech', 'News']
        }]
        assert result == expected
        mock_is_valid_url.assert_called_with('http://example.com')
        mock_parse.assert_called_once()

      
        no_valid_url_rss = '''
        <rss>
            <channel>
                <item>
                    <title>Test No URL</title>
                    <link>invalid_url</link>
                    <pubDate>Mon, 01 Oct 2023 12:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>
        '''
        result = rss_parser(no_valid_url_rss)
        assert result == []  # Item skipped due to invalid URL
        mock_is_valid_url.assert_called_with('invalid_url')

        # Test case 4: RSS feed with missing pubDate
        no_pubdate_rss = '''
        <rss>
            <channel>
                <item>
                    <title>Test No PubDate in item</title>
                    <link>http://example.com</link>
                </item>
            </channel>
        </rss>
        '''
        result = rss_parser(no_pubdate_rss)
        expected = [{
            'title': 'Test No PubDate in item',
            'link': 'http://example.com',
            'date': '2023-10-01'
        }]
        assert result == expected

        # Test case 5: RSS feed with no categories
        no_categories_rss = '''
        <rss>
            <channel>
                <item>
                    <title>Test No Categories</title>
                    <link>http://example.com</link>
                    <pubDate>Mon, 01 Oct 2023 12:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>
        '''
        result = rss_parser(no_categories_rss)
        expected = [{
            'title': 'Test No Categories',
            'link': 'http://example.com',
            'date': '2023-10-01'
        }]
        assert result == expected

        # Test case 6: Invalid XML
        with pytest.raises(ET.ParseError):
            rss_parser('invalid xml')
