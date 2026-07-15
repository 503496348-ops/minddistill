import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'transformers_bridge.py'


def run_bridge(*args):
    return subprocess.check_output(
        [sys.executable, str(SCRIPT), *map(str, args)],
        cwd=ROOT,
        text=True,
    )


def test_transformers_bridge_sample_compact_json():
    out = run_bridge('--sample', '--compact', '--mode', 'inspect')
    data = json.loads(out)
    assert data['status'] in {'ok', 'degraded'}
    assert data['repo'] == 'huggingface/transformers'
    assert 'result' in data
    assert data['result']['char_count'] > 0
    assert data['result']['approx_token_count'] > 0


def test_transformers_bridge_text_input():
    out = run_bridge('--text', 'transformer-based SEO diagnostics for sample page', '--mode', 'token_count')
    data = json.loads(out)
    assert data['result']['char_count'] > 10
    assert isinstance(data['result']['extra']['transformers_version'], (str, type(None)))
