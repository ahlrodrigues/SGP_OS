from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
import fnmatch
import threading
import tkinter as tk
from tkinter import messagebox

# Carrega as variáveis do .env
load_dotenv()

LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")

# Função principal de execução

def executar_em_silencio():
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("http://sgp.net4you.com.br:8000/admin/atendimento/relatorios/ocorrencia/os/")

        # LOGIN
        campo_login = wait.until(EC.presence_of_element_located((By.ID, "id_username")))
        campo_senha = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        botao_entrar = wait.until(EC.element_to_be_clickable((By.ID, "entrar")))
        time.sleep(5)
        campo_login.send_keys(LOGIN)
        campo_senha.send_keys(SENHA)
        botao_entrar.click()

        # Seleciona status "Aberta"
        campo_status = wait.until(EC.presence_of_element_located((By.ID, "id_status")))
        seletor_status = Select(campo_status)
        seletor_status.deselect_all()
        seletor_status.select_by_value("0")

        # Seleciona técnicos com JavaScript
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

        # Seleciona 'Conclusão Checklist'
        campo_select2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select2-selection--multiple")))
        campo_select2.click()
        input_select2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.select2-search__field")))
        input_select2.send_keys("Conclusão Checklist")
        opcao = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Conclusão Checklist')]")))
        opcao.click()

        # Consulta e exporta Excel
        driver.find_element(By.XPATH, "//input[@value='Consultar']").click()
        time.sleep(20)
        try:
            botao_excel = wait.until(EC.element_to_be_clickable((By.ID, "idprintexcel1")))
            botao_excel.click()
        except:
            time.sleep(5)
            driver.find_element(By.ID, "idprintexcel1").click()

        # Confirma se o arquivo foi baixado
        downloads_path = os.path.expanduser("~/Downloads")
        arquivos = os.listdir(downloads_path)
        lista_arquivos = [os.path.join(downloads_path, f) for f in arquivos if fnmatch.fnmatch(f.lower(), "ordemservico*.xlsx")]
        if not lista_arquivos:
            raise Exception("Nenhum arquivo de ordem de serviço encontrado.")
        ARQUIVO = max(lista_arquivos, key=os.path.getmtime)

        # Pop-up de sucesso
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Relatório", "Relatório de O.S. baixado com sucesso!")

    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erro", f"Erro: {str(e)}")
    finally:
        driver.quit()

# Executa em segundo plano
thread = threading.Thread(target=executar_em_silencio)
thread.start()
