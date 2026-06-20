import time
from mcrcon import MCRcon

# ==========================================
# CONFIGURAÇÕES DO MINECRAFT E ATORES
# ==========================================
SENHA_RCON   = "COLOQUE_SUA_SENHA_AQUI"
NOME_JOGADOR = "nome do jogador"        # O Apresentador (Fica estático no palco)
NOME_BOT     = "BotConstrutor"  # O Estagiário (Trabalha invisível lá atrás)

PALCO_X = -245      
PALCO_Y = -24       
PALCO_Z = -362      

DIRECAO_YAW   = -113   
DIRECAO_PITCH = -14     
TAMANHO_PAINEL = 64   

# ==========================================
# 🕹️ PAINEL DE CONTROLE DA FOTO
# ==========================================
DIRECAO_FOTO  = "east"
DISTANCIA_Z   = 80   
AJUSTE_X      = -32  
AJUSTE_ALTURA = -32   

# ==========================================
# LÓGICA DO ROBÔ (ARQUITETURA DE DUBLÊ)
# ==========================================
BUILD_X = PALCO_X + AJUSTE_X
BUILD_Y = PALCO_Y + AJUSTE_ALTURA
BUILD_Z = PALCO_Z + DISTANCIA_Z

def simular_foto():
    try:
        with MCRcon("127.0.0.1", SENHA_RCON, port=25575) as mcr:
            mcr.command("gamerule sendCommandFeedback false")

            # Define a margem de segurança para engolir a foto velha
            if DIRECAO_FOTO in ["north", "south"]:
                x1, x2 = BUILD_X - 5, BUILD_X + TAMANHO_PAINEL + 5
                z1, z2 = BUILD_Z - 3, BUILD_Z + 3
            else:
                x1, x2 = BUILD_X - 3, BUILD_X + 3
                z1, z2 = BUILD_Z - 5, BUILD_Z + TAMANHO_PAINEL + 5
                
            y1, y2 = BUILD_Y - 2, BUILD_Y + TAMANHO_PAINEL + 2

            print("⚡ EFEITO: Raio de impacto e estilhaços no telão antigo!")
            # O raio cai a 15 blocos do palco, perfeitamente enquadrado na câmera
            mcr.command(f"summon lightning_bolt {PALCO_X} {PALCO_Y + 10} {PALCO_Z + 15}")
            time.sleep(0.3)
            
            # Obliterador com animação de blocos quebrando (destroy)
            mcr.command(f"fill {x1} {y1} {z1} {x2} {y2} {z2} air destroy")
            time.sleep(0.4)

            # Limpa as "bochechas" de blocos caídos no chão para evitar lag no mapa
            mcr.command("kill @e[type=item,distance=..150]")

            # TELEPORTA APENAS O BOT (A câmera da Live no Bravura não pisca!)
            print(f"🕴️ Posicionando o {NOME_BOT}...")
            mcr.command(f"minecraft:tp {NOME_BOT} {BUILD_X} {BUILD_Y} {BUILD_Z} {DIRECAO_YAW} {DIRECAO_PITCH}")
            time.sleep(0.15)

            # O BOT CONSTRÓI A ARTE
            print(f"🖨️ {NOME_BOT} está desenhando a nova imagem...")
            mcr.command(f"sudo {NOME_BOT} pp create {DIRECAO_FOTO} foto-live.png {TAMANHO_PAINEL}")
            time.sleep(2.5)

            # EFEITOS DE COMEMORAÇÃO NO PALCO DO APRESENTADOR
            print("🎉 Show de encerramento no palco principal!")
            mcr.command(f"execute at {NOME_JOGADOR} run playsound entity.player.levelup player @a ~ ~ ~ 1 1")
            mcr.command(f"execute at {NOME_JOGADOR} run summon firework_rocket ~ ~2 ~ {{LifeTime:15,FireworksItem:{{id:firework_rocket,Count:1,tag:{{Fireworks:{{Explosions:[{{Type:1,Colors:[I;16711680,65280,255]}}]}}}}}}}}")
            mcr.command(f"effect give {NOME_JOGADOR} glowing 5 1 true")

        print("✅ Simulação Concluída!\n")

    except Exception as e:
        print(f"❌ Erro de conexão com o Minecraft: {e}")

if __name__ == "__main__":
    print("="*40)
    print("🎮 SIMULADOR V2 (PRODUÇÃO / DUBLÊ DE CORPO)")
    print("="*40)
    while True:
        input("🔴 Aperte [ENTER] no teclado para simular...")
        simular_foto()