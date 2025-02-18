from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuração do Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Comente esta linha para ver o navegador abrindo

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL inicial
url = "https://www.vagas.com.br/vagas-de-Fleury"
driver.get(url)

# Aguarda carregamento inicial
driver.implicitly_wait(5)

# URL base para links relativos
base_url = "https://www.vagas.com.br"

# Lista para armazenar as vagas
vagas_coletadas = []

# Função para clicar no botão "mostrar mais vagas" até ele sumir
def carregar_todas_as_vagas():
    while True:
        try:
            # Localiza o botão "mostrar mais vagas"
            botao = driver.find_element(By.ID, "maisVagas")
            botao.click()  # Clica no botão
            print("[+] Carregando mais vagas...")
            time.sleep(3)  # Espera carregar o conteúdo
        except NoSuchElementException:
            print("[+] Todas as vagas foram carregadas.")
            break

# Carrega todas as vagas
carregar_todas_as_vagas()

# Encontra as vagas na página
vagas = driver.find_elements(By.CSS_SELECTOR, "h2.cargo a")

# Extrai título e link das vagas
for vaga in vagas:
    titulo = vaga.text.strip()
    link = vaga.get_attribute("href")

    # Corrige links relativos
    if link.startswith("/"):
        link = base_url + link

    vagas_coletadas.append((titulo, link))
    print(f"{titulo}\n{link}\n")

# Fecha o navegador
driver.quit()

# Salva as vagas em um arquivo
with open("vagas_fleury.txt", "w", encoding="utf-8") as file:
    for titulo, link in vagas_coletadas:
        file.write(f"{titulo}\n{link}\n\n")

print(f"[+] Scraping concluído. {len(vagas_coletadas)} vagas coletadas!")
