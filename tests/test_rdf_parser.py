import pytest
import xml.etree.ElementTree as ET
from ultrafastrss.ultrafastrss import rdf_parser, parse_date, is_valid_url


def test_rdf_parser():
    """
    Tests the rdf_parser function with various XML inputs.
    """

    # Test case 1: Valid XML with multiple items
    valid_xml_multiple_items = """
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns="http://purl.org/rss/1.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <channel rdf:about="http://example.com/channel">
        <items>
          <rdf:Seq>
            <rdf:li rdf:resource="http://example.com/item1"/>
            <rdf:li rdf:resource="http://example.com/item2"/>
          </rdf:Seq>
        </items>
      </channel>
      <item rdf:about="http://example.com/item1">
        <title>  First Item Title  </title>
        <link>http://example.com/first-item</link>
        <dc:date>2023-01-15T12:30:00Z</dc:date>
      </item>
      <item rdf:about="http://example.com/item2">
        <title>Second Item Title</title>
        <link>https://example.com/second-item</link>
        <dc:date>2023-02-20T09:00:00Z</dc:date>
      </item>
    </rdf:RDF>
    """
    expected_multiple_items = [
        {"title": "First Item Title", "link": "http://example.com/first-item", "date": "2023-01-15", "tags": []},
        {"title": "Second Item Title", "link": "https://example.com/second-item", "date": "2023-02-20", "tags": []},
    ]
    assert rdf_parser(valid_xml_multiple_items) == expected_multiple_items

    # Test case 2: Valid XML with no items
    valid_xml_no_items = """
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns="http://purl.org/rss/1.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <channel rdf:about="http://example.com/channel">
        <items>
          <rdf:Seq/>
        </items>
      </channel>
    </rdf:RDF>
    """
    assert rdf_parser(valid_xml_no_items) == []

    # Test case 3: Invalid XML data
    invalid_xml = "This is not XML data."
    assert rdf_parser(invalid_xml) == []

    

    # Test case 5: XML with invalid link
    xml_invalid_link = """
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns="http://purl.org/rss/1.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <item rdf:about="http://example.com/item6">
        <title>Item with Invalid Link</title>
        <link>invalid-url</link>
        <dc:date>2023-04-05T11:00:00Z</dc:date>
      </item>
      <item rdf:about="http://example.com/item7">
        <title>Item with Valid Link</title>
        <link>http://example.com/valid-link</link>
        <dc:date>2023-04-05T11:00:00Z</dc:date>
      </item>
    </rdf:RDF>
    """
    expected_invalid_link = [
        {"title": "Item with Valid Link", "link": "http://example.com/valid-link", "date": "2023-04-05", "tags": []},
    ]
    # The item with "invalid-url" should be filtered out because data["link"] becomes "None"
    assert rdf_parser(xml_invalid_link) == expected_invalid_link

    # Test case 6: XML with empty text for elements
    xml_empty_text = """
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns="http://purl.org/rss/1.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <item rdf:about="http://example.com/item8">
        <title></title>
        <link></link>
        <dc:date></dc:date>
      </item>
      <item rdf:about="http://example.com/item9">
        <title>Item 9 Title</title>
        <link>http://example.com/item9-link</link>
        <dc:date>2023-05-10T08:00:00Z</dc:date>
      </item>
    </rdf:RDF>
    """
    expected_empty_text = [
        {"title": "None", "link": "None", "date": "None", "tags": []}, # This item will be filtered out due to link being "None"
        {"title": "Item 9 Title", "link": "http://example.com/item9-link", "date": "2023-05-10", "tags": []},
    ]
    # The first item will be filtered out because its link becomes "None"
    assert rdf_parser(xml_empty_text) == [
        {"title": "Item 9 Title", "link": "http://example.com/item9-link", "date": "2023-05-10", "tags": []},
    ]

    # Test case 7: XML with only whitespace in title
    xml_whitespace_title = """
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns="http://purl.org/rss/1.0/"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <item rdf:about="http://example.com/item10">
        <title>   </title>
        <link>http://example.com/item10-link</link>
        <dc:date>2023-06-15T14:00:00Z</dc:date>
      </item>
    </rdf:RDF>
    """
    expected_whitespace_title = [
        {"title": "", "link": "http://example.com/item10-link", "date": "2023-06-15", "tags": []},
    ]
    assert rdf_parser(xml_whitespace_title) == expected_whitespace_title


