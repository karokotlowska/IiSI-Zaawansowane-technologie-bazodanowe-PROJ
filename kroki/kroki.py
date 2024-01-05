import base64
import os.path
import zlib
import cairosvg
import requests
import glob
from config import output_dir, tmp_dir


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


def save_svg_diagram(path: str, diagram: str):
    with open(path, "wb") as f:
        f.write(diagram)


def convert_svg_to_png(svg_file_name, png_file_name):
    cairosvg.svg2png(url=svg_file_name, write_to=str(png_file_name), dpi=300)


def process_kroki_files():
    file_pattern = tmp_dir('description_for_kroki*.txt')
    kroki_files = glob.glob(file_pattern)

    for kroki_file in kroki_files:
        svg_diagram = get_diagram_svg(kroki_file, 'kroki.io')
        kroki_filename = os.path.basename(kroki_file)
        output_svg_file = output_dir(kroki_filename.replace('.txt', '_diagram.svg'))
        output_png_file = output_dir(kroki_filename.replace('.txt', '_diagram.png'))

        save_svg_diagram(output_svg_file, svg_diagram)
        convert_svg_to_png(output_svg_file, output_png_file)
