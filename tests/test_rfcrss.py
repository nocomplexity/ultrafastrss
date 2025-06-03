"""Sample to test that date is retrieved from <lastBuildDate> instead of None, when items have no date field"""

import pytest
from unittest.mock import patch

from ultrafastrss.ultrafastrss import rss_parser

from importlib.resources import files

expected_result = [{'title': 'RFC 9728: OAuth 2.0 Protected Resource Metadata',
  'link': 'https://www.rfc-editor.org/info/rfc9728',
  'date': '2025-04-23'},
 {'title': "RFC 9766: Extensions for Weak Cache Consistency in NFSv4.2's Flexible File Layout",
  'link': 'https://www.rfc-editor.org/info/rfc9766',
  'date': '2025-04-23'},
 {'title': 'RFC 9750: The Messaging Layer Security (MLS) Architecture',
  'link': 'https://www.rfc-editor.org/info/rfc9750',
  'date': '2025-04-23'},
 {'title': 'RFC 9765: RADIUS/1.1: Leveraging Application-Layer Protocol Negotiation (ALPN) to Remove MD5',
  'link': 'https://www.rfc-editor.org/info/rfc9765',
  'date': '2025-04-23'},
 {'title': 'RFC 9767: Grant Negotiation and Authorization Protocol Resource Server Connections',
  'link': 'https://www.rfc-editor.org/info/rfc9767',
  'date': '2025-04-23'},
 {'title': 'RFC 9753: Extension for Stateful PCE to Allow Optional Processing of Path Computation Element Communication Protocol (PCEP) Objects',
  'link': 'https://www.rfc-editor.org/info/rfc9753',
  'date': '2025-04-23'},
 {'title': 'RFC 9761: Manufacturer Usage Description (MUD) for TLS and DTLS Profiles for Internet of Things (IoT) Devices',
  'link': 'https://www.rfc-editor.org/info/rfc9761',
  'date': '2025-04-23'},
 {'title': 'RFC 9752: Conveying Vendor-Specific Information in the Path Computation Element Communication Protocol (PCEP) Extensions for Stateful PCE',
  'link': 'https://www.rfc-editor.org/info/rfc9752',
  'date': '2025-04-23'},
 {'title': 'RFC 9719: YANG Data Model for Routing in Fat Trees (RIFT)',
  'link': 'https://www.rfc-editor.org/info/rfc9719',
  'date': '2025-04-23'},
 {'title': 'RFC 9764: Bidirectional Forwarding Detection (BFD) Encapsulated in Large Packets',
  'link': 'https://www.rfc-editor.org/info/rfc9764',
  'date': '2025-04-23'},
 {'title': 'RFC 9692: RIFT: Routing in Fat Trees',
  'link': 'https://www.rfc-editor.org/info/rfc9692',
  'date': '2025-04-23'},
 {'title': 'RFC 9696: Routing in Fat Trees (RIFT) Applicability and Operational Considerations',
  'link': 'https://www.rfc-editor.org/info/rfc9696',
  'date': '2025-04-23'},
 {'title': 'RFC 9759: Unified Time Scaling for Temporal Coordination Frameworks',
  'link': 'https://www.rfc-editor.org/info/rfc9759',
  'date': '2025-04-23'},
 {'title': 'RFC 9726: Operational Considerations for Use of DNS in Internet of Things (IoT) Devices',
  'link': 'https://www.rfc-editor.org/info/rfc9726',
  'date': '2025-04-23'},
 {'title': 'RFC 9777: Multicast Listener Discovery Version 2 (MLDv2) for IPv6',
  'link': 'https://www.rfc-editor.org/info/rfc9777',
  'date': '2025-04-23'}]

def test_rss_parser():    
    xml_file_path = files("tests.resources") / "rfcrss.xml"
    with xml_file_path.open("r", encoding="utf-8") as f:
        xml_content = f.read()
        result = rss_parser(xml_content)
        assert result == expected_result