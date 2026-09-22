import cv2
import numpy as np
from pathlib import Path
import mss
import pyautogui
import sys

CONFIANCA_MINIMA = 0.85
def get_assets_path() -> Path:
    """Retorna o caminho da pasta assets tanto em modo script (.py) quanto em executável (.exe)."""
    if getattr(sys, "frozen", False):
        # Quando compilado com PyInstaller (--onefile)
        return Path(sys._MEIPASS) / "assets"
    else:
        # Quando rodando via terminal/IDE (.py)
        return Path(__file__).resolve().parent / "assets"


# Mantenha a mesma variável ASSETS para o resto do código usar
ASSETS = get_assets_path()

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