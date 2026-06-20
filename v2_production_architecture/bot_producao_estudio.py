import os
import io
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
# CONFIGURAÇÕES DOS ATORES DO JOGO
# ==========================================
NOME_JOGADOR   = "nome do jogador"          # O Apresentador (Fica estático no palco)
NOME_BOT       = "BotConstrutor"    # O Dublê (Trabalha em segundo plano)

PALCO_X = -245      
PALCO_Y = -24       
PALCO_Z = -362      

DIRECAO_YAW   = -113   
DIRECAO_PITCH = -14     
TAMANHO_PAINEL = 64   

# ==========================================
# 🕹️ COORDENADAS E AJUSTES DO PAINEL
# ==========================================
DIRECAO_FOTO  = "east"
DISTANCIA_Z   = 80   
AJUSTE_X      = -32  
AJUSTE_ALTURA = -32   

BUILD_X = PALCO_X + AJUSTE_X
BUILD_Y = PALCO_Y + AJUSTE_ALTURA
BUILD_Z = PALCO_Z + DISTANCIA_Z

# Inicializa o cliente do TikTok
client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

def processar_e_salvar_imagem(url_imagem):
    """Baixa a foto de perfil do espectador e salva no diretório do PixelPrinter"""
    try:
        resposta = requests.get(url_imagem, timeout=10)
        if resposta.status_code == 200:
            imagem = Image.open(io.BytesIO(resposta.content))
            # Garante que a imagem está salva no local correto que o plugin lê
            caminho_salvamento = os.path.join("plugins", "PixelPrinter", "images", "foto-live.png")
            os.makedirs(os.path.dirname(caminho_salvamento), exist_ok=True)
            imagem.save(caminho_salvamento)
            return True
    except Exception as e:
        print(f"❌ Erro ao processar imagem: {e}")
    return False

def executar_comandos_minecraft():
    """Conecta via RCON e gerencia os blocos e os atores no servidor"""
    try:
        with MCRcon(HOST_SERVIDOR, SENHA_RCON, port=25575) as mcr:
            mcr.command("gamerule sendCommandFeedback false")

            # Define a área de limpeza com margem de segurança
            if DIRECAO_FOTO in ["north", "south"]:
                x1, x2 = BUILD_X - 5, BUILD_X + TAMANHO_PAINEL + 5
                z1, z2 = BUILD_Z - 3, BUILD_Z + 3
            else:
                x1, x2 = BUILD_X - 3, BUILD_X + 3
                z1, z2 = BUILD_Z - 5, BUILD_Z + TAMANHO_PAINEL + 5
            y1, y2 = BUILD_Y - 2, BUILD_Y + TAMANHO_PAINEL + 2

            print("⚡ EFEITO: Raio de impacto e estilhaços no telão antigo!")
            mcr.command(f"summon lightning_bolt {PALCO_X} {PALCO_Y + 10} {PALCO_Z + 15}")
            
            # Animação cinematográfica de blocos quebrando
            mcr.command(f"fill {x1} {y1} {z1} {x2} {y2} {z2} air destroy")
            
            # Limpa os itens caídos para evitar lag na transmissão
            mcr.command("kill @e[type=item,distance=..150]")

            # Teleporta o Bot Construtor para a coordenada de início
            print(f"🕴️ Posicionando o {NOME_BOT}...")
            mcr.command(f"minecraft:tp {NOME_BOT} {BUILD_X} {BUILD_Y} {BUILD_Z} {DIRECAO_YAW} {DIRECAO_PITCH}")

            # O Bot inicia a construção da foto do usuário
            print(f"🖨️ {NOME_BOT} processando renderização da imagem...")
            mcr.command(f"sudo {NOME_BOT} pp create {DIRECAO_FOTO} foto-live.png {TAMANHO_PAINEL}")

            # EFEITOS DE VITÓRIA NO PALCO PRINCIPAL (Apresentador estático)
            print("🎉 Disparando efeitos visuais do show!")
            mcr.command(f"execute at {NOME_JOGADOR} run playsound entity.player.levelup player @a ~ ~ ~ 1 1")
            mcr.command(f"execute at {NOME_JOGADOR} run summon firework_rocket ~ ~2 ~ {{LifeTime:15,FireworksItem:{{id:firework_rocket,Count:1,tag:{{Fireworks:{{Explosions:[{{Type:1,Colors:[I;16711680,65280,255]}}]}}}}}}}}")
            mcr.command(f"effect give {NOME_JOGADOR} glowing 5 1 true")

    except Exception as e:
        print(f"❌ Erro de comunicação RCON com o Minecraft: {e}")

@client.on(LikeEvent)
async def on_like(event: LikeEvent):
    """Escuta os eventos de curtidas em tempo real na live do TikTok"""
    # Exemplo de lógica de meta: Dispara a automação a cada 500 likes acumulados do usuário
    if event.total_likes % 500 == 0:
        print(f"🔥 Meta atingida! {event.user.unique_id} enviou likes acumulados: {event.total_likes}")
        
        # Obtém a URL da foto de perfil de maior qualidade do espectador
        url_foto = event.user.avatar.urls[0]
        
        # Executa as tarefas pesadas de I/O em uma thread separada para não travar o loop assíncrono
        loop = asyncio.get_running_loop()
        sucesso = await loop.run_in_executor(None, processar_e_salvar_imagem, url_foto)
        
        if sucesso:
            # Envia os comandos de automação para o servidor de Minecraft
            await loop.run_in_executor(None, executar_comandos_minecraft)

if __name__ == "__main__":
    print("==================================================")
    print("🎮 INICIALIZANDO: MOTOR DE PRODUÇÃO TIKTOK REAL-TIME")
    print("==================================================")
    try:
        # Conecta na API do TikTok e inicia o monitoramento assíncrono da Live
        client.run()
    except KeyboardInterrupt:
        print("\n🛑 Processo encerrado pelo usuário.")
