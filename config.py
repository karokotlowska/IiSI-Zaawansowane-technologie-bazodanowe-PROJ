import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, 'output')
TMP_DIR = os.path.join(ROOT_DIR, 'tmp')


def tmp_dir(filename: str) -> str:
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    return os.path.join(TMP_DIR, filename)


def output_dir(filename: str) -> str:
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    return os.path.join(OUTPUT_DIR, filename)


def delete_tmp_dir():
    if os.path.exists(TMP_DIR):
        for file in os.listdir(TMP_DIR):
            os.remove(os.path.join(TMP_DIR, file))
        os.rmdir(TMP_DIR)

def delete_output_dir():
    if os.path.exists(OUTPUT_DIR):
        for file in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, file))
        os.rmdir(OUTPUT_DIR)
