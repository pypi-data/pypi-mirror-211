# robotframework-jsonquery [![tests](https://github.com/otemek/robotframework-jsonquery/actions/workflows/robotlib.yml/badge.svg?branch=master)](https://github.com/otemek/robotframework-jsonquery/actions/workflows/robotlib.yml) [![PyPI version](https://badge.fury.io/py/robotframework-jsonquery.svg)](https://badge.fury.io/py/robotframework-jsonquery)
Simple wrapper for libraries used to query json files with different query language implementations
- jsonpath-ng.ext (extended version with e.g. filters)
- jsonpath-ng
- jmespath

Example:
```Robot Framework
*** Settings ***
Library    JsonQuery    jsonpath-ng.ext

*** Test Cases ***
Read and query json file
    ${file}    Read Json File    sample.json
    ${result}   Query Json    ${file}    friends[?(@.id>1)]    #jsonpath-ng.ext syntax

```

```Robot Framework
*** Settings ***
Library    JsonQuery    jmespath

*** Test Cases ***
Read and query json file
    ${file}    Read Json File    sample.json
    ${result}   Query Json    ${file}    friends[?id>`1`]    #jmespath syntax

```

## Documentation
-   [Keyword Documentation](https://github.com/otemek/robotframework-jsonquery/doc/JsonQuery.html)
