# Quantities
quantities = {
 'P': 3,
 'M': 4,
 'G': 4,
 'GG': 3
}

# Rendimento do Moletinho Fine Algodão Aradefe: 2.50 m/kg
rendimento = 2.50 # m/kg

# 1. Scenario A: Hoodies (Casacos com Capuz)
# Standard consumption in meters per size (estimating for 1.90m open width)
consumption_hoodie = {
 'P': 1.30,
 'M': 1.40,
 'G': 1.50,
 'GG': 1.70
}

# 2. Scenario B: Sweatpants (Calças de moletom)
consumption_pants = {
 'P': 1.10,
 'M': 1.15,
 'G': 1.20,
 'GG': 1.30
}

# 3. Scenario C: Complete Tracksuits (Conjuntos Hoodie + Calça)
consumption_tracksuit = {
 'P': 2.40,
 'M': 2.55,
 'G': 2.70,
 'GG': 3.00
}

# 4. Scenario D: Simple T-Shirts / Blusas simples de moletinho fine
consumption_tshirt = {
 'P': 0.80,
 'M': 0.90,
 'G': 1.00,
 'GG': 1.10
}

def calculate_totals(consumption_dict, name):
 total_meters = 0
 print(f"\n--- {name} ---")
 print(f"{'Tamanho':<10} | {'Quantidade':<10} | {'Consumo/Peça (m)':<20} | {'Subtotal (m)':<15}")
 print("-" * 65)
 for size, qty in quantities.items():
     cons = consumption_dict[size]
     sub = qty * cons
     total_meters += sub
     print(f"{size:<10} | {qty:<10} | {cons:<20.2f} | {sub:<15.2f}")

 total_kg = total_meters / rendimento
 total_kg_safety = total_kg * 1.10 # 10% safety margin for shrinkage and cutting waste
 print("-" * 65)
 print(f"Total em metros: {total_meters:.2f} m")
 print(f"Total em kg (sem margem): {total_kg:.3f} kg")
 print(f"Total em kg (com margem de 10% para encolhimento e corte): {total_kg_safety:.3f} kg")
 return total_meters, total_kg, total_kg_safety

calculate_totals(consumption_hoodie, "Casaco com Capuz (Hoodie)")
calculate_totals(consumption_pants, "Calça Jogger / Cargo")
calculate_totals(consumption_tracksuit, "Conjunto Completo (Casaco + Calça)")
calculate_totals(consumption_tshirt, "Blusa Simples / Camiseta de Manga Longa")
