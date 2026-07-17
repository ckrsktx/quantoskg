# Ficha tecnica
rendimento = 2.50 # m/kg
largura_total = 190 # cm (95 cm tubular aberta)

# Quantities
quantities = {
 'P': 3,
 'M': 4,
 'G': 4,
 'GG': 3
}

# Tabela do usuario
tabela = {
 'P': {'altura': 73, 'largura': 52, 'manga': 23},
 'M': {'altura': 76, 'largura': 56, 'manga': 24},
 'G': {'altura': 80, 'largura': 59, 'manga': 26},
 'GG': {'altura': 82, 'largura': 63, 'manga': 27}
}

# Margens padrão de costura e acabamento
# Para t-shirt de moletinho:
# Margem na altura (ombro + bainha): +5 cm
# Margem na largura (costuras laterais): +2 cm (1cm de cada lado)
# Margem na manga (bainha + cava): +4 cm

print("CÁLCULO DE CONSUMO INDIVIDUAL POR TAMANHO (Otimizado para largura aberta de 190 cm):")
print("-" * 80)
print(f"{'Tamanho':<8} | {'Altura Cortada':<15} | {'Largura Cortada':<15} | {'Manga Cortada':<15} | {'Consumo Linear (m)':<20}")
print("-" * 80)

consumos = {}
for sz, val in tabela.items():
 alt_cortada = val['altura'] + 5
 larg_cortada = val['largura'] + 2
 manga_cortada = val['manga'] + 4

 # Como demonstrado, Frente + Costas (2x larg_cortada) + Mangas cabem na largura de 190 cm
 # Logo, o consumo linear por peça é determinado pela Altura Cortada do corpo
 consumo_linear = alt_cortada / 100.0 # em metros
 consumos[sz] = consumo_linear
 print(f"{sz:<8} | {alt_cortada:<3} cm (body) | {larg_cortada:<3} cm (half) | {manga_cortada:<3} cm (len) | {consumo_linear:<20.2f}")

print("\nCÁLCULO TOTAL DA PRODUÇÃO:")
print("-" * 80)
print(f"{'Tamanho':<8} | {'Quantidade':<10} | {'Consumo/Peça (m)':<20} | {'Subtotal (m)':<15}")
print("-" * 80)

total_meters = 0
for sz, qty in quantities.items():
 cons = consumos[sz]
 sub = qty * cons
 total_meters += sub
 print(f"{sz:<8} | {qty:<10} | {cons:<20.2f} | {sub:<15.2f}")

print("-" * 80)
print(f"Total de tecido em Metros: {total_meters:.2f} m")

total_kg = total_meters / rendimento
print(f"Total em Kilogramas (líquido): {total_kg:.3f} kg")

# Adicionando margens de segurança para encolhimento e retalhos
# 10% é o padrão seguro na indústria para malhas 100% algodão
total_kg_safety_10 = total_kg * 1.10
print(f"Total em Kilogramas com 10% de margem (corte/encolhimento): {total_kg_safety_10:.3f} kg")
