import datetime
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.meo.pt"
GUIA_URL = f"{BASE_URL}/isites/tv/guiatv/Paginas/guia-tv-sapo.aspx"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def obter_lista_canais():
  try:
    response = requests.get(GUIA_URL, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(response.content, "html.parser")
    canais = []

    links_canais = soup.find_all(
        "a", href=re.compile(r"/canal/([A-Za-z0-9_-]+)")
    )

    for link in links_canais:
      href = link.get("href")
      match = re.search(r"/canal/([A-Za-z0-9_-]+)", href)
      if match:
        canal_id = match.group(1)
        nome_canal = link.text.strip() or canal_id
        if not any(c["id"] == canal_id for c in canais):
          canais.append({
              "id": canal_id,
              "nome": nome_canal,
              "url": (
                  f"{BASE_URL}/isites/tv/guiatv/Paginas/guia-tv-sapo.aspx/canal/{canal_id}"
              ),
          })
    return canais
  except Exception as e:
    print(f"Erro ao obter canais: {e}")
    return []


def extrair_programacao_canal(tv_elem, canal):
  try:
    response = requests.get(canal["url"], headers=HEADERS, timeout=10)
    if response.status_code != 200:
      return

    soup = BeautifulSoup(response.content, "html.parser")

    channel_elem = ET.SubElement(tv_elem, "channel", id=f"{canal['id']}.pt")
    display_name = ET.SubElement(channel_elem, "display-name")
    display_name.text = canal["nome"]

    program_cards = soup.find_all("a")
    hoje = datetime.datetime.now().strftime("%Y%m%d")

    for card in program_cards:
      h2 = card.find("h2")
      if not h2:
        continue

      titulo = h2.text.strip()
      texto_card = card.text.strip()

      hora_match = re.search(r"(\d{2}:\d{2})\s*-\s*(\d{2}:\d{2})", texto_card)

      if hora_match:
        hora_inicio, hora_fim = hora_match.groups()
        h_ini, m_ini = hora_inicio.split(":")
        h_fim, m_fim = hora_fim.split(":")

        start_str = f"{hoje}{h_ini}{m_ini}00 +0100"
        stop_str = f"{hoje}{h_fim}{m_fim}00 +0100"
      else:
        start_str = f"{hoje}000000 +0100"
        stop_str = f"{hoje}010000 +0100"

      programme = ET.SubElement(
          tv_elem,
          "programme",
          start=start_str,
          stop=stop_str,
          channel=f"{canal['id']}.pt",
      )
      title_elem = ET.SubElement(programme, "title", lang="pt")
      title_elem.text = titulo
  except Exception as e:
    print(f"Erro no canal {canal['id']}: {e}")


def gerar_epg_completo():
  tv = ET.Element("tv")
  canais = obter_lista_canais()

  print(f"Encontrados {len(canais)} canais.")

  for i, canal in enumerate(canais, 1):
    print(f"[{i}/{len(canais)}] A processar: {canal['nome']}")
    extrair_programacao_canal(tv, canal)

  tree = ET.ElementTree(tv)
  tree.write("epg_meo.xml", encoding="utf-8", xml_declaration=True)
  print("Ficheiro epg_meo.xml gerado com sucesso!")


if __name__ == "__main__":
  gerar_epg_completo()
