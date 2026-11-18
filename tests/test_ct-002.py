import time
from datetime import datetime

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
from datetime import datetime

def capturar_tela(navegador, resultado):
    # Obtém a raiz do projeto
    pasta_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Define o diretório das evidências
    pasta_evidencias = os.path.join(pasta_raiz, "evidencias")

    # Obtém a data e a hora da execução
    data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Monta o caminho completo da imagem
    caminho_imagem = os.path.join(
        pasta_evidencias,
        f"add_amigo_{resultado}_{data_hora}.png"
    )

    # Captura a tela
    imagem_salva = navegador.save_screenshot(caminho_imagem)

    if imagem_salva:
        print(f"\nEvidência salva em: {caminho_imagem}")
    else:
        print("\nNão foi possível salvar a evidência.")

def test_add_amigo():
    navegador = webdriver.Chrome()

    try:
        navegador.maximize_window()

        # Acessa a página
        navegador.get("https://www.facebook.com/")
        time.sleep(2)

        # Preenche o usuário
        campo_email = WebDriverWait(navegador, 10).until(
         EC.element_to_be_clickable((By.NAME, "email"))
        )
        campo_email.send_keys("flavio.a3.2026@gmail.com")

        campo_senha = navegador.find_element(By.NAME, "pass")
        campo_senha.send_keys("flavio.pneu2026")

        botao_login = navegador.find_element(By.CSS_SELECTOR, "[aria-label='Entrar']")
        botao_login.click()
        
        WebDriverWait(
            navegador,
            40
        ).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[aria-label='Seu perfil']")
            )
        )

        time.sleep(5)

        campo_busca = navegador.find_element(By.CSS_SELECTOR, "input[type='search'][role='combobox']"
        )

        campo_busca.send_keys("Leo Messi")

        time.sleep(5)

        sugestao = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((
            By.CSS_SELECTOR, "li[role='option'] a[href*='q=leo%20messi']"
            ))
        )

        sugestao.click()

        link_messi = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "a[href*='facebook.com/leomessi']"
            ))
        )
        link_messi.click()

        botao_seguir = WebDriverWait(navegador, 10).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "div[role='button'][aria-label='Seguir']"
            ))
        )
        botao_seguir.click()

        # Captura a evidência de sucesso
        capturar_tela(navegador, "sucesso")

    except Exception:
        # Captura a evidência de falha
        capturar_tela(navegador, "falha")

        # Informa a falha ao pytest
        raise

    finally:
        # Executado antes de fechar o navegador,
        # independentemente do resultado do teste
        print("\nO navegador será fechado em 5 segundos...")
        time.sleep(5)

        navegador.quit()
