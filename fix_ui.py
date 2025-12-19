import os

def remove_lines(filepath, search_strings):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_count = 0
    
    for line in lines:
        if skip_count > 0:
            skip_count -= 1
            continue
            
        should_remove = False
        for search, lines_to_skip in search_strings:
            if search in line:
                should_remove = True
                skip_count = lines_to_skip
                break
        
        if not should_remove:
            new_lines.append(line)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# Fix sales.html
# Remove print button (4 lines)
remove_lines(r'd:\_templates\app\AppPoS\templates\sales.html', [
    ('onclick="printReceipt()"', 3) 
])

# Fix inventory.html
# Remove Margin header (1 line)
# Remove Margin data cell (1 line)
# Remove Margin preview block (6 lines approx)
remove_lines(r'd:\_templates\app\AppPoS\templates\inventory.html', [
    ('>Margen</th>', 0),
    ('${margin.toFixed(1)}%', 0),
    ('id="marginPreview"', 4) # This is inside a div, we need to be careful.
])

# For the margin preview, it's a block. Let's do a more specific removal for that.
with open(r'd:\_templates\app\AppPoS\templates\inventory.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the specific block for margin preview
# It looks like:
#                     <div class="pt-2 border-t border-gray-200 mt-2">
#                         <div class="flex justify-between items-center text-sm">
#                             <span class="text-gray-500">Margen:</span>
#                             <span id="marginPreview" class="font-bold text-gray-700">0%</span>
#                         </div>
#                     </div>
# We can try to replace this block.
start_marker = '<div class="pt-2 border-t border-gray-200 mt-2">'
end_marker = '</div>'
# This is risky with simple replace if markers are not unique.
# But that class string seems unique enough for this file.

if start_marker in content:
    # Find start
    start_idx = content.find(start_marker)
    # Find the closing div for this block. It's nested.
    # Let's just remove the lines containing these strings using the previous method but being careful.
    pass

# Refined inventory removal
# The previous remove_lines call might have left empty divs or broken structure if I'm not careful.
# Let's check the file content after the first pass.
