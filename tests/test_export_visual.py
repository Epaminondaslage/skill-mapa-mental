import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("export_visual", ROOT / "scripts" / "export_visual.py")
import sys
sys.path.insert(0, str(ROOT / "scripts"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ExportVisualTests(unittest.TestCase):
    def test_html_escapes_title(self):
        page = module.build_html('<script>alert(1)</script>', ['<svg xmlns="http://www.w3.org/2000/svg"></svg>'])
        self.assertIn('&lt;script&gt;', page)
        self.assertNotIn('<title><script>', page)
        self.assertIn('id="search"', page)

    def test_output_files(self):
        data = {"title":"Exemplo", "language":"pt-BR", "style":"tecnico",
                "sections":[{"title":"Etapa", "items":["Verificar conexão"]}]}
        with tempfile.TemporaryDirectory() as folder:
            status = module.export(data, folder)
            self.assertEqual(status["pages"], 1)
            self.assertTrue((Path(folder) / "mapa-01.svg").exists())
            self.assertTrue((Path(folder) / "mapa-interativo.html").exists())
            self.assertTrue((Path(folder) / "mapa.json").exists())
            if status["merged_pdf"]:
                from pypdf import PdfReader
                self.assertEqual(len(PdfReader(str(Path(folder) / "mapa-completo.pdf")).pages), 1)

if __name__ == "__main__":
    unittest.main()
