from datetime import datetime
import xml.etree.ElementTree as ET

ARQUIVO = "UrbanDrive_XMLTV.xml"
  # Caminho do seu arquivo XMLTV
LIMITE_HORAS = 4             # Programas com duração acima disso serão listados

def analisar_programas_longo(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    programas_longos = []

    for prog in root.findall('programme'):
        titulo = prog.find('title').text if prog.find('title') is not None else "Sem título"
        canal = prog.get('channel')

        start_raw = prog.get('start').split()[0]
        stop_raw = prog.get('stop').split()[0]

        # Formato: 20250616125018 → %Y%m%d%H%M%S
        start = datetime.strptime(start_raw, "%Y%m%d%H%M%S")
        stop = datetime.strptime(stop_raw, "%Y%m%d%H%M%S")
        duracao = stop - start

        if duracao.total_seconds() > LIMITE_HORAS * 3600:
            programas_longos.append({
                'canal': canal,
                'titulo': titulo,
                'inicio': start,
                'fim': stop,
                'duracao_horas': round(duracao.total_seconds() / 3600, 2)
            })

    return programas_longos

# Executar e mostrar
resultados = analisar_programas_longo(ARQUIVO)
if resultados:
    print(f"Programas com duração maior que {LIMITE_HORAS} horas:")
    for prog in resultados:
        print(f"- {prog['canal']} | {prog['titulo']} | {prog['inicio']} → {prog['fim']} ({prog['duracao_horas']}h)")
else:
    print("Nenhum programa com duração acima do limite encontrado.")
