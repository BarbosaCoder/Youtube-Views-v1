import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

# Configurações
TEST_URL = "https://www.youtube.com/watch?v=a4IXT7ORbNo"  # COLOQUE A URL QUE DESEJA VIEWS
# puro GPT
NUM_CYCLES = 5
VIEW_INTERVAL = (120, 180)  # 2-3 minutos em segundos, intervalo de visualização
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
]

# Inicialização
fake = Faker()
log = []

def setup_driver():
    """Configura o driver com opções realistas"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--lang=en-US,en;q=0.9")
    
    driver = webdriver.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def human_type(element, text, speed_variation=0.2):
    """Simula digitação humana com variação"""
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.05, 0.05 + speed_variation))

def simulate_view(driver):
    try:
        # 1. Navegação inicial com comportamento humano
        driver.get("https://www.google.com")
        time.sleep(random.uniform(1, 2.5))
        
        # 2. Busca orgânica variada
        search_terms = [
            f"{fake.word()} tutorial",
            f"how to {fake.word()}",
            f"{fake.word()} tips",
            "best " + fake.word()
        ]
        
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        
        human_type(search_box, random.choice(search_terms))
        time.sleep(random.uniform(0.8, 1.5))
        search_box.send_keys(Keys.RETURN)
        time.sleep(random.uniform(2, 4))
        
        # 3. Scroll humano
        for _ in range(random.randint(2, 4)):
            scroll_px = random.randint(300, 800)
            driver.execute_script(f"window.scrollBy(0, {scroll_px})")
            time.sleep(random.uniform(0.8, 2.2))
        
        # 4. Acesso ao vídeo
        driver.get(TEST_URL)
        time.sleep(random.uniform(3, 6))
        
        view_duration = random.randint(45, 180)  # 45s-3min
        start_time = time.time()
        
        # Simulação de interações
        while time.time() - start_time < view_duration:
            if random.random() > 0.6:
                scroll_px = random.randint(200, 500)
                driver.execute_script(f"window.scrollBy(0, {scroll_px})")
                time.sleep(random.uniform(1, 3))
            
            if random.random() > 0.85:
                try:
                    like_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.yt-spec-button-shape-next"))
                    )
                    ActionChains(driver).move_to_element(like_btn).pause(0.5).click().perform()
                    print(" - 👍 Curtiu o vídeo")
                    time.sleep(random.uniform(2, 4))
                except:
                    pass
            
            # Mudança de contexto
            if random.random() > 0.9:
                driver.switch_to.new_window('tab')
                driver.get("https://wikipedia.org")
                time.sleep(random.uniform(5, 12))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)
            
            time.sleep(random.uniform(3, 8))
        
        # Registrar a visualização
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration": view_duration,
            "search_term": search_terms,
            "user_agent": driver.execute_script("return navigator.userAgent;")
        }
        log.append(log_entry)
        print(f"✅ Visualização simulada ({view_duration}s)")
        return True
        
    except Exception as e:
        print(f"❌ Erro na simulação: {str(e)}")
        return False
    finally:
        # Fechar abas extras
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
        driver.switch_to.window(driver.window_handles[0])

def generate_report():
    """Gera relatório de atividades"""
    if not log:
        print("Nenhum dado para gerar relatório")
        return
    
    df = pd.DataFrame(log)
    df['duration'] = pd.to_numeric(df['duration'])
    
    # Salvar logs
    if not os.path.exists('logs'):
        os.makedirs('logs')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    df.to_csv(f'logs/view_log_{timestamp}.csv', index=False)
    
    # Gerar gráfico
    plt.figure(figsize=(10, 6))
    plt.bar(df['timestamp'], df['duration'], color='skyblue')
    plt.title('Histórico de Visualizações Simuladas')
    plt.xlabel('Horário')
    plt.ylabel('Duração (segundos)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'logs/view_report_{timestamp}.png')
    print(f"📊 Relatório salvo em logs/view_report_{timestamp}.png")

def main():
    print("🚀 Iniciando simulador de visualizações")
    driver = setup_driver()
    
    try:
        for i in range(1, NUM_CYCLES + 1):
            print(f"\n--- Ciclo {i}/{NUM_CYCLES} ---")
            simulate_view(driver)
            
            if i < NUM_CYCLES:
                wait_time = random.randint(*VIEW_INTERVAL)
                print(f"⏳ Próxima visualização em {wait_time//60} min {wait_time%60} seg...")
                time.sleep(wait_time)
        
        print("\nSimulação concluída! Gerando relatório...")
        generate_report()
        
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo usuário")
    finally:
        driver.quit()
        print("Navegador fechado")

if __name__ == "__main__":
    main()