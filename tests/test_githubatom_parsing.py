import pytest

from ultrafastrss.ultrafastrss import atom_parser
from importlib.resources import files

expected_result = [
    {
        "date": "2025-05-06",
        "link": "https://github.com/Velocidex/velociraptor/commit/99dba703bfeecce3ad1b265d175ab11e5f1eb656",
        "title": "Bugfixes: Fix build and VQL Memory limit bug (#4223)",
        "tags": []
    },
    {
        "date": "2025-05-05",
        "link": "https://github.com/Velocidex/velociraptor/commit/fe670b27ed46735d164e32a34c0220e5607e99db",
        "title": "Update Memory Acquisition artifact to store driver in user directory …",
        "tags": []
    },
    {
        "date": "2025-05-02",
        "link": "https://github.com/Velocidex/velociraptor/commit/f1c0bc6a4066ba3709ae3769f0e26e3ea8d040e8",
        "title": "Update security.md (#4219)",
        "tags": []
    },
    {
        "date": "2025-04-29",
        "link": "https://github.com/Velocidex/velociraptor/commit/5ab2cf238ce4c75c7af69e645e317270106960fb",
        "title": "Added VQL functions to manipulate secrets. (#4215)",
        "tags": []
    },
    {
        "date": "2025-04-28",
        "link": "https://github.com/Velocidex/velociraptor/commit/fe4a5e0a579d78d003eb77161ab716fd6e87cc7a",
        "title": "Giving default folder Read & Traverse permissions in Darwin installer…",
        "tags": []
    },
    {
        "date": "2025-04-28",
        "link": "https://github.com/Velocidex/velociraptor/commit/1543bef34a4e526b182f5602ea99ad00ca0639af",
        "title": "Bugfix: Allows azure authenticator to use the proxy setting. (#4214)",
        "tags": []
    },
    {
        "date": "2025-04-27",
        "title": "Delay flow error until the flow is completed. (#4210)",
        "link": "https://github.com/Velocidex/velociraptor/commit/cda0eb7672b566f04a4bb70a2c8cd0f8cedff3a1",
        "tags": []
    },
    {
        "date": "2025-04-22",
        "title": "Keep record of finished flows in client's flow manager. (#4202)",
        "link": "https://github.com/Velocidex/velociraptor/commit/a5abaee504234366a0ebe2eb114d0e02019f38d5",
        "tags": []
    },
    {
        "date": "2025-04-22",
        "title": "Avoid I/O after deleting client flows (#4179)",
        "link": "https://github.com/Velocidex/velociraptor/commit/6c27e7e2ea509c76201b64431ba71b0c3b7a2758",
        "tags": []
    },
    {
        "date": "2025-04-22",
        "title": "Fixed tests",
        "link": "https://github.com/Velocidex/velociraptor/commit/22f8245dfe0b93d818acdbbb2e66791ffc2c06e5",
        "tags": []
    },
    {
        "date": "2025-04-22",
        "title": "Bugfix: Allow API client to push events without high permissions.",
        "link": "https://github.com/Velocidex/velociraptor/commit/3f050cdae7d0e61ccf7e631daa2cb001a2db9c2d",
        "tags": []
    },
    {
        "date": "2025-04-19",
        "title": "Bugfix: Move atomic fields to the start of the struct (#4197)",
        "link": "https://github.com/Velocidex/velociraptor/commit/bd0017a76271a8ede39f2661af26de9efb9d3c58",
        "tags": []
    },
    {
        "date": "2025-04-19",
        "title": "Bugfix: Implement better elastic index sanitization (#4196)",
        "link": "https://github.com/Velocidex/velociraptor/commit/a53a69328d2f8ca83eabac38009d8507c50be3bf",
        "tags": []
    },
    {
        "date": "2025-04-18",
        "title": "Bugfix: Do not complete collection on error.  (#4194)",
        "link": "https://github.com/Velocidex/velociraptor/commit/3de202739fa04af1e519298a08fa464b3a733e74",
        "tags": []
    },
    {
        "date": "2025-04-18",
        "title": "Bump http-proxy-middleware from 2.0.7 to 2.0.9 in /gui/velociraptor (…",
        "link": "https://github.com/Velocidex/velociraptor/commit/f082efe463a052b5bb663c9c8f13f106511ad316",
        "tags": []
    },
    {
        "date": "2025-04-18",
        "title": "Bugfix: Close tempfile before removing (#4191)",
        "link": "https://github.com/Velocidex/velociraptor/commit/1dbc9e0de8e7c9d546933d1e89a2faf752af8aef",
        "tags": []
    },
    {
        "date": "2025-04-17",
        "title": "Bugfix: Fixed bug in Server.Orgs.NewOrg",
        "link": "https://github.com/Velocidex/velociraptor/commit/62bb7709c55d7dd316231643ed56ed480cf1b87e",
        "tags": []
    },
    {
        "date": "2025-04-17",
        "title": "fix syntax error in pattern of TempFile",
        "link": "https://github.com/Velocidex/velociraptor/commit/9097291080c9777c2748c86a6b9e1a733c7b74fc",
        "tags": []
    },
    {
        "date": "2025-04-16",
        "title": "Set the user avatar in the datastore (#4180)",
        "link": "https://github.com/Velocidex/velociraptor/commit/f9bf853b591e8de845836ffbddca6c4e70a55628",
        "tags": []
    },
    {
        "date": "2025-04-15",
        "title": "Bump github.com/gorilla/csrf from 1.6.2 to 1.7.3 (#4176)",
        "link": "https://github.com/Velocidex/velociraptor/commit/cffeae708d886d973d24ab3efccff71b48b6cdf5",
        "tags": []
    }
]



def test_github_atom_parser():    
    xml_file_path = files("tests.resources") / "github.atom"
    with xml_file_path.open("r", encoding="utf-8") as f:
        xml_content = f.read()
        result = atom_parser(xml_content)
        print(result)
        assert result == expected_result