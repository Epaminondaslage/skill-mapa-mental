import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "render_infografico.py"
spec = importlib.util.spec_from_file_location("render_infografico", MODULE)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

class InfograficoTests(unittest.TestCase):
    def test_svg(self):
        data = {"title": "Rede & diagnóstico", "style": "tecnico", "sections": [{"title": "Verificar", "items": ["IP < gateway"]}]}
        pages = renderer.render_svg(data)
        self.assertEqual(len(pages), 1)
        self.assertIn("Rede &amp; diagnóstico", pages[0])
        self.assertIn("IP &lt; gateway", pages[0])

    def test_invalid_style(self):
        with self.assertRaises(ValueError):
            renderer.render_svg({"title": "X", "style": "inexistente", "sections": [{"title": "Y"}]})

    def test_pagination(self):
        sections = [{"title": f"Seção {i}", "items": ["Verificar configuração e registrar o resultado."] * 5} for i in range(12)]
        pages = renderer.render_svg({"title": "Diagnóstico", "sections": sections})
        self.assertGreater(len(pages), 1)
        self.assertEqual(sum(page.count('<circle cx=') for page in pages), 12 * 5 + 12)

    def test_decision_layout(self):
        data = {
            "title": "Qual estrutura usar?",
            "layout": "decision",
            "prompt": "Qual é a operação principal?",
            "branches": [
                {"title": "Acesso", "options": [
                    {"question": "Acesso por posição?", "result": "ARRAY", "detail": "Índice direto."}
                ]},
                {"title": "Ordem", "options": [
                    {"question": "Primeiro a entrar?", "result": "QUEUE", "detail": "Ordem FIFO."}
                ]}
            ]
        }
        pages = renderer.render_svg(data, orientation="portrait")
        self.assertEqual(len(pages), 1)
        self.assertIn("MAPA DE DECISÃO", pages[0])
        self.assertIn("ARRAY", pages[0])
        self.assertIn("QUEUE", pages[0])

    def test_decision_layout_rejects_missing_result(self):
        data = {
            "title": "Escolha",
            "layout": "decision",
            "prompt": "O que fazer?",
            "branches": [
                {"title": "A", "options": [{"question": "Pergunta?"}]},
                {"title": "B", "options": [{"question": "Pergunta?", "result": "Resposta"}]}
            ]
        }
        with self.assertRaises(ValueError):
            renderer.render_svg(data)

if __name__ == "__main__":
    unittest.main()
