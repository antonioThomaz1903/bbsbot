import asyncio
import mss
import pyautogui
from core import capturar_tela, procurar_imagem, ASSETS


async def task_event_farm(log):
    logprefix = "[EVENT FARM]"
    def tasklog(str:str):
        log(f"{logprefix} - {str}")

    tasklog("Iniciando task EVENT FARM")
    tentativas_sem_close = 0
    fechou_pelo_menos_um = False

    with mss.MSS() as sct:
        estado = "START_QUEST"

        while True:

            tela = await asyncio.to_thread(capturar_tela, sct)

            if estado == "START_QUEST":
                encontrado = await asyncio.to_thread(lambda: procurar_imagem(tela, ASSETS / "botoes" / "start_quest.png"))

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(f"Encontrou botão START QUEST com confianca: {confianca:.2f}")


                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    estado = "WAITING_START"

            elif estado == "WAITING_START":
                encontrado = await asyncio.to_thread(
                    lambda: procurar_imagem(tela, ASSETS / "botoes" / "start_quest.png"))

                if encontrado:
                    tasklog("Esperando iniciar quest")
                    x, y, confianca = encontrado
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))

                else:
                    tasklog("Quest iniciada")
                    estado = "FINALIZAR_QUEST"


            elif estado == "FINALIZAR_QUEST":

                encontrado = await asyncio.to_thread(lambda: procurar_imagem(tela, ASSETS / "botoes" / "event_tap_screen.png"))
                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(f"Encontrou botão TAP SCREEN com confianca: {confianca:.2f}")
                    await asyncio.sleep(2)
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    await asyncio.sleep(2)
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    estado = "FECHAR_AVISOS"

            if estado == "FECHAR_AVISOS":
                encontrado = await asyncio.to_thread(
                    procurar_imagem,
                    tela,
                    ASSETS / "botoes" / "close.png",
                )

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(
                        f"Encontrou botão CLOSE com confiança: {confianca:.2f}"
                    )
                    await asyncio.sleep(0.3)
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    fechou_pelo_menos_um = True
                    tentativas_sem_close = 0
                    await asyncio.sleep(1.2)


                else:
                    if fechou_pelo_menos_um:
                        tentativas_sem_close += 1
                        if tentativas_sem_close >= 15:
                            tasklog(
                                "Primeiro CLOSE fechado e nenhum extra encontrado. Avançando..."
                            )
                            fechou_pelo_menos_um = False
                            tentativas_sem_close = 0
                            estado = "ESPERANDO_RETRY"


            elif estado == "ESPERANDO_RETRY":
                encontrado = await asyncio.to_thread(lambda: procurar_imagem(tela, ASSETS / "botoes" / "event_retry.png"))

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(f"Encontrou botão RETRY com confianca: {confianca:.2f}")
                    await asyncio.sleep(0.5)
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    estado = "START_QUEST"

            encontrado = await asyncio.to_thread(lambda: procurar_imagem(tela, ASSETS / "botoes" / "close.png"))
            if encontrado:
                x, y, confianca = encontrado
                tasklog(f"Encontrou botão CLOSE com confianca: {confianca:.2f}")
                await asyncio.sleep(0.15)
                await asyncio.to_thread(lambda: pyautogui.click(x, y))

            await asyncio.sleep(0.25)