🎮 Minecraft TikTok Live Automation
Um sistema automatizado em Python que conecta a API de Lives do TikTok com um servidor local de Minecraft. Quando uma meta de Likes é atingida, o sistema baixa a foto de perfil do usuário e a constrói em tempo real dentro do jogo usando comandos RCON.

🛠️ Tecnologias Utilizadas
Python (Asyncio, Requests, Pillow para processamento de imagem)

TikTokLive API (Websockets para escutar os eventos da live)

MCRcon (Comunicação direta com o console do servidor de Minecraft)

Engenharia de Prompt / IA (Desenvolvimento assistido por inteligência artificial)

🧠 A Evolução do Projeto (Problem Solving)
Versão 1: A Abordagem Algorítmica (v1_math_algorithm)
Inicialmente, criei um sistema baseado em trigonometria (Seno e Cosseno) que calculava dinamicamente onde o jogador estava olhando e teleportava o avatar para construir a imagem.

O Problema: Na prática, limitações de plugins do Minecraft (como o PixelPrinter) e o teleporte constante geravam flicker (piscar de tela), estragando a experiência visual da Live.

Versão 2: A Abordagem Arquitetural (v2_production_architecture)
Para resolver a experiência do usuário, mudei a arquitetura do sistema. Abandonei a matemática complexa de cálculo de eixo e introduzi um sistema de "Dublê" (Dummy Bot).

A Solução: O código em Python agora gerencia dois atores no servidor. A conta principal fica livre para interagir com o público e realizar danças (Emotecraft), enquanto a automação assume o controle de um "Bot Construtor" escondido no mapa para processar e gerar a imagem de fundo. Resultado: 100% de estabilidade e estética visual cinematográfica.



Nota: A lógica central e a estrutura deste projeto foram idealizadas e arquitetadas por mim, com a codificação escrita em colaboração com ferramentas de IA (LLMs). Atuei como Tech Lead do projeto, realizando os testes de integração, refatoração e adaptação do código para contornar as limitações da engine do Minecraft e dos plugins de servidor.