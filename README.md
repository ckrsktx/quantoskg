---
title: QUANTOS KG?
emoji: 🧮
colorFrom: gray
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: mit
---

# QUANTOS KG?

Este é um agente interativo e inteligente de cálculo de consumo de tecidos para confecção de roupas, ideal para marcas de streetwear, produtores independentes e modelistas.

## 🗂️ Recursos do Aplicativo:
1. **🧮 Calculadora de Consumo:** Permite preencher as medidas e quantidades (P, M, G, GG) e calcula exatamente o consumo de rolo em metros e quilogramas (kg) com margens e folgas de segurança automáticas.
2. **🧹 Limpar Grade:** Botão rápido para zerar as quantidades e começar novos cálculos imediatamente.
3. **🧵 presets Integrados:** Moletinho Fine e Malhão Heavy pré-programados com rendimento, largura e margem de fábrica.

## 🎨 Design do Aplicativo
Conforme especificações, o aplicativo possui uma interface limpa, moderna e minimalista:
* **Fundo da Página:** Branco Puro (`#ffffff`)
* **Fontes e Textos:** Preto Puro (`#000000`)
* **Elementos Visuais e Botões:** Design minimalista de alto contraste (Black & White style) 100% responsivo para celulares e desktops.

## 🚀 Como usar e fazer Deploy no Hugging Face Spaces:
1. Crie um novo **Space** no Hugging Face.
2. Selecione **Gradio** como SDK de desenvolvimento.
3. Suba estes 3 arquivos do diretório:
   * `app.py` (código da aplicação com a calculadora reativa e o robô crawler de estoque)
   * `requirements.txt` (bibliotecas necessárias)
   * `README.md` (metadados e instruções do Space)
4. O Hugging Face fará o deploy automático e iniciará o seu aplicativo **QUANTOS KG?**!
