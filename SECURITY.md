# Security

* This code uses the default Python library for RSS XML parsing. XML parsing has many hard to solve [vulnerabilities](https://docs.python.org/3/library/xml.html#xml-vulnerabilities). So take appropriate measurements when running this code. Use e.g. a jail or environment that is from a security point of view separated. Beware that almost all Python RSS tools published on PYPI.org has this vulnerability.

