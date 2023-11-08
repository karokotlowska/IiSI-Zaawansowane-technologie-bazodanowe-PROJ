import sys
import base64
import zlib

import cairosvg
import requests

def generate_url_from_str(path: str, server_url: str) -> str:
    with open(path, 'rb') as f:
        diagram = f.read()
    url_diagram = base64.urlsafe_b64encode(zlib.compress(diagram, 9)).decode('ascii')
    url = f"https://{server_url}/erd/svg/{url_diagram}"
    return url

def get_diagram_svg(diagram: str, server_url: str) -> bytes:
    url = generate_url_from_str(diagram, server_url)
    r = requests.get(url)
    return r.content

def save_svg_diagram(path: str, diagram:str):
    with open(path, "wb") as f:
        f.write(diagram)

def convert_svg_to_png(file_name):
    png_file_name = file_name.replace('.svg', '.png')
    cairosvg.svg2png(url=file_name, write_to=str(png_file_name), dpi=300)
