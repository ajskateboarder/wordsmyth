# Rateboat scripting

This is an completely new pre-alpha project to add Lua scripting to Rateboat to let users extend rating however they prefer.

## Usage

Make sure you have Python and Lua 5.3 installed.

Clone this branch:

```bash
git clone https://github.com/themysticsavages/rateboat --depth=1 -b lua-scripting
```

Install the requirements and run the test script:

```bash
pip install -r requirements.txt
python3 test.py
```

All links from google.com with the CSS selector `a.gb4` should be printed to standard output.

## Todo

### Unfinished

- Modularize the code
- Support a web API
- Support fetching on primarily JS pages

### ✅ Finished

- Most HTTP methods
- POSTing with a body
- JSON and DOM API
