"""
Function to test only parse_feed

Generated test - so beware!

Explanation:

    Mocking: The rss_parser, atom_parser, and rdf_parser functions are mocked to avoid testing their implementation. They return predefined values to test the logic of parse_feed.
    Test Cases:
        RSS 2.0: Tests if the function correctly identifies an RSS feed and calls rss_parser.
        Atom: Tests if the function identifies an Atom feed and calls atom_parser.
        RDF: Tests if the function identifies an RDF feed and calls rdf_parser.
        Unknown Feed: Tests if the function returns 'Unknown feed type' for an unrecognized root tag.
        Invalid XML: Tests if the function raises an ET.ParseError for malformed XML.
    Assertions: Verifies that the correct parser is called and the expected output is returned.
    Module Reference: Replace 'your_module' with the actual module name where parse_feed and the parser functions are defined.

This test ensures the parse_feed function correctly handles different feed types and errors. Save it in a file like test_parse_feed.py and run with pytest.
"""


import pytest
import xml.etree.ElementTree as ET
from unittest.mock import patch
from ultrafastrss.ultrafastrss import parse_feed

def test_parse_feed():
    # Mock the parser functions
    with patch('ultrafastrss.ultrafastrss.rss_parser') as mock_rss, \
         patch('ultrafastrss.ultrafastrss.atom_parser') as mock_atom, \
         patch('ultrafastrss.ultrafastrss.rdf_parser') as mock_rdf:

        # Mock return values
        mock_rss.return_value = [{"title": "RSS feed"}]
        mock_atom.return_value = [{"title": "Atom feed"}]
        mock_rdf.return_value = [{"title": "RDF feed"}]

        # Test case 1: RSS 2.0 feed
        rss_xml = '<rss><channel><item><title>RSS feed</title></item></channel></rss>'
        result = parse_feed(rss_xml)
        mock_rss.assert_called_once_with(rss_xml)
        assert result == [{"title": "RSS feed"}]

        # Test case 2: Atom feed
        atom_xml = '<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Atom feed</title></entry></feed>'
        result = parse_feed(atom_xml)
        mock_atom.assert_called_once_with(atom_xml)
        assert result == [{"title": "Atom feed"}]

        # Test case 3: RDF feed
        rdf_xml = '<RDF xmlns="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><item><title>RDF feed</title></item></RDF>'
        result = parse_feed(rdf_xml)
        mock_rdf.assert_called_once_with(rdf_xml)
        assert result == [{"title": "RDF feed"}]

        # Test case 4: Unknown feed type
        unknown_xml = '<invalid>Invalid feed</invalid>'
        result = parse_feed(unknown_xml)
        assert result == 'Unknown feed type'

        # Test case 5: Invalid XML
        with pytest.raises(ET.ParseError):
            parse_feed('invalid xml')

