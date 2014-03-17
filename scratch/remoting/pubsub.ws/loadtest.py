# loadtest.py
"""
this script pairs with loadtest.html for stressing the limits of websockets
"""

import sys
import subprocess

n = int(sys.argv[1]) if len(sys.argv)>=2 else 10

subprocess.call(["python2", "pubsub.py", "8080"] + ["/socks/%d" % d for d in range(n)])
