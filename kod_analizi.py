import ast
import re
from radon.complexity import cc_visit
from radon.metrics import h_visit
from pylint import epylint as lint

class KodAnalizcisi:
    def __init__(self):
        self.hatalar = []
        self.uyarilar = []
    
    def analiz_et(self, kod):
        self.hatalar = []
        self.uyarilar = []
        
        try:
            tree = ast.parse(kod)
            self.generic_visit(tree)
            
            self.karmasiklik_analizi(kod)
            self.yorum_analizi(kod)
            self.lint_analizi(kod)
            
            return {
                "hatalar": self.hatalar,
                "uyarilar": self.uyarilar
            }
        except SyntaxError as e:
            return {"hatalar": [f"Sözdizimi hatası: {str(e)}"]}
    
    def generic_visit(self, node):
        for child in ast.iter_child_nodes(node):
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            visitor(child)

    def visit_FunctionDef(self, node):
        if len(node.args.args) > 5:
            self.uyarilar.append(f"Fonksiyon çok fazla parametre alıyor: {node.name}")
        self.generic_visit(node)

    def karmasiklik_analizi(self, kod):
        complexity = cc_visit(kod)
        for item in complexity:
            if item.complexity > 10:
                self.uyarilar.append(f"{item.name} fonksiyonu çok karmaşık (CC: {item.complexity})")

    def yorum_analizi(self, kod):
        yorum_sayisi = len(re.findall(r'#.*$', kod, re.MULTILINE))
        if yorum_sayisi < len(kod.split('\n')) / 10:
            self.uyarilar.append("Daha fazla yorum eklemeyi düşünün")

    def lint_analizi(self, kod):
        (pylint_stdout, pylint_stderr) = lint.py_run(kod, return_std=True)
        for line in pylint_stdout:
            if line.strip():
                self.uyarilar.append(f"Lint uyarısı: {line.strip()}")

if __name__ == "__main__":
    analizci = KodAnalizcisi()
    ornek_kod = """
def cok_parametreli_fonksiyon(a, b, c, d, e, f):
    pass

for i in range(10000):
    print(i)
    """
    print(analizci.analiz_et(ornek_kod))
