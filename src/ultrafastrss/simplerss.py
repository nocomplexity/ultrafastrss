"""
License GPL3

(C) 2024-2025 Created by Maikel Mardjan - https://nocomplexity.com/

Date created    : 11-12-2024
Last updated    : See git history

Simple FAST Async RSS parser
"""

import asyncio
import gzip
import zlib
import brotli

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# from datetime import datetime
from dateutil import parser
from dateutil.tz import tzoffset
import xml.etree.ElementTree as ET
import re

import datetime


nocxheaders = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0",
    "Accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8",
    "Accept-Encoding": "gzip, deflate,br",
}
nocxtimeout = 7

# Define known timezone mappings
tzinfos = {
    "GMT": tzoffset("UTC", 0),
    "UT": tzoffset("UTC", 0),
    "UTC": tzoffset("UTC", 0),
    "PST": tzoffset("PST", -8 * 3600),  # Pacific Standard Time: UTC-8
    "PDT": tzoffset("PDT", -7 * 3600),  # Pacific Daylight Time: UTC-7
    "EST": tzoffset("EST", -5 * 3600),  # Eastern Standard Time: UTC-5
    "EDT": tzoffset("EDT", -4 * 3600),  # Eastern Daylight Time: UTC-4
    "CST": tzoffset("CST", -6 * 3600),  # Central Standard Time: UTC-6
    "CDT": tzoffset("CDT", -5 * 3600),  # Central Daylight Time: UTC-5
    "MST": tzoffset("MST", -7 * 3600),  # Mountain Standard Time: UTC-7
    "MDT": tzoffset("MDT", -6 * 3600),  # Mountain Daylight Time: UTC-6
    "HST": tzoffset("HST", -10 * 3600),  # Hawaii Standard Time: UTC-10
}


async def async_feedparser(url):
    """
    async version to parse RSS feeds in a 2025 way.
    Checks the status of a given URL and reports HTTP status codes or DNS errors.

    Args:
        url (str): The URL to check.

    Returns:
        tuple: A tuple containing the URL and either the status code or an error message.
    """

    def feedparser():
        try:
            request = Request(url, headers=nocxheaders)
            with urlopen(request, timeout=nocxtimeout) as response:
                content: bytes = response.read()
                content_encoding = response.headers.get("Content-Encoding")
                # Decompress content based on encoding
                if content_encoding == "gzip":
                    content = gzip.decompress(content)
                elif content_encoding == "deflate":
                    content = zlib.decompress(content, -zlib.MAX_WBITS)
                elif content_encoding == "br":  # Handle Brotli encoding
                    content = brotli.decompress(content)
                elif content_encoding not in [None]:
                    raise ValueError(f"Unexpected content encoding: {content_encoding}")
                # Decode content based on charset
                content_type = response.headers.get("Content-Type", "")
                content_charset = response.headers.get_content_charset()
                # If no charset is provided, extract it from Content-Type header
                if not content_charset and "charset=" in content_type:
                    content_charset = content_type.split("charset=")[-1].split(";")[0]
                # Default to UTF-8 if no charset is found
                content_charset = content_charset or "utf-8"
                # Decode with fallback for invalid bytes
                xml_content = content.decode(content_charset, errors="replace")
                parse_result = parse_feed(xml_content)
            return parse_result
        except HTTPError as e:
            print(f"{url} : HTTP Error: {e.code} {e.reason}")
        except URLError as e:
            print(f"{url} : URL Error: {e.reason}")
        except Exception as e:
            print(f"{url} : Unexpected Error: {str(e)}")

    return await asyncio.to_thread(feedparser)


def parse_feed(xml_content):
    """Feed parser
    Parses RSS feeds (atom 2.0) and returns JSON

    Args:
        xml_content: xml of RSS

    Returns:
        json: rss content as json
    """
    root = ET.fromstring(xml_content)
    # Check for RSS 2.0
    if root.tag == "rss":
        # Use the RSS parser
        filedata = rss_parser(xml_content)
    elif root.tag == "{http://www.w3.org/2005/Atom}feed":
        filedata = atom_parser(xml_content)
    elif root.tag == "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF":
        filedata = rdf_parser(xml_content)
    else:
        # Unknown feed type - or I do not want this complexity
        filedata = "Unknown feed type"
    return filedata


def rss_parser(xml_data):
    """Parse the RSS XML"""
    ns = {"dc": "http://purl.org/dc/elements/1.1/"}  # namespace for dc:date
    root = ET.fromstring(xml_data)
    items = root.findall(".//item")
    filedata = []
    for entry in items:
        data = {}
        title_element = entry.find("title")
        if title_element is not None:
            title = title_element.text
            # Remove all newlines and leading/trailing spaces
            cleaned_title = str(title).replace("\n", "").strip()
            data["title"] = cleaned_title
        else:
            # malformed RSS! So no title but it is a item.
            data["title"] = "None"
        link_element = entry.find("link")
        if link_element is not None:
            link = link_element.text
            # Check if link is valid
            if is_valid_url(link):
                data["link"] = link
            else:
                data["link"] = "Invalid URL"
        else:
            link_element = entry.find("guid")
            link = link_element.text
            data["link"] = link
        pub_date_element = entry.find("pubDate")
        dc_date_element = entry.find("dc:date", ns)
        date_text = None
        # Check if the 'pubDate' element exists and has text
        if pub_date_element is not None and pub_date_element.text:
            date_text = pub_date_element.text.strip()
        elif dc_date_element is not None and dc_date_element.text:
            date_text = dc_date_element.text.strip()
        else:
            # Handle case when <pubDate> or <dc_date> is not found
            fallback_date = get_last_build_date(xml_data)
            if fallback_date:
                date_text = fallback_date.strip()

        if date_text:
            try:
                date_obj = parser.parse(date_text, tzinfos=tzinfos)
                formatted_date = date_obj.strftime("%Y-%m-%d")
                data["date"] = formatted_date
            except Exception:
                # set current date instead of Invalid [open issue]
                today_date = (datetime.datetime.now()).date()
                data["date"] = str(today_date)
                # data['date'] = 'Invalid date'
        else:
            data["date"] = "None"
        # Now check for categories in feed
        categories = entry.findall("category")
        if categories:
            tags = []
            for category in categories:
                tags.append(category.text)
                data["tags"] = tags
        # Only store items with a valid URL
        if is_valid_url(link):
            filedata.append(data)
    return filedata


def get_last_build_date(xml_content):
    """
    Retrieves the <lastBuildDate> from an RSS XML string.

    Args:
        xml_content (str): The RSS XML content as a string.

    Returns:
        str: The text of the <lastBuildDate> element, or 'None' if not found or if parsing fails.

    Raises:
        ET.ParseError: If the XML is malformed and cannot be parsed.
    """
    try:
        # Parse the XML content
        root = ET.fromstring(xml_content)

        # Find the <lastBuildDate> element in the <channel>
        last_build_date_element = root.find(".//channel/lastBuildDate")

        # Check if the element exists and has text
        if last_build_date_element is not None and last_build_date_element.text:
            return last_build_date_element.text.strip()
        else:
            return "None"

    except ET.ParseError:
        return "None"


def atom_parser(xml_data):
    """Parse the Atom XML"""
    root = ET.fromstring(xml_data)
    # Namespace handling
    namespace = {
        "atom": "http://www.w3.org/2005/Atom",
        "xhtml": "http://www.w3.org/1999/xhtml",
        "media": "http://search.yahoo.com/mrss/",
    }  # Added media namespace
    # Find all entries using namespace-aware XPath
    items = root.findall(".//atom:entry", namespaces=namespace)
    # Extract data
    parsed_entries = []
    for item in items:
        data = {}
        # Find the <title> element
        title_element = item.find("atom:title", namespaces=namespace)
        if title_element is not None:
            if title_element.get("type") == "xhtml":
                # Find the nested <div> element
                div_element = title_element.find("xhtml:div", namespaces=namespace)
                if div_element is not None:
                    title = div_element.text
                else:
                    title = None  # Handle case where div is missing
            else:
                title = title_element.text
            cleaned_title = str(title).replace("\n", "").strip()
            data["title"] = cleaned_title
        else:
            data["title"] = None  # Handle case where title is missing

        # Now link: Prioritize atom:link with rel="alternate"
        link_element = item.find("atom:link[@rel='alternate']", namespaces=namespace)
        if link_element is not None:
            link = link_element.get("href")
        elif item.find("atom:id", namespaces=namespace) is not None:
            # Fallback to atom:id if no alternate link is found (though less common for primary link)
            link = item.find("atom:id", namespaces=namespace).text
        else:
            link = None
        data["link"] = link

        # published element
        published = item.find("atom:published", namespaces=namespace)
        if published is not None:
            simplified_date = parse_date(published)
        else:
            published = item.find("atom:updated", namespaces=namespace)
            if published is not None:
                simplified_date = parse_date(published)
            else:
                simplified_date = "None"
        data["date"] = simplified_date

        categories = item.findall("atom:category", namespaces=namespace)
        if categories:
            tags = [
                category.get("term") for category in categories if category.get("term")
            ]
            data["tags"] = tags
        else:
            data["tags"] = []  # Set tags to empty list if no categories found

        # Only store items with a valid URL
        if link is not None and is_valid_url(
            link
        ):  # Ensure link is not None before checking validity
            parsed_entries.append(data)
        # Return parsed entries
    return parsed_entries


def rdf_parser(xml_data):
    """Parse RDF XML."""
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError:
        return []
    namespaces = {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "dc": "http://purl.org/dc/elements/1.1/",
        "": "http://purl.org/rss/1.0/",
    }
    filedata = []
    for item in root.findall(".//item", namespaces):
        data = {}
        title = item.find("title", namespaces)
        link = item.find("link", namespaces)
        date_field = item.find("dc:date", namespaces)
        data["title"] = (
            title.text.replace("\n", "").strip()
            if title is not None and title.text
            else "None"
        )
        data["link"] = (
            link.text if link is not None and is_valid_url(link.text) else "None"
        )
        data["date"] = (
            parse_date(date_field)
            if date_field is not None and date_field.text
            else "None"
        )
        data["tags"] = []  # Add for consistency
        if data["link"] != "None":
            filedata.append(data)
    return filedata


def parse_date(date_field):
    """Make date field simple - or do not use this if you want need exact timezones with time
    Input: XML date field

    Output: None or date in format string "Y-m-d"
    """
    # Check if the 'pubDate' element exists and has text
    if date_field is not None and date_field.text:
        published = date_field.text
        # Input: Format date string, can be different for RSS feeds and Remove 'GMT'
        standardized_published = published.strip()  # Ensure no leading/trailing spaces
        # Parse date with tzinfos for known timezones
        date_obj = parser.parse(standardized_published, tzinfos=tzinfos)
        formatted_date = date_obj.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD
        simplified_date = str(formatted_date)
        return simplified_date
    else:
        # Handle case when pubDate is not found
        return "None"


async def process_rssfeeds(urls):
    """Process multiple RSS Feeds URLs asynchronously."""
    tasks = [async_feedparser(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


def is_valid_url(url):
    """
    Check if a string is a valid URL starting with http:// or https://.

    Args:
        url (str): The string to check.

    Returns:
        bool: True if the string is a valid URL, False otherwise.
    """
    if not isinstance(url, str) or not url.strip():
        # Reject non-string inputs or empty/whitespace-only strings
        return False

    url_regex = re.compile(
        r"^(https?://)"  # Must start with http:// or https://
        r"(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})"  # Domain with valid TLD
        r"(:\d+)?"  # Optional port
        r"(/[a-zA-Z0-9\-._~:/?#[\]@!$&\'()*+,;=]*)?$"  # Optional path, query, and fragment
    )
    return bool(url_regex.match(url))
