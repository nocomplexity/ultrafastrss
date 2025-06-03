import pytest
import asyncio
from ultrafastrss.ultrafastrss import process_rssfeeds

import json


def test_integration(tmp_path):
    """Test0 - the async URL check with my RSS URLs
    tmp_path is a pytest fixture that provides a temporary directory unique to the test, managed by pytest.
    """
    urls = [
        'https://nocomplexity.com/rss',
        'https://www.eff.org/rss/updates.xml',
        'https://www.freebsd.org/news/rss.xml',
        'https://ubuntu.com/blog/feed',
        'https://nlnet.nl/feed.atom',
        'https://j3s.sh/feed.atom',
        'https://blog.research.google/atom.xml'
    ]
    
    # Run the async RSS feed processing
    results = asyncio.run(process_rssfeeds(urls))
    
    # Assert that results is a list
    assert isinstance(results, list), "Results should be a list"
    
    # Save results rss_results.json
    d = tmp_path / "testoutput"
    d.mkdir()
    output_path = d / "rss_results.json"
    try:
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to: file:/{output_path}")  # Print the message
    except IOError as e:
        pytest.fail(f"Failed to write results to {output_path}: {e}")
    
    # Optionally, verify the file was written
    assert output_path.exists(), f"JSON file was not created at: {output_path}"
