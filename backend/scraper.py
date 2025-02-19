import sqlite3
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do banco de dados SQLite
db_path = os.path.abspath("vagas.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vagas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT UNIQUE,
        link TEXT UNIQUE
    )
""")
conn.commit()

# Configurar o navegador Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Rodar em modo headless (sem abrir o navegador)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Variável para total de vagas encontradas
total_vagas_encontradas = 0

# Função para carregar todas as vagas do Vagas.com.br
def carregar_vagas_vagas():
    global total_vagas_encontradas
    print("[+] Acessando Vagas.com.br...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    driver.implicitly_wait(5)

    # Carregar todas as vagas clicando no botão "Mais Vagas"
    while True:
        try:
            botao = driver.find_element(By.ID, "maisVagas")
            botao.click()
            print("[+] Carregando mais vagas...")
            time.sleep(3)
        except NoSuchElementException:
            print("[+] Todas as vagas foram carregadas.")
            break

    # Coletar vagas
    base_url = "https://www.vagas.com.br"
    vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

    total = 0
    total_vagas = 0
    for vaga in vagas:
        titulo = vaga.text.strip()
        link = vaga.get_attribute("href")
        if link.startswith("/"):
            link = base_url + link

        # Inserir no banco, evitando duplicatas
        cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
        print(f"[+] {titulo} - {link}")
        total_vagas += 1
        total += 1

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do Grupo Fleury: {total_vagas}")

# Função para coletar vagas do NaturaCarreiras
def carregar_vagas_natura():
    global total_vagas_encontradas
    print("[+] Acessando NaturaCarreiras...")
    url_natura = "https://avon.wd5.myworkdayjobs.com/pt-BR/NaturaCarreiras"
    driver.get(url_natura)
    driver.implicitly_wait(5)

    total_vagas = 0
    pagina_atual = 1  # Controla a página atual

    while True:
        print(f"[+] Coletando vagas da página {pagina_atual}...")

        # Coletar as vagas da página atual
        vagas_natura = driver.find_elements(By.CSS_SELECTOR, "a.css-19uc56f")

        for vaga in vagas_natura:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")

            # Inserir no banco, evitando duplicatas
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link) VALUES (?, ?)", (titulo, link))
            print(f"[+] {titulo} - {link}")
            total_vagas += 1

        try:
            # Encontrar o botão da próxima página com base no número
            pagina_atual += 1
            botao_proxima = driver.find_element(By.XPATH, f"//button[@aria-label='page {pagina_atual}']")

            if "disabled" in botao_proxima.get_attribute("class"):  # Se estiver desativado, paramos
                print("[+] Última página alcançada. Encerrando...")
                break

            botao_proxima.click()
            print(f"[+] Avançando para a página {pagina_atual}...")
            time.sleep(3)  # Tempo para garantir o carregamento da página

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break  # Sai do loop quando não há mais páginas

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do NaturaCarreiras: {total_vagas}")


def carregar_vagas_raizen():
    global total_vagas_encontradas
    url = "https://genteraizen.gupy.io/"
    driver.get(url)
    driver.implicitly_wait(5)

    total_vagas = 0

    while True:
        print("[+] Coletando vagas da página atual...")

        # Captura os títulos das vagas
        vagas_raizen = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-gdyeKB hhuvfr-2')]")

        for vaga in vagas_raizen:
            titulo = vaga.text.strip()
            print(f"[+] {titulo}")
            total_vagas += 1

        # Tenta encontrar o botão da próxima página (numerado)
        try:
            # Encontra todos os botões de página numerados
            botoes_pagina = driver.find_elements(By.XPATH, "//button[contains(@class, 'pagination-page-button')]")

            # Verifica se o último botão não é o maior número
            if not botoes_pagina:
                print("[+] Não há mais páginas disponíveis.")
                break

            # Verifica o número da página atual e do próximo botão
            ultima_pagina = botoes_pagina[-1].text  # Último botão, que deve ser o maior número
            pagina_atual = botoes_pagina[-2].text  # Penúltimo botão, deve ser o número anterior

            # Se o número da página atual for igual ao número da última página, então não há mais páginas
            if pagina_atual == ultima_pagina:
                print("[+] Última página alcançada. Encerrando...")
                break

            # Usa JavaScript para clicar no próximo botão numerado
            driver.execute_script("arguments[0].click();", botoes_pagina[-1])
            print("[+] Avançando para a próxima página...")
            time.sleep(5)  # Aguarda carregamento

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break  # Sai do loop quando não há mais páginas

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas da Raízen: {total_vagas}")



def carregar_vagas_cosan():
    global total_vagas_encontradas
    url = "https://cosan.gupy.io/"
    driver.get(url)
    driver.implicitly_wait(5)

    total_vagas = 0

    while True:
        print("[+] Coletando vagas da página atual...")

        # Captura os títulos das vagas
        vagas_cosan = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-d1f2599d-2')]")

        for vaga in vagas_cosan:
            titulo = vaga.text.strip()
            print(f"[+] {titulo}")
            total_vagas += 1

        # Tenta encontrar o botão da próxima página
        try:
            # Tenta capturar o botão da próxima página
            botao_proxima = driver.find_element(By.XPATH, "//button[@data-testid='pagination-page-button']")

            # Verifica se o botão está visível e ativo
            if "disabled" in botao_proxima.get_attribute("class") or not botao_proxima.is_enabled():
                print("[+] Última página alcançada. Encerrando...")
                break  # Interrompe o loop se o botão estiver desabilitado ou invisível

            # Usa JavaScript para clicar no botão
            driver.execute_script("arguments[0].click();", botao_proxima)
            print("[+] Avançando para a próxima página...")
            time.sleep(5)  # Aguarda carregamento

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break  # Sai do loop quando o botão não for encontrado

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas da Cosan: {total_vagas}")


def carregar_vagas_cosan():
    global total_vagas_encontradas
    url = "https://cosan.gupy.io/"
    driver.get(url)
    driver.implicitly_wait(5)

    total_vagas = 0

    while True:
        print("[+] Coletando vagas da página atual...")

        # Captura os títulos das vagas
        vagas_cosan = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-d1f2599d-2')]")

        for vaga in vagas_cosan:
            titulo = vaga.text.strip()
            print(f"[+] {titulo}")
            total_vagas += 1

        # Tenta encontrar o botão da próxima página
        try:
            botao_proxima = driver.find_element(By.XPATH, "//button[@data-testid='pagination-page-button']")
            
            # Verifica se o botão está desativado
            if "disabled" in botao_proxima.get_attribute("class"):
                print("[+] Última página alcançada. Encerrando...")
                break  # Se o botão estiver desabilitado, encerra o loop.

            # Usa JavaScript para clicar no botão
            driver.execute_script("arguments[0].click();", botao_proxima)
            print("[+] Avançando para a próxima página...")
            time.sleep(5)  # Aguarda carregamento

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas da Cosan: {total_vagas}")


# Executar as funções de scraping
carregar_vagas_vagas()
carregar_vagas_natura()
carregar_vagas_raizen()
carregar_vagas_cosan()

# Exibir o total de vagas encontradas
print(f"[+] Total de vagas encontradas: {total_vagas_encontradas}")

# Salvar e fechar conexões
conn.commit()
conn.close()
driver.quit()

print("[+] Scraping finalizado e dados salvos no banco de dados!")
