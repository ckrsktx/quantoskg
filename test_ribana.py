# Quantities
quantities = {'P': 3, 'M': 4, 'G': 4, 'GG': 3}

# Ribana specs
strip_height = 7.0 / 100.0 # meters (7 cm)
lengths = {'P': 0.42, 'M': 0.44, 'G': 0.46, 'GG': 0.48} # meters

# Moletinho Ribana (2X1) - 280 g/m²
moletinho_rib_g = 0.280 # kg/m²
total_mo_area = 0
for sz, qty in quantities.items():
 area = strip_height * lengths[sz] * qty
 total_mo_area += area
mo_rib_net = total_mo_area * moletinho_rib_g
print(f"Moletinho Ribana Net: {mo_rib_net:.3f} kg")

# Malhao Ribana (Heavy) - 320 g/m²
malhao_rib_g = 0.320 # kg/m²
total_ma_area = 0
for sz, qty in quantities.items():
 area = strip_height * lengths[sz] * qty
 total_ma_area += area
ma_rib_net = total_ma_area * malhao_rib_g
print(f"Malhao Ribana Net: {ma_rib_net:.3f} kg")
