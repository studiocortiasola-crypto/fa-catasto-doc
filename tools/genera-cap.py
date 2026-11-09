"""Genera src/lib/core/dati/cap.generated.ts: i codici di avviamento postale di ogni comune, indicizzati per
codice catastale, a partire da comuni.json del progetto https://github.com/matteocontrini/comuni-json.
Uso: python3 tools/genera-cap.py <percorso comuni.json> [data AAAA-MM-GG dei dati]
Serve solo a proporre il CAP del dichiarante: il valore resta sempre modificabile."""
import json, sys, os, re, datetime

src = sys.argv[1]
dati = json.load(open(src, encoding='utf-8'))
righe = []
for c in dati:
    cod = (c.get('codiceCatastale') or '').strip().upper()
    cap = sorted({x.strip() for x in c.get('cap', []) if re.fullmatch(r'\d{5}', x.strip())})
    if re.fullmatch(r'[A-Z]\d{3}', cod) and cap:
        righe.append(f'{cod}|{",".join(cap)}')
righe.sort()
data = sys.argv[2] if len(sys.argv) > 2 else datetime.date.fromtimestamp(os.path.getmtime(src)).isoformat()
out = os.path.join(os.path.dirname(__file__), '..', 'src', 'lib', 'core', 'dati', 'cap.generated.ts')
with open(out, 'w', encoding='utf-8') as f:
    f.write('// GENERATO da tools/genera-cap.py a partire da comuni.json (github.com/matteocontrini/comuni-json).\n')
    f.write('// Formato: codice catastale|cap1,cap2,... una riga per comune.\n')
    f.write(f"export const DATA_CAP_INCORPORATI = '{data}';\n")
    f.write('export const CAP_INCORPORATI = `' + '\n'.join(righe) + '`;\n')
print(len(righe), 'comuni ->', out)
