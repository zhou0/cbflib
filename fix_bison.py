import sys

with open('CMakeLists.txt', 'r') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'if(WIN32)' in line and 'find_package(BISON 2.7)' in lines[i+1]:
        start_idx = i
    if 'endif()' in line and i > start_idx and start_idx != -1:
        # Check if this is the end of the if(WIN32) block
        if 'else()' in lines[i+1] and 'find_package(BISON 2.7)' in lines[i+2]:
             end_idx = i + 4 # include endif()
             break

if start_idx != -1 and end_idx != -1:
    print(f"Found Bison block at {start_idx} to {end_idx}")
    new_content = lines[:start_idx]
    new_content.append("if(NOT BISON_FOUND)\n")
    # Indent the original block
    for line in lines[start_idx:end_idx]:
        new_content.append("  " + line)
    new_content.append("endif()\n")
    new_content.extend(lines[end_idx:])

    with open('CMakeLists.txt', 'w') as f:
        f.writelines(new_content)
    print("Successfully wrapped Bison block")
else:
    print(f"Failed to find Bison block: start_idx={start_idx}, end_idx={end_idx}")
