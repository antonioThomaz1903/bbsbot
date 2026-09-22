import asyncio
import mss
import pyautogui
from core import ASSETS, capturar_tela, procurar_imagem


async def task_epic_raid(log):
    log_prefix = "[EPIC RAID]"

    def tasklog(mensagem: str):
        log(f"{log_prefix} - {mensagem}")

    tasklog("Iniciando task EPIC RAID")

    estado = "CREATE_ROOM"

    with mss.MSS() as sct:
        while True:
            tela = await asyncio.to_thread(capturar_tela, sct)

            if estado == "CREATE_ROOM":
                encontrado = await asyncio.to_thread(
                    procurar_imagem,
                    tela,
                    ASSETS / "botoes" / "epic_raid_create_room_button.png",
                )

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(
                        f"Encontrou botão CREATE ROOM com confiança: {confianca:.2f}"
                    )
                    await asyncio.sleep(0.25)

                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    estado = "START_QUEST"

            elif estado == "START_QUEST":
                encontrado = await asyncio.to_thread(
                    procurar_imagem,
                    tela,
                    ASSETS / "botoes" / "epic_raid_start_quest_5_button.png",
                )

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(
                        f"Encontrou botão START QUEST com confiança: {confianca:.2f}"
                    )
                    await asyncio.sleep(0.1)

                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    estado = "WAITING_START"

            elif estado == "WAITING_START":
                encontrado = await asyncio.to_thread(
                    procurar_imagem,
                    tela,
                    ASSETS / "botoes" / "epic_raid_start_quest_5_button.png",
                )

                if encontrado is None:
                    tasklog("Iniciando quest")
                    estado = "ENDING_QUEST"
                else:
                    x, y, confianca = encontrado
                    tasklog(
                        f"Encontrou botão START QUEST com confiança: {confianca:.2f}"
                    )
                    await asyncio.sleep(0.25)
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))

            elif estado == "ENDING_QUEST":
                encontrado = await asyncio.to_thread(
                    procurar_imagem,
                    tela,
                    ASSETS / "botoes" / "epic_raid_tap_screen_button.png",
                )

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(
                        f"Encontrou botão TAP SCREEN com confiança: {confianca:.2f}"
                    )
                    await asyncio.sleep(1.5)

                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    await asyncio.sleep(1.0)
                    await asyncio.to_thread(lambda: pyautogui.click(x, y))

                    estado = "RETRY_QUEST"

            elif estado == "RETRY_QUEST":
                encontrado = await asyncio.to_thread(
                    procurar_imagem,
                    tela,
                    ASSETS / "botoes" / "retry_button.png",
                )

                if encontrado:
                    x, y, confianca = encontrado
                    tasklog(
                        f"Encontrou botão RETRY com confiança: {confianca:.2f}"
                    )
                    await asyncio.sleep(0.25)

                    await asyncio.to_thread(lambda: pyautogui.click(x, y))
                    estado = "CREATE_ROOM"

            await asyncio.sleep(0.25)