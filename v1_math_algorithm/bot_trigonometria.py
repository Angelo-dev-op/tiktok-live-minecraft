import math
import time
from mcrcon import MCRcon

# ==========================================
# CONFIGURAÇÕES DO MINECRAFT E PALCO
# ==========================================
SENHA_RCON   = "COLOQUE_SUA_SENHA_AQUI"
NOME_JOGADOR = "nome do jogador"

PALCO_X = -245      
PALCO_Y = -24       
PALCO_Z = -362      

DIRECAO_YAW   = -113   
DIRECAO_PITCH = -14     

TAMANHO_PAINEL = 64   
DISTANCIA_PAINEL = 80   
AJUSTE_ALTURA  = -32   
AJUSTE_LATERAL = -32  

painel_anterior = None

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

def simular_foto():
    global painel_anterior
    p = _calcular_painel(PALCO_X, PALCO_Y, PALCO_Z, DIRECAO_YAW, DISTANCIA_PAINEL, TAMANHO_PAINEL, AJUSTE_ALTURA, AJUSTE_LATERAL)

    try:
        with MCRcon("127.0.0.1", SENHA_RCON, port=25575) as mcr:
            mcr.command("gamerule sendCommandFeedback false")

            if painel_anterior:
                pa = painel_anterior
                print("⚡ Soltando o raio no painel antigo...")
                mcr.command(f"summon lightning_bolt {pa['cx']} {pa['cy']} {pa['cz']}")
                time.sleep(0.4)
                mcr.command(f"fill {pa['x1']} {pa['y1']} {pa['z1']} {pa['x2']} {pa['y2']} {pa['z2']} air")
                time.sleep(0.2)

            print("🕴️ Teleportando para construir...")
            mcr.command(f"minecraft:tp {NOME_JOGADOR} {p['build_x']} {p['build_y']} {p['build_z']} {DIRECAO_YAW} {DIRECAO_PITCH}")
            time.sleep(0.15)

            print("🖨️ Desenhando...")
            mcr.command(f"sudo {NOME_JOGADOR} pp create {p['facing']} foto-live.png {TAMANHO_PAINEL}")
            time.sleep(2.5)

            mcr.command(f"minecraft:tp {NOME_JOGADOR} {PALCO_X} {PALCO_Y} {PALCO_Z} {DIRECAO_YAW} {DIRECAO_PITCH}")

            print("🎉 Show de encerramento!")
            mcr.command(f"execute at {NOME_JOGADOR} run playsound entity.player.levelup player @a ~ ~ ~ 1 1")
            mcr.command(f"execute at {NOME_JOGADOR} run summon firework_rocket ~ ~2 ~ {{LifeTime:15,FireworksItem:{{id:firework_rocket,Count:1,tag:{{Fireworks:{{Explosions:[{{Type:1,Colors:[I;16711680,65280,255]}}]}}}}}}}}")
            mcr.command(f"effect give {NOME_JOGADOR} glowing 5 1 true")

            # A pirueta final da V1
            for _ in range(8):
                mcr.command(f"execute as {NOME_JOGADOR} at @s run minecraft:tp @s ~ ~ ~ ~45 ~")
                time.sleep(0.1)

            mcr.command(f"minecraft:tp {NOME_JOGADOR} {PALCO_X} {PALCO_Y} {PALCO_Z} {DIRECAO_YAW} {DIRECAO_PITCH}")

        painel_anterior = {
            "x1": p["x1"], "y1": p["y1"], "z1": p["z1"],
            "x2": p["x2"], "y2": p["y2"], "z2": p["z2"],
            "cx": p["cx"], "cy": p["cy"], "cz": p["cz"],
        }
        print("✅ Simulação Concluída!\n")

    except Exception as e:
        print(f"❌ Erro de conexão com o Minecraft: {e}")

if __name__ == "__main__":
    print("="*40)
    print("🎮 SIMULADOR V1 (ALGORITMO MATEMÁTICO)")
    print("="*40)
    while True:
        input("🔴 Aperte [ENTER] no teclado para simular...")
        simular_foto()