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
        link TEXT UNIQUE,
        empresa TEXT
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

def carregar_vagas_vagas():
    global total_vagas_encontradas
    empresa = "Fleury"
    print("[+] Acessando Vagas.com.br...")
    url = "https://www.vagas.com.br/vagas-de-Fleury"
    driver.get(url)
    driver.implicitly_wait(5)

    while True:
        try:
            botao = driver.find_element(By.ID, "maisVagas")
            botao.click()
            print("[+] Carregando mais vagas...")
            time.sleep(3)
        except NoSuchElementException:
            print("[+] Todas as vagas foram carregadas.")
            break

    base_url = "https://www.vagas.com.br"
    vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

    total_vagas = 0
    for vaga in vagas:
        titulo = vaga.text.strip()
        link = vaga.get_attribute("href")
        if link.startswith("/"):
            link = base_url + link

        cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link, empresa) VALUES (?, ?, ?)", (titulo, link, empresa))
        print(f"[+] {titulo, empresa} - {link} ({empresa})")
        total_vagas += 1

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do Grupo Fleury: {total_vagas}")

def carregar_vagas_natura(): 
    global total_vagas_encontradas
    empresa = "Natura"
    print("[+] Acessando NaturaCarreiras...")
    url_natura = "https://avon.wd5.myworkdayjobs.com/pt-BR/NaturaCarreiras"
    driver.get(url_natura)
    driver.implicitly_wait(5)

    total_vagas = 0
    pagina_atual = 1

    while True:
        print(f"[+] Coletando vagas da página {pagina_atual}...")
        vagas_natura = driver.find_elements(By.CSS_SELECTOR, "a.css-19uc56f")

        for vaga in vagas_natura:
            titulo = vaga.text.strip()
            link = vaga.get_attribute("href")

            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link, empresa) VALUES (?, ?, ?)", (titulo, link, empresa))
            print(f"[+] {titulo, empresa} - {link} ({empresa})")
            total_vagas += 1

        try:
            pagina_atual += 1
            botao_proxima = driver.find_element(By.XPATH, f"//button[@aria-label='page {pagina_atual}']")

            if "disabled" in botao_proxima.get_attribute("class"):
                print("[+] Última página alcançada. Encerrando...")
                break

            botao_proxima.click()
            print(f"[+] Avançando para a página {pagina_atual}...")
            time.sleep(3)

        except NoSuchElementException:
            print("[+] Não há mais páginas disponíveis.")
            break

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas do NaturaCarreiras: {total_vagas}")

def carregar_vagas_raizen():
    global total_vagas_encontradas
    empresa = "Raízen"
    url = "https://genteraizen.gupy.io/"
    driver.get(url)

    total_vagas = 0

    while True:
        print("Acessando Raízen na Gupy")
        vagas_raizen = driver.find_elements(By.XPATH, "//a[@data-testid='job-list__listitem-href']")
        
        for vaga in vagas_raizen:
            titulo = vaga.get_attribute("aria-label").strip()
            link = vaga.get_attribute("href")
            
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link, empresa) VALUES (?, ?, ?)", (titulo, link, empresa))
            print(f"[+] {titulo, empresa} - {link} ({empresa})")
            total_vagas += 1

        conn.commit()
        
        try:
            botao_proximo = driver.find_element(By.XPATH, "//button[@data-testid='pagination-next-button']")
            
            if botao_proximo.get_attribute("aria-disabled") == "true":
                print("[+] Última página alcançada. Encerrando...")
                break

            driver.execute_script("arguments[0].click();", botao_proximo)
            print("[+] Avançando para a próxima página...")
            time.sleep(5)

        except NoSuchElementException:
            print("[+] Botão de próxima página não encontrado. Encerrando...")
            break

    total_vagas_encontradas += total_vagas
    print(f"[+] Total de vagas coletadas da Raízen: {total_vagas}")

def carregar_vagas_cosan():
    global total_vagas_encontradas
    empresa = "Cosan"
    url = "https://cosan.gupy.io/"
    driver.get(url)
    driver.implicitly_wait(5)

    total_vagas = 0

    while True:
        print("[+] Coletando vagas da página atual...")
        vagas_cosan = driver.find_elements(By.XPATH, "//div[contains(@class, 'sc-d1f2599d-2')]")

        for vaga in vagas_cosan:
            titulo = vaga.text.strip()
            cursor.execute("INSERT OR IGNORE INTO vagas (titulo, link, empresa) VALUES (?, ?, ?)", (titulo, "", empresa))
            print(f"[+] {titulo, empresa} ({empresa})")
            total_vagas += 1

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
