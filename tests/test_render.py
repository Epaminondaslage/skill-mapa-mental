import copy
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render import render_svg, validate

class RenderTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples" / "exemplo.json").read_text(encoding="utf-8"))

    def test_svg(self):
        self.assertIn("<svg", render_svg(self.data))
        self.assertIn("Mapas mentais", render_svg(self.data))

    def test_italian(self):
        data = json.loads((ROOT / "examples" / "esempio-it.json").read_text(encoding="utf-8"))
        self.assertIn("Mappe mentali", render_svg(data))

    def test_duplicate_id(self):
        data = copy.deepcopy(self.data)
        data["nodes"].append(dict(data["nodes"][0]))
        with self.assertRaises(ValueError):
            validate(data)

    def test_cycle(self):
        data = copy.deepcopy(self.data)
        data["nodes"][0]["parent"] = "radial"
        with self.assertRaises(ValueError):
            validate(data)

    def test_pdf_export_documented(self):
        script = (ROOT / "scripts" / "render.py").read_text(encoding="utf-8")
        self.assertIn("cairosvg.svg2pdf", script)
        self.assertIn('dest / "mapa.pdf"', script)

    def test_bad_language(self):
        data = copy.deepcopy(self.data)
        data["language"] = "en-US"
        with self.assertRaises(ValueError):
            validate(data)

if __name__ == "__main__":
    unittest.main()
