
import sys
import requests

def gerar_epg():
    # Fonte pública completa e atualizada diariamente com TODOS os canais de Portugal
    URL_EPG = "https://epg.pw/xmltv/epg_PT.xml"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print("A descarregar o EPG completo de Portugal...")
    try:
        response = requests.get(URL_EPG, headers=headers, timeout=60)

        if response.status_code == 200 and len(response.content) > 10000:
            with open("epg_meo.xml", "wb") as f:
                f.write(response.content)
            print("EPG descarregado e guardado com sucesso!")
        else:
            print(f"Erro ao descarregar: Status {response.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"Erro na execução: {e}")
        sys.exit(1)

if __name__ == "__main__":
    gerar_epg()
