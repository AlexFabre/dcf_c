# dcf_c
Transform a `.dcf` or `.eds` into a C header

# Dependancies

~~~py
import argparse
import canopen
from datetime import datetime
import re
~~~

# Usage

~~~sh
python dcf_c.py <configuration/file.dcf> <generated/header/file.h> [--device=<PREFIX> --nodeID=<NODEID>]
~~~

- `--device` (optional. default value is "OD") a string literal that will prefix every object in the header (defnitions, struct, etc...)
