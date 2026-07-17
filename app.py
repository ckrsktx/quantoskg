import gradio as gr
import pandas as pd
import socket

# Fabric definitions dictionary (Saved 100% locally and offline in python!)
FABRIC_PRESETS = {
    "Moletinho Fine Algodão (Aradefe)": {
        "width": 190.0,
        "yield_m_kg": 2.50,
        "margin": 10.0,
        "seam_allowance": 5.0,
        "ref": "105.05ft-pr1001",
        "link": "https://aradefe.com.br/loja/aradefe/produto/105.05ft-pr1001/moletinho-fine-algodao-preto",
        "ribana_pct": 15.0,
        "ribana_name": "Ribana 2X1 Moletinho Fine - Preto"
    },
    "Malhão Heavy Algodão (Aradefe)": {
        "width": 188.0,
        "yield_m_kg": 1.97,
        "margin": 10.0,
        "seam_allowance": 5.0,
        "ref": "110.62ft-pr1001",
        "link": "https://aradefe.com.br/loja/aradefe/produto/110.62ft-pr1001/malhao-heavy-algodao-preto",
        "ribana_pct": 5.0,
        "ribana_name": "Ribana Heavy 2x1 Algodão - Preto"
    },
    "Personalizado (Defina manualmente)": {
        "width": None,
        "yield_m_kg": None,
        "margin": None,
        "seam_allowance": None,
        "ref": "-",
        "link": ""
    }
}

# Default Standard Grade Values
GRADE_DEFAULTS = {
    'P':  {'qty': 3, 'h': 73, 'w': 52, 's': 23},
    'M':  {'qty': 4, 'h': 76, 'w': 56, 's': 24},
    'G':  {'qty': 4, 'h': 80, 'w': 59, 's': 26},
    'GG': {'qty': 3, 'h': 82, 'w': 63, 's': 27}
}

def get_connection_status_html():
    """
    Checks if the Hugging Face server has active internet access.
    Displays a clear B&W styled warning if offline, reassuring the user 
    that all fabric presets are saved locally and the calculator works 100% normally.
    """
    try:
        socket.setdefaulttimeout(1.0)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        # Online Status
        return """
        <div style="background-color: #ffffff; border: 1px solid #000000; padding: 6px 12px; border-radius: 4px; font-size: 11px; display: inline-flex; align-items: center; gap: 6px; font-family: sans-serif; color: #000000; float: right; margin-top: -15px; margin-bottom: 10px;">
            <span style="color: #00cc00; font-size: 14px; line-height: 1;">●</span> <b>CONECTADO</b> | Presets de fábrica ativos
        </div>
        <div style="clear: both;"></div>
        """
    except Exception:
        # Offline Status (Reassuring the user)
        return """
        <div style="background-color: #ffffff; border: 1px solid #000000; padding: 6px 12px; border-radius: 4px; font-size: 11px; display: inline-flex; align-items: center; gap: 6px; font-family: sans-serif; color: #000000; float: right; margin-top: -15px; margin-bottom: 10px;">
            <span style="color: #cc0000; font-size: 14px; line-height: 1;">●</span> <b>SERVIDOR OFFLINE</b> | Tecidos Padrões carregados localmente (O cálculo funciona normalmente!)
        </div>
        <div style="clear: both;"></div>
        """

def clear_quantities():
    # Set all quantities to 0
    return 0, 0, 0, 0

def calculate_fabric_logic(
    preset_name, custom_name,
    p_qty, p_h, p_w, p_s,
    m_qty, m_h, m_w, m_s,
    g_qty, g_h, g_w, g_s,
    gg_qty, gg_h, gg_w, gg_s,
    fabric_width, fabric_yield, seam_allowance, safety_margin
):
    # Validation for Personalizado empty inputs
    if fabric_width is None or fabric_yield is None or seam_allowance is None or safety_margin is None:
        return "<div style='color: #000000; font-weight: bold; border: 2px solid #000000; padding: 15px; background-color: #ffffff; text-align: center; font-size: 13px;'>Aguardando preenchimento das Propriedades Técnicas para calcular.</div>"
        
    if fabric_width <= 0 or fabric_yield <= 0:
        return "<div style='color: red; font-weight: bold; border: 2px solid #000000; padding: 15px; background-color: #fff0f0; text-align: center; font-size: 13px;'>Largura e Rendimento do tecido devem ser maiores que zero.</div>"

    # Get final fabric name
    final_fabric_name = preset_name
    if preset_name == "Personalizado (Defina manualmente)":
        final_fabric_name = custom_name.strip() if custom_name.strip() else "Tecido Personalizado"

    # Safe parsing of quantities and inputs
    p_qty = int(p_qty or 0)
    m_qty = int(m_qty or 0)
    g_qty = int(g_qty or 0)
    gg_qty = int(gg_qty or 0)

    raw_data = {
        'P':  {'qty': p_qty,  'h': p_h,  'w': p_w,  's': p_s},
        'M':  {'qty': m_qty,  'h': m_h,  'w': m_w,  's': m_s},
        'G':  {'qty': g_qty,  'h': g_h,  'w': g_w,  's': g_s},
        'GG': {'qty': gg_qty, 'h': gg_h, 'w': gg_w, 's': gg_s}
    }
    
    results = []
    total_meters = 0
    total_pieces = 0
    
    # Analyze each size
    for size, val in raw_data.items():
        qty = val['qty']
        if qty <= 0:
            continue
            
        # Validation for missing measurements of active sizes
        h, w, s = val['h'], val['w'], val['s']
        if h is None or w is None or s is None or h <= 0 or w <= 0 or s <= 0:
            return f"<div style='color: red; font-weight: bold; border: 2px solid #000000; padding: 15px; background-color: #fff0f0; text-align: center; font-size: 13px;'>Por favor, preencha as medidas de Altura, Largura e Manga para o tamanho {size}.</div>"
            
        alt_cortada = int(h + seam_allowance)
        larg_cortada = int(w + 2) # side seam margin
        manga_cortada = int(s + 4) # sleeve margin
        
        # Calculate width layout efficiency
        body_width_used = 2 * larg_cortada # Front + Back side-by-side
        sobra_lateral = int(fabric_width - body_width_used)
        
        consumo_unitario = alt_cortada / 100.0 # meters
        subtotal_m = qty * consumo_unitario
        total_meters += subtotal_m
        total_pieces += qty
        
        results.append({
            'Tamanho': size,
            'Quantidade': qty,
            'Altura de Corte': alt_cortada,
            'Largura de Corte': larg_cortada,
            'Manga': manga_cortada,
            'Sobra Lateral': sobra_lateral,
            'Consumo Unitário': round(consumo_unitario, 2),
            'Subtotal': round(subtotal_m, 2)
        })
        
    if total_pieces == 0:
        return "<div style='color: #000000; font-weight: bold; border: 2px solid #000000; padding: 15px; background-color: #ffffff; text-align: center; font-size: 13px;'>Adicione pelo menos 1 quantidade para algum tamanho para calcular o consumo.</div>"
        
    # Calculate weights
    net_kg = total_meters / fabric_yield
    safety_factor = 1 + (safety_margin / 100.0)
    safety_kg = net_kg * safety_factor
    
    # Check if we are calculating for ONLY 1 size
    active_sizes = [r['Tamanho'] for r in results]
    if len(active_sizes) == 1:
        recommended_title = f"COMPRAR TAMANHO {active_sizes[0]}"
        detail_msg = f"Consumo exclusivo para o tamanho {active_sizes[0]}"
    else:
        recommended_title = f"COMPRAR (COM {safety_margin}% MARGEM)"
        detail_msg = f"Grade total de {total_pieces} peças"
    
    # Get ribana specs based on active fabric preset
    preset_data = FABRIC_PRESETS.get(preset_name, FABRIC_PRESETS["Personalizado (Defina manualmente)"])
    ribana_name = preset_data["ribana_name"] if preset_data["ribana_name"] else "Ribana Gola (3 cm)"
    
    # Commercial recommendations from Aradefe store
    ribana_pct = preset_data["ribana_pct"]
    ribana_html = ""
    if ribana_pct is not None:
        ribana_commercial_kg = safety_kg * (ribana_pct / 100.0)
        ribana_html = f"""
        <div style="flex: 1; min-width: 140px; padding: 12px; border: 2px dashed #000000; background-color: #ffffff; border-radius: 4px; text-align: center;">
            <p style="margin: 0; font-size: 10px; text-transform: uppercase; color: #555555; font-weight: bold; letter-spacing: 0.5px;">⭐ COMPRA DE RIBANA SUGERIDA</p>
            <p style="margin: 4px 0 0 0; font-size: 26px; font-weight: bold; color: #000000; line-height: 1;">{ribana_commercial_kg:.3f} kg</p>
            <p style="margin: 4px 0 0 0; font-size: 11px; color: #444444;">{ribana_name} ({ribana_pct:.0f}%)</p>
        </div>
        """

    # Generate beautifully organized responsive HTML results box
    summary_html = f"""
<div class="result-card" style="border: 2px solid #000000; padding: 16px; background-color: #ffffff; border-radius: 4px; font-family: sans-serif; color: #000000;">
    <h2 style="margin-top: 0; color: #000000; border-bottom: 2px solid #000000; padding-bottom: 8px; font-weight: bold; text-transform: uppercase; font-size: 15px; letter-spacing: 0.5px; color: #000000;">
        ⚖️ COMPRA DE TECIDO RECOMENDADA
    </h2>
    
    <div style="display: flex; flex-wrap: wrap; margin-bottom: 16px; gap: 12px;">
        <div style="flex: 1; min-width: 140px; padding: 12px; border: 2px solid #000000; background-color: #ffffff; border-radius: 4px; text-align: center;">
            <p style="margin: 0; font-size: 10px; text-transform: uppercase; color: #555555; font-weight: bold; letter-spacing: 0.5px;">{recommended_title}</p>
            <p style="margin: 4px 0 0 0; font-size: 30px; font-weight: bold; color: #000000; line-height: 1;">{safety_kg:.3f} kg</p>
            <p style="margin: 4px 0 0 0; font-size: 11px; color: #444444;">{detail_msg}</p>
        </div>
        <div style="flex: 1; min-width: 140px; padding: 12px; border: 1px solid #000000; background-color: #f9f9f9; border-radius: 4px; text-align: center;">
            <p style="margin: 0; font-size: 10px; text-transform: uppercase; color: #666666; font-weight: bold; letter-spacing: 0.5px;">PESO LÍQUIDO (SEM PERDAS)</p>
            <p style="margin: 4px 0 0 0; font-size: 22px; font-weight: bold; color: #333333; line-height: 1;">{net_kg:.3f} kg</p>
            <p style="margin: 4px 0 0 0; font-size: 11px; color: #666666;">Total em metros: {total_meters:.2f} m</p>
        </div>
        {ribana_html}
    </div>
    
    <div style="border-top: 1px solid #000000; padding-top: 12px; font-size: 12px; line-height: 1.4; color: #000000;">
        <p style="margin: 2px 0;"><b>🧵 Tecido de Base:</b> {final_fabric_name}</p>
        {f"<p style='margin: 2px 0;'><b>📦 Parâmetros:</b> Ref. {FABRIC_PRESETS[preset_name]['ref']} | {fabric_yield:.2f} m/kg | Largura {fabric_width/100.0:.2f}m</p>" if preset_name != "Personalizado (Defina manualmente)" else f"<p style='margin: 2px 0;'><b>📦 Parâmetros Personalizados:</b> Rendimento {fabric_yield:.2f} m/kg | Largura {fabric_width/100.0:.2f}m</p>"}
    </div>
</div>

<br>

<h3 style="margin-top: 20px; font-weight: bold; text-transform: uppercase; color: #000000; border-bottom: 2px solid #000000; padding-bottom: 6px; font-size: 13px; letter-spacing: 0.5px; color: #000000;">
    📐 DETALHES TÉCNICOS DE CORTE
</h3>
<p style="font-size: 11px; color: #444444; margin-bottom: 12px; line-height: 1.3;">
    <i>*Encaixe Otimizado: Frente/Costas cortadas lado a lado. Mangas cortadas aproveitando a Sobra Lateral do tecido.</i>
</p>

<!-- DESKTOP VIEW: Beautiful Clean Table (hidden on mobile) -->
<div class="desktop-only-table">
<table style="width: 100%; border-collapse: collapse; color: #000000; text-align: center; font-size: 12px; font-family: sans-serif; border: 1px solid #000000; background-color: #ffffff;">
    <thead>
        <tr style="background-color: #f2f2f2; border-bottom: 2px solid #000000; color: #000000;">
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Tam.</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Qtd.</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Compr. Corte (cm)</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Larg. Corte (cm)</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Manga (cm)</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Sobra Lateral (cm)</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Cons. Unit. (m)</th>
            <th style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">Cons. Total Lote (m)</th>
        </tr>
    </thead>
    <tbody>
"""
    for r in results:
        summary_html += f"""
        <tr style="border-bottom: 1px solid #000000; color: #000000;">
            <td style="padding: 10px; border: 1px solid #000000; font-weight: bold; background-color: #f9f9f9; color: #000000;">{r['Tamanho']}</td>
            <td style="padding: 10px; border: 1px solid #000000; color: #000000;">{r['Quantidade']}</td>
            <td style="padding: 10px; border: 1px solid #000000; color: #000000;">{r['Altura de Corte']}</td>
            <td style="padding: 10px; border: 1px solid #000000; color: #000000;">{r['Largura de Corte']}</td>
            <td style="padding: 10px; border: 1px solid #000000; color: #000000;">{r['Manga']}</td>
            <td style="padding: 10px; border: 1px solid #000000; color: #000000;">{r['Sobra Lateral']} (OK)</td>
            <td style="padding: 10px; border: 1px solid #000000; font-weight: bold; color: #000000;">{r['Consumo Unitário']:.2f}</td>
            <td style="padding: 10px; border: 1px solid #000000; font-weight: bold; background-color: #f9f9f9; color: #000000;">{r['Subtotal']:.2f}</td>
        </tr>
"""
    summary_html += """
    </tbody>
</table>
</div>

<!-- MOBILE VIEW: Structured list cards (hidden on desktop) -->
<div class="mobile-only-cards" style="display: none;">
"""
    for r in results:
        summary_html += f"""
    <div style="border: 1px solid #000000; padding: 12px; margin-bottom: 10px; background-color: #ffffff; border-radius: 4px; font-family: sans-serif; font-size: 11px;">
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid #000000; padding-bottom: 4px; margin-bottom: 6px;">
            <span style="font-size: 13px; font-weight: bold; color: #000000;">TAMANHO {r['Tamanho']}</span>
            <span style="font-size: 12px; font-weight: bold; color: #111111;">Quantidade: {r['Quantidade']} peças</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">
            <p style="margin: 0; color: #000000;"><b>Alt. Corte:</b> {r['Altura de Corte']} cm</p>
            <p style="margin: 0; color: #000000;"><b>Larg. Corte:</b> {r['Largura de Corte']} cm</p>
            <p style="margin: 0; color: #000000;"><b>Manga:</b> {r['Manga']} cm</p>
            <p style="margin: 0; color: #000000;"><b>Sobra Lateral:</b> {r['Sobra Lateral']} cm (OK)</p>
            <p style="margin: 0; grid-column: span 2; border-top: 1px dashed #cccccc; padding-top: 4px; margin-top: 2px; color: #000000;">
                <b>Consumo Unitário:</b> {r['Consumo Unitário']:.2f} m | <b>Subtotal do Lote:</b> <b>{r['Subtotal']:.2f} m</b>
            </p>
        </div>
    </div>
"""
    summary_html += """
</div>
"""
    return summary_html

def load_fabric_preset_and_reset_grade(preset_name):
    """
    Triggers automatically when preset changes. 
    It resets quantities and measurements back to default standard,
    loads the new fabric properties, and INSTANTLY recalculates the results
    so the recommended purchase box is updated without displaying old data.
    """
    # Grade Defaults
    p_qty, p_h, p_w, p_s = 3, 73, 52, 23
    m_qty, m_h, m_w, m_s = 4, 76, 56, 24
    g_qty, g_h, g_w, g_s = 4, 80, 59, 26
    gg_qty, gg_h, gg_w, gg_s = 3, 82, 63, 27
    
    if preset_name == "Personalizado (Defina manualmente)":
        prompt_html = "<div style='border: 1px solid #000000; padding: 15px; text-align: center; font-weight: bold; background-color: #ffffff; color: #000000;'>Por favor, preencha as Propriedades Técnicas e clique em Calcular.</div>"
        return (
            gr.update(value=None, interactive=True),  # fabric_width
            gr.update(value=None, interactive=True),  # fabric_yield
            gr.update(value=None, interactive=True),  # seam_allowance
            gr.update(value=None, interactive=True),  # safety_margin
            gr.update(value="", visible=True, interactive=True), # custom_name_input
            p_qty, p_h, p_w, p_s,
            m_qty, m_h, m_w, m_s,
            g_qty, g_h, g_w, g_s,
            gg_qty, gg_h, gg_w, gg_s,
            prompt_html # Clear calculation card
        )
    else:
        preset = FABRIC_PRESETS[preset_name]
        
        # Instantly run calculation for standard grade on selected fabric!
        initial_html = calculate_fabric_logic(
            preset_name, preset_name,
            p_qty, p_h, p_w, p_s,
            m_qty, m_h, m_w, m_s,
            g_qty, g_h, g_w, g_s,
            gg_qty, gg_h, gg_w, gg_s,
            preset["width"], preset["yield_m_kg"], preset["seam_allowance"], preset["margin"]
        )
        
        return (
            gr.update(value=preset["width"], interactive=False),
            gr.update(value=preset["yield_m_kg"], interactive=False),
            gr.update(value=preset["seam_allowance"], interactive=False),
            gr.update(value=preset["margin"], interactive=False),
            gr.update(value=preset_name, visible=False), # custom_name_input
            p_qty, p_h, p_w, p_s,
            m_qty, m_h, m_w, m_s,
            g_qty, g_h, g_w, g_s,
            gg_qty, gg_h, gg_w, gg_s,
            initial_html # Update output instantly!
        )

# Custom CSS targeting Gradio theme tokens directly with robust responsive styling
custom_css = """
:root, .dark {
    /* Pure white background for everything */
    --body-background-fill: #ffffff !important;
    --background-fill-primary: #ffffff !important;
    --background-fill-secondary: #ffffff !important;
    --block-background-fill: #ffffff !important;
    --container-background-fill: #ffffff !important;
    
    /* Strong solid borders */
    --border-color-primary: #000000 !important;
    --border-color-secondary: #000000 !important;
    --block-border-color: #000000 !important;
    --block-border-width: 1px !important;
    
    /* Black text colors */
    --body-text-color: #000000 !important;
    --body-text-color-subdued: #000000 !important;
    --block-title-text-color: #000000 !important;
    --block-label-text-color: #000000 !important;
    --block-info-text-color: #000000 !important;
    --input-placeholder-color: #666666 !important;
    
    /* Input element styling - white background, black text and borders */
    --input-background-fill: #ffffff !important;
    --input-background-fill-focus: #ffffff !important;
    --input-border-color: #000000 !important;
    --input-border-color-focus: #000000 !important;
    --input-text-color: #000000 !important;
    
    /* Primary buttons (black background, white text) */
    --button-primary-background-fill: #000000 !important;
    --button-primary-background-fill-hover: #222222 !important;
    --button-primary-text-color: #ffffff !important;
    --button-primary-border-color: #000000 !important;
    
    /* Secondary buttons */
    --button-secondary-background-fill: #ffffff !important;
    --button-secondary-background-fill-hover: #f0f0f0 !important;
    --button-secondary-text-color: #000000 !important;
    --button-secondary-border-color: #000000 !important;
}

/* General component overrides */
body, html, .gradio-container, .gr-box, .gr-form, .gr-padded, .gr-column, .gr-row, .gr-block {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #000000 !important;
}

/* Force headings and paragraphs to black */
h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #000000 !important;
}

/* Text boxes, dropdowns, and number inputs */
input, select, textarea, .gr-input, .gr-text-input, .secondary {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
    border-radius: 4px !important;
}

/* Force no wrapping of text in tables */
th, td {
    white-space: nowrap !important;
    text-overflow: clip !important;
}

/* Custom style to make Radio buttons look modern and high contrast */
fieldset label, label[class*="radio"], .gr-radio-label {
    background-color: #ffffff !important;
    background: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
    border-radius: 4px !important;
    padding: 10px 14px !important;
    margin-bottom: 8px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    cursor: pointer;
}

fieldset label span, label[class*="radio"] span, .gr-radio-label span {
    color: #000000 !important;
    font-weight: bold !important;
}

fieldset label.selected, label[class*="radio"].selected {
    background-color: #000000 !important;
    background: #000000 !important;
    color: #ffffff !important;
}

fieldset label.selected span, label[class*="radio"].selected span {
    color: #ffffff !important;
}

/* Clear button specific styling */
.clear-btn {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 2px dashed #000000 !important;
    font-weight: bold !important;
    margin-bottom: 15px !important;
}
.clear-btn:hover {
    background-color: #f2f2f2 !important;
}

/* RESPONSIVE MEDIA QUERIES FOR MOBILE DEVICES */
@media (max-width: 600px) {
    .desktop-only-table {
        display: none !important;
    }
    .mobile-only-cards {
        display: block !important;
    }
    
    h1 { font-size: 18px !important; }
    h2 { font-size: 14px !important; }
    h3 { font-size: 12px !important; }
    p, label, span, input, select { font-size: 11px !important; }
    
    .gr-padded, .gr-block {
        padding: 8px !important;
    }
    
    .result-card {
        padding: 10px !important;
    }
}
"""

with gr.Blocks(css=custom_css, title="QUANTOS KG?") as demo:
    gr.Markdown("# 🧮 QUANTOS KG?")
    
    # Render the offline/online status bar dynamically inside the UI!
    gr.HTML(value=get_connection_status_html())
    
    gr.Markdown("Selecione o tecido e defina as propriedades para calcular exatamente o consumo em quilogramas (kg) necessários para a sua produção.")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📦 Seleção do Tecido")
            preset_select = gr.Radio(
                label="Escolha uma opção de Tecido",
                choices=list(FABRIC_PRESETS.keys()),
                value="Moletinho Fine Algodão (Aradefe)"
            )
            
            # Custom Fabric Name: Only visible and editable when "Personalizado" is chosen
            custom_name_input = gr.Textbox(
                label="Nome do Tecido Personalizado",
                value="Moletinho Fine Algodão (Aradefe)",
                placeholder="Ex: Meia Malha Penteada 30.1",
                visible=False,
                interactive=True
            )
            
            gr.Markdown("### 📏 Propriedades Técnicas")
            fabric_width = gr.Number(label="Largura Aberta (cm)", value=190.0, precision=1, interactive=False)
            fabric_yield = gr.Number(label="Rendimento (m/kg)", value=2.50, precision=2, interactive=False)
            seam_allowance = gr.Number(label="Margem de Costura / Bainha (cm)", value=5.0, precision=1, interactive=False)
            safety_margin = gr.Number(label="Margem de Segurança / Encolhimento (%)", value=10.0, precision=1, interactive=False)
            
        with gr.Column(scale=2):
            gr.Markdown("### 👕 Tabela de Medidas (Camiseta Oversized)")
            
            # CLEAR GRID BUTTON: Placed below the subtitle and right before the grid quantities!
            clear_grid_btn = gr.Button("🗑️ Limpar Grade Padrão", elem_classes="clear-btn")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Tamanho P")
                    p_qty = gr.Number(label="Quantidade", value=3, precision=0, interactive=True)
                    p_h = gr.Number(label="Altura (cm)", value=73, precision=0, interactive=True)
                    p_w = gr.Number(label="Largura (cm)", value=52, precision=0, interactive=True)
                    p_s = gr.Number(label="Manga (cm)", value=23, precision=0, interactive=True)
                
                with gr.Column():
                    gr.Markdown("#### Tamanho M")
                    m_qty = gr.Number(label="Quantidade", value=4, precision=0, interactive=True)
                    m_h = gr.Number(label="Altura (cm)", value=76, precision=0, interactive=True)
                    m_w = gr.Number(label="Largura (cm)", value=56, precision=0, interactive=True)
                    m_s = gr.Number(label="Manga (cm)", value=24, precision=0, interactive=True)
                    
            with gr.Row():
                with gr.Column():
                    gr.Markdown("#### Tamanho G")
                    g_qty = gr.Number(label="Quantidade", value=4, precision=0, interactive=True)
                    g_h = gr.Number(label="Altura (cm)", value=80, precision=0, interactive=True)
                    g_w = gr.Number(label="Largura (cm)", value=59, precision=0, interactive=True)
                    g_s = gr.Number(label="Manga (cm)", value=26, precision=0, interactive=True)
                
                with gr.Column():
                    gr.Markdown("#### Tamanho GG")
                    gg_qty = gr.Number(label="Quantidade", value=3, precision=0, interactive=True)
                    gg_h = gr.Number(label="Altura (cm)", value=82, precision=0, interactive=True)
                    gg_w = gr.Number(label="Largura (cm)", value=63, precision=0, interactive=True)
                    gg_s = gr.Number(label="Manga (cm)", value=27, precision=0, interactive=True)

    btn = gr.Button("Calcular Tecido", variant="primary")
    
    with gr.Row():
        output_html = gr.HTML(label="Resultado do Cálculo")

    # All event triggers MUST be inside the gr.Blocks() context!
    # Interactive preset loading & keyboard activation behavior
    preset_select.change(
        load_fabric_preset_and_reset_grade,
        inputs=[preset_select],
        outputs=[
            fabric_width, fabric_yield, seam_allowance, safety_margin, custom_name_input,
            p_qty, p_h, p_w, p_s,
            m_qty, m_h, m_w, m_s,
            g_qty, g_h, g_w, g_s,
            gg_qty, gg_h, gg_w, gg_s,
            output_html # Instantly recalculates outputs!
        ]
    )
    
    # Click behavior for clearing quantities in the grid
    clear_grid_btn.click(
        clear_quantities,
        inputs=[],
        outputs=[p_qty, m_qty, g_qty, gg_qty]
    )
    
    btn.click(
        calculate_fabric_logic,
        inputs=[
            preset_select, custom_name_input,
            p_qty, p_h, p_w, p_s,
            m_qty, m_h, m_w, m_s,
            g_qty, g_h, g_w, g_s,
            gg_qty, gg_h, gg_w, gg_s,
            fabric_width, fabric_yield, seam_allowance, safety_margin
        ],
        outputs=[output_html]
    )

    # Run a quick startup calculation on load so the screen launches with the correct preset data!
    demo.load(
        calculate_fabric_logic,
        inputs=[
            preset_select, custom_name_input,
            p_qty, p_h, p_w, p_s,
            m_qty, m_h, m_w, m_s,
            g_qty, g_h, g_w, g_s,
            gg_qty, gg_h, gg_w, gg_s,
            fabric_width, fabric_yield, seam_allowance, safety_margin
        ],
        outputs=[output_html]
    )

if __name__ == "__main__":
    demo.launch()
