# Génère des icônes PNG simples pour la PWA
import struct, zlib

def make_png(size, bg=(26,26,46), fg=(255,255,255)):
    def pack32(n): return struct.pack('>I', n)
    def chunk(name, data):
        c = zlib.crc32(name + data) & 0xffffffff
        return pack32(len(data)) + name + data + pack32(c)
    
    # Image data
    rows = []
    for y in range(size):
        row = [0]  # filter byte
        for x in range(size):
            # Draw radar icon
            cx, cy = size//2, size//2
            dx, dy = x-cx, y-cy
            dist = (dx*dx + dy*dy) ** 0.5
            r_outer = size*0.42
            r_inner = size*0.28
            r_dot = size*0.08
            
            # Outer ring
            if abs(dist - r_outer) < size*0.035:
                row += list(fg)
            # Inner ring  
            elif abs(dist - r_inner) < size*0.03:
                row += list(fg)
            # Center dot
            elif dist < r_dot:
                row += list(fg)
            # Radar sweep line (top-right quadrant)
            elif dx >= 0 and dy <= 0 and abs(dy) < dx * 0.15 and dist < r_outer:
                row += [min(255,fg[0]), min(255,fg[1]//2), min(255,fg[2]//3)]
            else:
                row += list(bg)
        rows.append(bytes(row))
    
    compressed = zlib.compress(b''.join(rows))
    
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', pack32(size) + pack32(size) + bytes([8,2,0,0,0]))
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

for size in [192, 512]:
    with open(f'icon-{size}.png', 'wb') as f:
        f.write(make_png(size))
    print(f'icon-{size}.png OK')
