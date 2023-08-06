"""Library for handling json queries using different backends
"""

import json
from types import ModuleType

from importlib import import_module

from JsonQuery.queries import JmesPath, JsonPathNg, Querable

jsonParserModule = {
    "jmespath": JmesPath,
    "jsonpath_ng.ext": JsonPathNg,
    "jsonpath_ng": JsonPathNg,
}


class JsonQuery:
    ROBOT_LIBRARY_SCOPE = "SUITE"

    def __init__(self, query_module: str = "jmespath") -> None:
        """Initialize library with a module name used to parse syntax for a specific implementation

        Example:
        |   =Settings=  |
        |   Libraray    |   JsonQuery   |   jmespath        |   # initialize library with jmespath library |
        |   Libraray    |   JsonQuery   | jsonpath_ng.ext   |   # initialize library with jsonpath_ng.ext (extended version which handles filtering, etc.) |
        """
        self.imported_module: ModuleType = import_module(query_module)
        self.qmodule: Querable = jsonParserModule[query_module](self.imported_module)

    def get_query_module(self) -> str:
        """Get module name loaded in initialization

        Example:
        |   =Settings=      |
        |   Library         |   JsonQuery   |   `jmespath`  |
        | |
        |   =Keywords=      |
        | ... |
        |   ${module_name}  |   Get Module Name |
        |   Should Be Equal |   `jmespath`      |   ${module_name}  |
        """
        return f"{self.imported_module.__name__}"

    def read_json_file(self, file_path: str) -> dict:
        """Read json file using standard json module and return data in a dict format

        Example:
        | ... |
        |   =Test Cases=        |
        |   Read Sample File    |
        |                       | ${content} | Read Json File | /path/to/the/json/file.json \ \ \     # unix-like path |
        | ... |
        """
        with open(file_path, "r") as fl:
            content = json.load(fl)
        return content

    def query_json(self, document: dict, expression: str) -> dict:
        """Query json document/dictionary with a given expression using module of choice

        | ... |
        | =Keywords= |
        | ... | 
        | ${content} | Read Json File | /path/to/file.json |
        | ${query_result} | Query Json | ${content} | locations[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)} | #jmespath syntax |
        """
        result = self.qmodule.search(expression, document)
        return result
