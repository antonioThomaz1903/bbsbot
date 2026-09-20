import cv2
import numpy as np
import mss
import pyautogui
import time
from pathlib import Path


ASSETS = Path("assets")
CONFIANCA_MINIMA = 0.85


def capturar_tela(sct):
    monitor = sct.monitors[1]

    screenshot = sct.grab(monitor)

    tela = np.array(screenshot)
    tela = cv2.cvtColor(tela, cv2.COLOR_BGRA2BGR)

    return tela


def procurar_imagem(tela, caminho):
    template = cv2.imread(str(caminho))

    if template is None:
        print(f"ERRO: não consegui abrir {caminho}")
        return None

    resultado = cv2.matchTemplate(
        tela,
        template,
        cv2.TM_CCOEFF_NORMED
    )

    _, confianca, _, posicao = cv2.minMaxLoc(resultado)

    if confianca < CONFIANCA_MINIMA:
        return None

    altura, largura = template.shape[:2]

    x = posicao[0] + largura // 2
    y = posicao[1] + altura // 2

    return x, y, confianca

def procurar_imagens(tela, imagens):
    melhor = None

    for imagem in imagens:
        resultado = procurar_imagem(tela, imagem)

        if resultado:
            x, y, confianca = resultado

            if melhor is None or confianca > melhor["confianca"]:
                melhor = {
                    "imagem": imagem.name,
                    "x": x,
                    "y": y,
                    "confianca": confianca,
                }

    return melhor

def main():
    imagens = list(ASSETS.glob("*.png"))

    print("Imagens carregadas:")

    for imagem in imagens:
        print(" -", imagem)

    print("\nBot iniciado. CTRL+C para parar.\n")

    with mss.MSS() as sct:
        estado = "START_QUEST"

        while True:

            tela = capturar_tela(sct)

            if estado == "INICIO":
                print("PREPARE FOR QUEST")
                time.sleep(0.5)
                encontrado = procurar_imagem(tela, ASSETS / "botoes" / "prepare_button.png")

                if encontrado:
                    x, y, confianca = encontrado
                    pyautogui.click(x, y)
                    estado = "START_QUEST"

            if estado == "START_QUEST":
                print("START QUEST")
                encontrado = procurar_imagem(
                    tela,
                    ASSETS / "botoes" / "start_quest.png"
                )

                if encontrado:
                    time.sleep(2.5)
                    x, y, confianca = encontrado
                    pyautogui.click(x, y)
                    estado = "FINALIZAR QUEST"

            elif estado == "FINALIZAR QUEST":

                encontrado = procurar_imagem(
                    tela,
                    ASSETS / "botoes" / "epic_raid_tap_screen_button.png"
                )

                if encontrado:
                    time.sleep(2)
                    x, y, confianca = encontrado
                    pyautogui.click(x, y)
                    time.sleep(2)
                    pyautogui.click(x, y)
                    estado = "ESPERANDO_RETRY"


            elif estado == "ESPERANDO_RETRY":
                print("ESPERANDO RETRY")
                time.sleep(3)
                encontrado = procurar_imagem(
                    tela,
                    ASSETS / "botoes" / "event_retry.png"
                )

                encontrado_close = procurar_imagem(
                    tela,
                    ASSETS / "botoes" / "close.png"
                )

                if encontrado:
                    time.sleep(0.5)
                    x, y, confianca = encontrado
                    pyautogui.click(x, y)
                    estado = "START_QUEST"

                if encontrado_close:
                    time.sleep(0.5)
                    x, y, confianca = encontrado_close
                    pyautogui.click(x, y)
                    time.sleep(1)

if __name__ == "__main__":
    main()