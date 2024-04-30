import svgwrite

def create_function_block_diagram(filename, block_name, connection_points):
    # Basic configurations
    font_size = 14
    block_width = 200
    padding = 40
    circle_radius = 5
    block_stroke_width = 4
    text_offset = 30
    block_height = max(len(connection_points) * 40, 100)
    
    # Calculate the SVG canvas size
    dwg = svgwrite.Drawing(filename, size=(block_width + 3 * padding + font_size + 10, block_height + 2 * padding + 10))
    
    # Draw the block
    block = dwg.rect(insert=(padding * 1.5 + font_size, padding), size=(block_width, block_height),
                     stroke='black', fill='white', stroke_width=block_stroke_width)
    dwg.add(block)
    
    # Add connection points and their names on the left and right sides
    spacing = block_height / (len(connection_points) + 1)
    for i, point in enumerate(connection_points):
        y_pos = (i + 1) * spacing + padding
        
        # Left side connection points and names
        # Inside circle
        dwg.add(dwg.circle(center=(padding * 1.5 + font_size, y_pos), r=3, fill='white', stroke='black'))
        # Outside circle
        dwg.add(dwg.circle(center=(padding * 1.5 + font_size - circle_radius - block_stroke_width, y_pos), r=circle_radius, fill='none', stroke='black'))
        # Connection point names
        dwg.add(dwg.text(point, insert=(padding * 1.5 + font_size + text_offset - 2*circle_radius, y_pos + font_size/3), text_anchor="end", font_size=font_size))
        
        # Right side connection points and names (mirrored)
        # Inside circle
        dwg.add(dwg.circle(center=(padding * 1.5 + font_size + block_width, y_pos), r=3, fill='white', stroke='black'))
        # Outside circle
        dwg.add(dwg.circle(center=(padding * 1.5 + font_size + block_width + circle_radius + block_stroke_width, y_pos), r=circle_radius, fill='none', stroke='black'))
        # Connection point names
        dwg.add(dwg.text(point, insert=(padding * 1.5 + font_size + block_width - text_offset + 2*circle_radius, y_pos + font_size/3), text_anchor="start", font_size=font_size))
    
    # Block name
    dwg.add(dwg.text(block_name, insert=((block_width + 3 * padding + font_size) / 2, block_height + padding * 1.5 + 10), text_anchor="middle", font_size=font_size))
    
    dwg.save()

# Example usage
create_function_block_diagram('function_block_diagram_corrected.svg', 'MyBlock', ['P1', 'P2', 'P3', 'P4'])
