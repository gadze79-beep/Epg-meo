
import datetime
import xml.etree.ElementTree as ET
import requests

# API pública de EPG de Portugal (rápida e sem bloqueios)
API_URL = "https://www meo.pt/..." # Substituído por fonte pública universal

def obter_epg_portugal():
    tv = ET.Element('tv')

    # Lista de canais principais da grelha PT
    canais_alvo = [
        {"id": "DAZN1.pt", "name": "DAZN 1", "query": "DAZN 1"},
        {"id": "DAZN2.pt", "name": "DAZN 2", "query": "DAZN 2"},
        {"id": "RTP1.pt", "name": "RTP 1", "query": "RTP 1"},
        {"id": "SIC.pt", "name": "SIC", "query": "SIC"},
        {"id": "TVI.pt", "name": "TVI", "query": "TVI"},
        {"id": "SPORTTV1.pt", "name": "Sport TV 1", "query": "SPORT TV 1"}
    ]

    # API de backup com dados EPG estruturados
    url_epg = "https://raw.githubusercontent.com/iptv-org/epg/master/providers/meo.pt/guide.xml"

    try:
        res = requests.get(url_epg, timeout=30)
        if res.status_code == 200:
            with open("epg_meo.xml", "wb") as f:
                f.write(res.content)
            print("EPG descarregado e gerado com sucesso!")
            return
    except Exception as e:
        print(f"Erro ao obter EPG secundário: {e}")

    # Fallback estruturado básico caso a rede falhe
    for c in canais_alvo:
        channel = ET.SubElement(tv, 'channel', id=c['id'])
        display = ET.SubElement(channel, 'display-name')
        display.text = c['name']

    tree = ET.ElementTree(tv)
    tree.write('epg_meo.xml', encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    obter_epg_portugal()
