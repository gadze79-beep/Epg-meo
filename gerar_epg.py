
import datetime
import xml.etree.ElementTree as ET
import requests

# Endpoints da API da NOS TV
CANAIS_URL = (
    "https://api.nostv.pt/v2/channels"  # Obtém a lista completa de canais
)
EPG_URL = "https://api.nostv.pt/v2/epg/programs"  # Obtém a programação

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Origin": "https://nostv.pt",
    "Referer": "https://nostv.pt/",
}


def obter_todos_os_canais():
  """Procura todos os canais disponíveis na plataforma NOS TV."""
  try:
    res = requests.get(CANAIS_URL, headers=HEADERS, timeout=30)
    if res.status_code == 200:
      dados = res.json()
      # Retorna lista de canais da API
      return dados if isinstance(dados, list) else dados.get("channels", [])
  except Exception as e:
    print(f"Erro ao obter lista de canais: {e}")

  return []


def gerar_epg_completo_nos():
  tv = ET.Element("tv")
  hoje = datetime.datetime.now().strftime("%Y-%m-%d")

  print("A obter a lista de TODOS os canais da NOS TV...")
  canais = obter_todos_os_canais()

  if not canais:
    print(
        "A recorrer à fonte pública global de Portugal para garantir todos os"
        " canais..."
    )
    # Se a API direta recusar pedidos do GitHub, obtém o guia completo consolidado
    url_global = "https://raw.githubusercontent.com/iptv-org/epg/master/providers/nos.pt/guide.xml"
    res = requests.get(url_global, headers=HEADERS, timeout=60)
    if res.status_code == 200 and len(res.content) > 5000:
      with open("epg_meo.xml", "wb") as f:
        f.write(res.content)
      print("EPG com TODOS os canais gerado com sucesso!")
      return

  # Processar a lista de canais obtida da NOS
  for c in canais:
    channel_id = str(c.get("id") or c.get("callSign") or c.get("sigla"))
    channel_name = c.get("name") or c.get("title") or channel_id

    # Criar nó do canal
    channel_elem = ET.SubElement(
        tv, "channel", id=f"{channel_id}.pt"
    )  # Ex: 139.pt, DAZN1.pt
    display_name = ET.SubElement(channel_elem, "display-name")
    display_name.text = channel_name

  tree = ET.ElementTree(tv)
  tree.write("epg_meo.xml", encoding="utf-8", xml_declaration=True)
  print("Ficheiro com a lista total de canais atualizado!")


if __name__ == "__main__":
  gerar_epg_completo_nos()
