# 🎮 Minecraft TikTok Live Automation

Sistema de automação em Python que integra eventos de uma Live do TikTok com um servidor local de Minecraft em tempo real.
Quando uma meta de Likes é atingida, o sistema captura a interação do espectador, obtém sua foto de perfil, processa a imagem automaticamente e a recria dentro do Minecraft utilizando PixelPrinter e comandos RCON.

---

## 🚀 Tecnologias Utilizadas
* **Python**
* **AsyncIO**
* **Requests**
* **Pillow (PIL)**
* **TikTokLive API**
* **MCRcon**
* **Minecraft Java Edition**
* **PixelPrinter**
* **Desenvolvimento Assistido por IA (LLMs)**

---

## 🧩 Desafio do Projeto
O objetivo era criar uma experiência interativa em que espectadores da Live pudessem influenciar diretamente o cenário do Minecraft através de suas interações no TikTok.
O principal desafio foi integrar sistemas que originalmente não foram projetados para trabalhar juntos:

* Eventos em tempo real do TikTok
* Download dinâmico de imagens de perfil
* Processamento de imagens
* Comunicação com o servidor Minecraft via RCON
* Geração automática de estruturas dentro do jogo

---

## 🧠 Evolução da Solução

### Versão 1 — Algoritmo Matemático
A primeira implementação utilizava cálculos trigonométricos (seno e cosseno) para determinar dinamicamente a posição de construção da imagem com base na orientação do jogador.

**Problemas Encontrados:**
* Flickering causado pelos teletransportes constantes.
* Dependência da posição física do jogador.
* Limitações do plugin PixelPrinter para execução remota de comandos.
* Experiência visual inconsistente durante transmissões ao vivo.

### Versão 2 — Arquitetura de Produção
Após identificar os gargalos da primeira abordagem, o sistema foi redesenhado utilizando uma arquitetura baseada em separação de responsabilidades.
Foi introduzido um personagem auxiliar (**"Bot Construtor"**), responsável exclusivamente pelas tarefas de construção.

**Benefícios:**
* O apresentador permanece estático no palco.
* Eliminação do flickering visual.
* Construção das imagens sem interferir na câmera principal da Live.
* Código mais simples de manter e expandir.
* Experiência visual mais profissional para o público.

---

## 📚 Conhecimentos Aplicados
* Programação assíncrona com AsyncIO
* Consumo de APIs em tempo real
* Processamento de imagens
* Automação de servidores Minecraft
* Arquitetura de sistemas
* Resolução de problemas e depuração
* Integração entre múltiplas tecnologias

---

## 📌 Observação
Este projeto foi idealizado, desenvolvido, testado e refinado por mim, com suporte de ferramentas de IA para acelerar prototipação, pesquisa e validação de soluções. Todas as decisões arquiteturais, testes de integração e adaptações necessárias para contornar limitações do Minecraft, PixelPrinter e TikTokLive foram realizadas durante o desenvolvimento do projeto.
