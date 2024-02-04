import tkinter as tk
from tkinter import ttk
import json
import ctypes as ct

import base64

def encode(data):
    try:
        # Standard Base64 Encoding
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        return str(encodedBytes, "utf-8")
    except:
        return ""
    
def decode(data):
    try:
        message_bytes = base64.b64decode(data)
        return message_bytes.decode('utf-8')
    except:
        return ""

your_code = encode("""

""")

exec(decode(your_code))