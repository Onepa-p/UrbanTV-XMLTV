import requests
import xml.etree.ElementTree as ET

# Lista com dicionários dos feeds para processar
FEEDS = [
    {
        "name": "UrbanDrive",
        "url": "https://urbantv.com.br/epg/00/Urban-Drive.xml",
        "output_file": "UrbanDrive_XMLTV.xml"
    },
    {
        "name": "Otaku",
        "url": "https://urbantv.com.br/epg/00/Otaku.xml",
        "output_file": "Otaku_XMLTV.xml"
    },
    {
        "name": "UrbanTravel",
        "url": "https://urbantv.com.br/epg/00/Urban-Travel.xml",
        "output_file": "UrbanTravel_XMLTV.xml"
    }
]

def format_time(time_str):
    """
    Garante que o tempo esteja no formato XMLTV: YYYYMMDDHHMMSS ±HHMM
    """
    try:
        if ' ' in time_str:
            dt_part, tz_part = time_str.split(" ")
            dt = dt_part.replace("-", "").replace(":", "")
            return f"{dt} {tz_part}"
        else:
            return time_str
    except:
        return "20000101000000 +0000"

def convert_to_xmltv(xml_data):
    root = ET.fromstring(xml_data)
    
    tv = ET.Element("tv", attrib={
        "generator-info-name": "UrbanTV XML Converter",
        "generator-info-url": "https://urbantv.com.br"
    })

    # Adiciona canais
    for ch in root.findall("channel"):
        ch_id = ch.attrib.get("id", "unknown")
        channel_elem = ET.SubElement(tv, "channel", id=ch_id)
        for name in ch.findall("display-name"):
            ET.SubElement(channel_elem, "display-name", name.attrib).text = name.text

    # Adiciona programas
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

def process_feed(feed):
    try:
        print(f"🔄 Baixando XML da URL: {feed['url']}")
        response = requests.get(feed["url"])
        response.raise_for_status()

        print(f"✅ Convertendo feed '{feed['name']}' para XMLTV...")
        xmltv_bytes = convert_to_xmltv(response.content)

        with open(feed["output_file"], "wb") as f:
            f.write(xmltv_bytes)

        print(f"✅ Arquivo salvo: {feed['output_file']}\n")
    except Exception as e:
        print(f"❌ Erro no feed '{feed['name']}': {e}\n")

def main():
    for feed in FEEDS:
        process_feed(feed)

if __name__ == "__main__":
    main()
