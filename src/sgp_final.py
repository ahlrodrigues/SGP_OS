from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
import requests
import mimetypes
import glob
import fnmatch

# Carrega as variáveis do .env
load_dotenv()

LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")
ACCESS_TOKEN = os.getenv("MATRIX_TOKEN")

# Inicia navegador
driver = webdriver.Firefox()
driver.get("http://sgp.net4you.com.br:8000/admin/atendimento/relatorios/ocorrencia/os/")
wait = WebDriverWait(driver, 10)

# LOGIN
campo_login = wait.until(EC.presence_of_element_located((By.ID, "id_username")))
campo_senha = wait.until(EC.presence_of_element_located((By.NAME, "password")))
botao_entrar = wait.until(EC.element_to_be_clickable((By.ID, "entrar")))
time.sleep(5)
campo_login.send_keys(LOGIN)
campo_senha.send_keys(SENHA)
botao_entrar.click()

# Seleciona status "Aberta"
try:
    campo_status = wait.until(EC.presence_of_element_located((By.ID, "id_status")))
    seletor_status = Select(campo_status)
    seletor_status.deselect_all()
    seletor_status.select_by_value("0")
    print("✅ Opção 'Aberta' selecionada com sucesso.")
except Exception as e:
    print("❌ Erro ao selecionar 'Aberta':", e)

# Seleciona técnicos com JavaScript
try:
    tecnicos_para_selecionar = ["JOAO PAULO", "ELIAS", "CABRAL", "DIEGO", "ERIKI", "FRANCIVALDO", "MICAEL"]
    nomes_js = "[" + ",".join([f'\"{nome}\"' for nome in tecnicos_para_selecionar]) + "]"
    js_code = f"""
    var select = document.getElementById('id_tecnicos');
    var nomes = {nomes_js};
    for (var i = 0; i < select.options.length; i++) {{
        if (nomes.includes(select.options[i].text)) {{
            select.options[i].selected = true;
        }}
    }}
    $('#id_tecnicos').trigger('change');
    """
    driver.execute_script(js_code)
    print("✅ Técnicos selecionados com JavaScript.")
except Exception as e:
    print(f"❌ Erro ao selecionar técnicos via JS: {e}")

# Seleciona 'Conclusão Checklist'
campo_select2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select2-selection--multiple")))
campo_select2.click()
input_select2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.select2-search__field")))
input_select2.send_keys("Conclusão Checklist")
opcao = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Conclusão Checklist')]")))
opcao.click()
print("✅ 'Conclusão Checklist' foi selecionado.")

# Consulta e exporta Excel
driver.find_element(By.XPATH, "//input[@value='Consultar']").click()
time.sleep(20)
try:
    botao_excel = wait.until(EC.element_to_be_clickable((By.ID, "idprintexcel1")))
    botao_excel.click()
    print("✅ Clique no botão Excel realizado.")
except:
    print("❌ Falha ao clicar. Tentando novamente após 5s...")
    time.sleep(5)
    driver.find_element(By.ID, "idprintexcel1").click()

# ===== ENVIO VIA MATRIX COM TOKEN DO .env =====
HOMESERVER = "https://matrix.net4you.com.br"
ROOM_ID = "!plCAQfAehDyLoWWoqr:matrix.net4you.com.br"

# Localiza o arquivo mais recente com padrão 'ordemservico*.xlsx'
arquivos = os.listdir("/home/ahlr/Downloads")
lista_arquivos = [os.path.join("/home/ahlr/Downloads", f) for f in arquivos if fnmatch.fnmatch(f.lower(), "ordemservico*.xlsx")]
if not lista_arquivos:
    raise Exception("Nenhum arquivo de ordem de serviço encontrado.")
ARQUIVO = max(lista_arquivos, key=os.path.getmtime)
print(f"📁 Arquivo mais recente encontrado: {ARQUIVO}")

# Sessão com token
session = requests.Session()
session.headers.update({"Authorization": f"Bearer {ACCESS_TOKEN}"})

# Upload do arquivo
def upload_arquivo():
    url = f"{HOMESERVER}/_matrix/media/r0/upload"
    nome = os.path.basename(ARQUIVO)
    mime, _ = mimetypes.guess_type(ARQUIVO)
    mime = mime or "application/octet-stream"
    with open(ARQUIVO, "rb") as f:
        headers = {"Content-Type": mime}
        params = {"filename": nome}
        resp = session.post(url, headers=headers, params=params, data=f)
        if resp.status_code != 200:
            raise Exception("Erro no upload: " + resp.text)
        return resp.json()["content_uri"]

# Envia mensagem com arquivo
def enviar_mensagem(content_uri):
    nome = os.path.basename(ARQUIVO)
    mime, _ = mimetypes.guess_type(ARQUIVO)
    mime = mime or "application/octet-stream"
    tamanho = os.path.getsize(ARQUIVO)
    txn_id = int(time.time())
    url = f"{HOMESERVER}/_matrix/client/r0/rooms/{ROOM_ID}/send/m.room.message/{txn_id}"
    payload = {
        "msgtype": "m.file",
        "body": nome,
        "url": content_uri,
        "info": {
            "mimetype": mime,
            "size": tamanho
        }
    }
    resp = session.put(url, json=payload)
    if resp.status_code not in (200, 201):
        raise Exception("Erro ao enviar mensagem: " + resp.text)
    print("✅ Arquivo enviado com sucesso!")
    os.remove(ARQUIVO)
        print(f"🧹 Arquivo local removido: {ARQUIVO}")
# Execução principal
if __name__ == "__main__":
    try:
        uri = upload_arquivo()
        print(f"📄 Upload OK: {uri}")
        enviar_mensagem(uri)
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        driver.quit()
        print("🧹 Navegador fechado.")
