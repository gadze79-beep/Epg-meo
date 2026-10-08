

import datetime
import xml.etree.ElementTree as ET
import requests

# API Oficial do Guia TV MEO
API_URL = "https://www.meo.pt/_layouts/15/OTB.SP.MEO.EPG/Services/EPG.ashx/getPrograms"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}


def gerar_epg():
  tv = ET.Element("tv")

  # Obter data de hoje no formato YYYY-MM-DD
  hoje = datetime.datetime.now().strftime("%Y-%m-%d")

  payload = {"date": hoje, "channel": ""}

  try:
    response = requests.post(
        API_URL, json=payload, headers=HEADERS, timeout=30
    )
    dados = response.json()

    # Processar os canais e programas devolvidos pela API
    if "channels" in dados:
      for ch in dados["channels"]:
        canal_id = ch.get("sigla", ch.get("callSign", "canal"))
        canal_nome = ch.get("name", canal_id)

        # Adicionar definição do canal
        channel_elem = ET.SubElement(tv, "channel", id=f"{canal_id}.pt")
        display_name = ET.SubElement(channel_elem, "display-name")
        display_name.text = canal_nome

        # Adicionar programas do canal
        for prog in ch.get("programs", []):
          titulo = prog.get("name", "Sem título")

          # Datas no formato YYYYMMDDHHMMSS +0100
          inicio_raw = prog.get("dateInterval", {}).get("start")
          fim_raw = prog.get("dateInterval", {}).get("end")

          if inicio_raw and fim_raw:
            # Converter formato de data se necessário
            start_str = (
                inicio_raw.replace("-", "").replace(":", "").replace("T", "")
                + " +0100"
            )
            stop_str = (
                fim_raw.replace("-", "").replace(":", "").replace("T", "")
                + " +0100"
            )
          else:
            continue

          programme = ET.SubElement(
              tv,
              "programme",
              start=start_str,
              stop=stop_str,
              channel=f"{canal_id}.pt",
          )
          title_elem = ET.SubElement(programme, "title", lang="pt")
          title_elem.text = titulo

          if "description" in prog and prog["description"]:
            desc_elem = ET.SubElement(programme, "desc", lang="pt")
            desc_elem.text = prog["description"]

  except Exception as e:
    print(f"Erro ao obter dados da API: {e}")

  tree = ET.ElementTree(tv)
  tree.write("epg_meo.xml", encoding="utf-8", xml_declaration=True)
  print("Ficheiro epg_meo.xml gerado com sucesso!")


if __name__ == "__main__":
  gerar_epg()
