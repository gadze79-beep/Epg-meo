
import sys
import requests


def atualizar_epg():
  # Fonte XMLTV pública e atualizada com a grelha de Portugal (MEO, NOS, Vodafone)
  url_epg = "https://raw.githubusercontent.com/iptv-org/epg/master/providers/meo.pt/guide.xml"

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      )
  }

  print("A descarregar o guia de programação atualizado...")
  try:
    response = requests.get(url_epg, headers=headers, timeout=60)
    if response.status_code == 200 and len(response.content) > 500:
      with open("epg_meo.xml", "wb") as f:
        f.write(response.content)
      print("EPG descarregado e guardado em epg_meo.xml com sucesso!")
    else:
      print(f"Erro no download: Status {response.status_code}")
      sys.exit(1)
  except Exception as e:
    print(f"Exceção ao descarregar EPG: {e}")
    sys.exit(1)


if __name__ == "__main__":
  atualizar_epg()
