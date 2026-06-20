import os
import io
import math
import asyncio
import requests
from PIL import Image
from mcrcon import MCRcon
from TikTokLive import TikTokLiveClient
from TikTokLive.events import LikeEvent

# ==========================================
# CONFIGURAÇÕES DE REDE E SEGURANÇA
# ==========================================
HOST_SERVIDOR  = "127.0.0.1"        # IP local do servidor Minecraft
SENHA_RCON     = "COLOQUE_SUA_SENHA_AQUI" # Senha protegida para o GitHub
TIKTOK_USERNAME = "seu_usuario_aqui" # Usuário da Live do TikTok

# ==========================================
# CONFIGURAÇÕES DO MINECRAFT E PALCO (V1)
# ==========================================
NOME_JOGADOR = "seu_usuario_aqui"            # Na V1, o apresentador é quem viaja e constrói

PALCO_X = -245      
PALCO_Y = -24       
PALCO_Z = -362      

DIRECAO_YAW   = -113   
DIRECAO_PITCH = -14     

TAMANHO_PAINEL   = 64   
DISTANCIA_PAINEL = 80   
AJUSTE_ALTURA    = -32   
AJUSTE_LATERAL   = -32  

painel_anterior = None
client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

# ==========================================
# MOTOR MATEMÁTICO (TRIGONOMETRIA DO ANTIGRAVITY)
# ==========================================
def _facing_pp(yaw_deg: int) -> str:
    yaw_mod = yaw_deg % 360
    if   yaw_mod < 45 or yaw_mod >= 315: return "south"
    elif 45 <= yaw_mod < 135: return "west"
    elif 135 <= yaw_mod < 225: return "north"
    else: return "east"

def _calcular_painel(palco_x, palco_y, palco_z, yaw_deg, distancia, tamanho, ajuste_altura, ajuste_lateral):
    rad = math.radians(yaw_deg)
    dx_costas = math.sin(rad)
    dz_costas = -math.cos(rad)
    dx_lat = dz_costas     
    dz_lat = -dx_costas

    meio = (tamanho // 2) + ajuste_lateral
    
    build_x = round(palco_x + dx_costas * distancia - dx_lat * meio)
    build_y = palco_y + ajuste_altura          
    build_z = round(palco_z + dz_costas * distancia - dz_lat * meio)

    fill_x1 = build_x
    fill_y1 = build_y
    fill_z1 = build_z
    fill_x2 = round(build_x + dx_lat * tamanho)
    fill_y2 = build_y + tamanho          
    fill_z2 = round(build_z + dz_lat * tamanho)

    if fill_x1 > fill_x2: fill_x1, fill_x2 = fill_x2, fill_x1
    if fill_y1 > fill_y2: fill_y1, fill_y2 = fill_y2, fill_y1
    if fill_z1 > fill_z2: fill_z1, fill_z2 = fill_z2, fill_z1

    cx = (fill_x1 + fill_x2) // 2
    cz = (fill_z1 + fill_z2) // 2
    cy = (fill_y1 + fill_y2) // 2   

    return {
        "build_x": build_x, "build_y": build_y, "build_z": build_z,
        "x1": fill_x1, "y1": fill_y1, "z1": fill_z1,
        "x2": fill_x2, "y2": fill_y2, "z2": fill_z2,
        "cx": cx, "cy": cy, "cz": cz,
        "facing": _facing_pp(yaw_deg),
    }

# ==========================================
# GESTÃO DE IMAGENS E I/O
# ==========================================
def processar_e_salvar_imagem(url_imagem):
    try:
        resposta = requests.get(url_imagem, timeout=10)
        if resposta.status_code == 200:
            imagem = Image.open(io.BytesIO(resposta.content))
            caminho_salvamento = os.path.join("plugins", "PixelPrinter", "images", "foto-live.png")
            os.makedirs(os.path.dirname(caminho_salvamento), exist_ok=True)
            imagem.save(caminho_salvamento)
            return True
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
    return False

def executar_comandos_minecraft():
    global painel_anterior
    p = _calcular_painel(PALCO_X, PALCO_Y, PALCO_Z, DIRECAO_YAW, DISTANCIA_PAINEL, TAMANHO_PAINEL, AJUSTE_ALTURA, AJUSTE_LATERAL)

    try:
        with MCRcon(HOST_SERVIDOR, SENHA_RCON, port=25575) as mcr:
            mcr.command("gamerule sendCommandFeedback false")

            # Se existia um painel antigo calculado pela matemática, limpa ele
            if painel_anterior:
                pa = painel_anterior
                print("⚡ V1 EFEITO: Raio caindo no centro do painel antigo...")
                mcr.command(f"summon lightning_bolt {pa['cx']} {pa['cy']} {pa['cz']}")
                import time
                time.sleep(0.4)
                mcr.command(f"fill {pa['x1']} {pa['y1']} {pa['z1']} {pa['x2']} {pa['y2']} {pa['z2']} air")
                time.sleep(0.2)

            # TELEPORTA A CONTA PRINCIPAL (Gera o piscar de tela na live)
            print("🕴️ V1: Teleportando o jogador principal para construir...")
            mcr.command(f"minecraft:tp {NOME_JOGADOR} {p['build_x']} {p['build_y']} {p['build_z']} {DIRECAO_YAW} {DIRECAO_PITCH}")
            import time
            time.sleep(0.15)

            print("🖨️ Desenhando estrutura...")
            mcr.command(f"sudo {NOME_JOGADOR} pp create {p['facing']} foto-live.png {TAMANHO_PAINEL}")
            time.sleep(2.5)

            # Devolve o jogador para o Palco
            mcr.command(f"minecraft:tp {NOME_JOGADOR} {PALCO_X} {PALCO_Y} {PALCO_Z} {DIRECAO_YAW} {DIRECAO_PITCH}")

            print("🎉 Show de encerramento e comemoração!")
            mcr.command(f"execute at {NOME_JOGADOR} run playsound entity.player.levelup player @a ~ ~ ~ 1 1")
            mcr.command(f"execute at {NOME_JOGADOR} run summon firework_rocket ~ ~2 ~ {{LifeTime:15,FireworksItem:{{id:firework_rocket,Count:1,tag:{{Fireworks:{{Explosions:[{{Type:1,Colors:[I;16711680,65280,255]}}]}}}}}}}}")
            mcr.command(f"effect give {NOME_JOGADOR} glowing 5 1 true")

            # A famosa PIRUETA de comemoração da V1 (Gira a tela do jogador)
            for _ in range(8):
                mcr.command(f"execute as {NOME_JOGADOR} at @s run minecraft:tp @s ~ ~ ~ ~45 ~")
                time.sleep(0.1)

            # Garante o alinhamento final da câmera olhando pro telão
            mcr.command(f"minecraft:tp {NOME_JOGADOR} {PALCO_X} {PALCO_Y} {PALCO_Z} {DIRECAO_YAW} {DIRECAO_PITCH}")

        # Guarda na memória a quina calculada para conseguir apagar no próximo Like
        painel_anterior = {
            "x1": p["x1"], "y1": p["y1"], "z1": p["z1"],
            "x2": p["x2"], "y2": p["y2"], "z2": p["z2"],
            "cx": p["cx"], "cy": p["cy"], "cz": p["cz"],
        }
        print("✅ Operação V1 realizada com sucesso!\n")

    except Exception as e:
        print(f"❌ Erro de conexão RCON com o Minecraft: {e}")

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    """Escuta os likes e extrai as informações da V1"""
    if event.total_likes % 500 == 0:
        print(f"🔥 Meta Atingida na V1 por {event.user.unique_id}!")
        url_foto = event.user.avatar.urls[0]
        
        loop = asyncio.get_running_loop()
        sucesso = await loop.run_in_executor(None, processar_e_salvar_imagem, url_foto)
        
        if sucesso:
            await loop.run_in_executor(None, executar_comandos_minecraft)

if __name__ == "__main__":
    print("==================================================")
    print("🎮 INICIALIZANDO: MOTOR V1 (TRIGONOMETRIA AO VIVO)")
    print("==================================================")
    try:
        client.run()
    except KeyboardInterrupt:
        print("\n🛑 Processo encerrado.")
