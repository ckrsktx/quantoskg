p_qty, p_h, p_w, p_s = 10, None, 52, 23

# Check validation
qty = int(p_qty or 0)
if qty > 0:
 h = p_h
 w = p_w
 s = p_s
 if h is None or w is None or s is None or h <= 0 or w <= 0 or s <= 0:
     print("Validation error: Measurements cannot be empty for active sizes!")
 else:
     print("All OK!")
