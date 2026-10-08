
import datetime
import xml.etree.ElementTree as ET
import requests

API_URL = "https://www.meo.pt/_layouts/15/OTB.SP.MEO.EPG/Services/EPG.ashx/getPrograms"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}


def gerar_xml_epg():
  tv = ET.Element("tv")
  hoje = datetime.datetime.now().strftime("%Y-%m-%d")

  payload = {"date": hoje, "channel": ""}

  try:
    response = requests.post(
        API_URL, json=payload, headers=HEADERS, timeout=30
    )

    if response.status_code == 200:
      dados = response.json()
      canais = dados.get("channels", [])

      print(f"Foram encontrados {len(canais)} canais no MEO.")

      for ch in canais:
        canal_sigla = ch.get("sigla") or ch.get("callSign") or "CANAL"
        canal_nome = ch.get("name") or canal_sigla

        # Criar elemento do canal
        channel_elem = ET.SubElement(tv, "channel", id=f"{canal_sigla}.pt")
        display_name = ET.SubElement(channel_elem, "display-name")
        display_name.text = canal_nome

        # Criar elementos dos programas
        programas = ch.get("programs", [])
        for prog in programas:
          titulo = prog.get("name", "Sem Título")
          inicio_raw = prog.get("dateInterval", {}).get("start")
          fim_raw = prog.get("dateInterval", {}).get("end")

          if inicio_raw and fim_raw:
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
              channel=f"{canal_sigla}.pt",
          )
          title_elem = ET.SubElement(programme, "title", lang="pt")
          title_elem.text = titulo

          desc = prog.get("description")
          if desc:
            desc_elem = ET.SubElement(programme, "desc", lang="pt")
            desc_elem.text = desc

  except Exception as e:
    print(f"Erro ao ligar à API MEO: {e}")

  tree = ET.ElementTree(tv)
  tree.write("epg_meo.xml", encoding="utf-8", xml_declaration=True)
  print("Processo concluído com sucesso!")


if __name__ == "__main__":
  gerar_xml_epg()
