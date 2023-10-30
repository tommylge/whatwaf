# WhatWaf?

WhatWaf is an advanced firewall detection tool who's goal is to give you the idea of "There's a WAF?". WhatWaf works by detecting a firewall on a web application.

This repo is forked from https://github.com/Ekultek/WhatWaf and has been modified to fit my uses.

## How to Run

### Installation

Ensure you have Python installed and preferably inside a virtual environment.

1. Install the required packages:

```bash
pip install git+https://github.com/tommylge/whatwaf
```

### Usage
```py
import whatwaf

detected_protections = whatwaf.detection_main(response)
```
- `<response>`: Scrapy response object (must include body attribute).

Example return:
```py
[
    'cloudflare',
    'akamai',
    'perimeterx',
]
```