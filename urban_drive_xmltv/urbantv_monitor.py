import requests
import xml.etree.ElementTree as ET
import time
import json
import os

CHECK_INTERVAL = 15 * 60
STATE_FILE = "urbantv_state.json"

CHANNELS = {
    "Otaku": {
        "url": "https://urbantv.com.br/epg/00/Otaku.xml",
        "output": "Otaku_XMLTV.xml",
    },
    "UrbanDrive": {
        "url": "https://urbantv.com.br/epg/00/Urban-Drive.xml",
        "output": "UrbanDrive_XMLTV.xml",
    },
     "UrbanTravel": {
        "url": "https://urbantv.com.br/epg/00/Urban-Travel.xml",
        "output": "UrbanTravel_XMLTV.xml",
    }
    # Pode adicionar mais canais aqui
    
}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def format_time(time_str):
    try:
        if ' ' in time_str:
            dt_part, tz_part = time_str.split(" ")
            dt = dt_part.replace("-", "").replace(":", "")
            return f"{dt} {tz_part}"
        else:
            return time_str
    except:
        return "20000101000000 +0000"

def convert_to_xmltv(xml_data, generator_name, generator_url):
    root = ET.fromstring(xml_data)
    tv = ET.Element("tv", attrib={
        "generator-info-name": generator_name,
        "generator-info-url": generator_url
    })
    for ch in root.findall("channel"):
        ch_id = ch.attrib.get("id", "unknown")
        channel_elem = ET.SubElement(tv, "channel", id=ch_id)
        for name in ch.findall("display-name"):
            ET.SubElement(channel_elem, "display-name", name.attrib).text = name.text
    for prog in root.findall("programme"):
        start = format_time(prog.attrib.get("start", ""))
        stop = format_time(prog.attrib.get("stop", ""))
        channel = prog.attrib.get("channel", "unknown")
        programme = ET.SubElement(tv, "programme", {
            "start": start,
            "stop": stop,
            "channel": channel
        })
        for child in prog:
            if child.tag in ["title", "desc", "category", "date"]:
                ET.SubElement(programme, child.tag, child.attrib).text = (child.text or "").strip()
            elif child.tag == "credits":
                credits_elem = ET.SubElement(programme, "credits")
                for credit in child:
                    ET.SubElement(credits_elem, credit.tag).text = (credit.text or "").strip()
    return ET.tostring(tv, encoding="utf-8", xml_declaration=True)

def check_and_update(channel_name, channel_info, state):
    headers = {}
    if channel_name in state:
        if state[channel_name].get("etag"):
            headers["If-None-Match"] = state[channel_name]["etag"]
        if state[channel_name].get("last_modified"):
            headers["If-Modified-Since"] = state[channel_name]["last_modified"]

    try:
        print(f"🔄 [{channel_name}] Verificando atualizações...")
        response = requests.get(channel_info["url"], headers=headers)

        if response.status_code == 304:
            print(f"✅ [{channel_name}] Sem alterações desde a última verificação.")
            return

        response.raise_for_status()

        state[channel_name] = {
            "etag": response.headers.get("ETag"),
            "last_modified": response.headers.get("Last-Modified")
        }

        print(f"✅ [{channel_name}] Arquivo atualizado, convertendo para XMLTV...")
        xmltv_bytes = convert_to_xmltv(
            response.content,
            generator_name=f"UrbanTV XML Converter - {channel_name}",
            generator_url="https://urbantv.com.br"
        )

        with open(channel_info["output"], "wb") as f:
            f.write(xmltv_bytes)

        print(f"✅ [{channel_name}] XMLTV salvo em: {channel_info['output']}\n")

    except requests.HTTPError as e:
        print(f"❌ [{channel_name}] Erro HTTP: {e}")
    except Exception as e:
        print(f"❌ [{channel_name}] Erro inesperado: {e}")

def main_loop():
    print("🚀 Iniciando monitoramento contínuo dos canais UrbanTV...\n")
    state = load_state()
    try:
        while True:
            for name, info in CHANNELS.items():
                check_and_update(name, info, state)
            save_state(state)
            print(f"⏳ Aguardando {CHECK_INTERVAL//60} minutos para próxima checagem...\n")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento interrompido pelo usuário. Salvando estado e saindo.")
        save_state(state)

if __name__ == "__main__":
    main_loop()
