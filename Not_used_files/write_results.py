import os

def get_directory_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 ** 3)  # Konvertiere Bytes in Gigabytes

def create_html_file(file_paths, output_file):
    total_size_gb = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>Luna Project Search</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; }\n')
        f.write('table { width: 100%; border-collapse: collapse; }\n')
        f.write('th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n')
        f.write('th { background-color: #f2f2f2; }\n')
        f.write('tr:nth-child(even) { background-color: #f9f9f9; }\n')
        f.write('button, input[type="checkbox"] { cursor: pointer; }\n')
        f.write('</style>\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Luna Project Search</h1>\n')
        f.write('<table>\n')
        f.write('<tr><th>Select</th><th>Projektname</th><th>Größe (GB)</th></tr>\n')
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            size = get_directory_size(file_path)
            total_size_gb += size
            f.write(f'<tr><td><input type="checkbox" name="project" value="{file_path}"></td><td>{file_name}</td><td>{size:.2f}</td></tr>\n')
        f.write('</table>\n')
        f.write(f'<button onclick="generateScript(\'move\')">Move Selection</button>\n')
        f.write(f'<button onclick="generateScript(\'delete\')">Delete Selection</button>\n')
        f.write(f'<h2>Gesamtgröße aller Projekte: {total_size_gb:.2f} GB</h2>\n')
        f.write('<script>\n')
        f.write('function generateScript(action) {\n')
        f.write('  var selected = Array.from(document.querySelectorAll("input[name=\'project\']:checked")).map(el => el.value);\n')
        f.write('  fetch(`/${action}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({projects: selected}) })\n')
        f.write('  .then(response => response.json()).then(data => alert(data.message)).catch(error => console.error("Error:", error));\n')
        f.write('}\n')
        f.write('</script>\n')
        f.write('</body>\n</html>')

def main():
    input_file = os.path.join(os.path.dirname(__file__), '../templates/treffer.txt')
    output_file = os.path.join(os.path.dirname(__file__), '../templates/treffer.html')
    
    with open(input_file, 'r', encoding='utf-8') as file:
        file_paths = file.read().splitlines()
    
    create_html_file(file_paths, output_file)
    print("HTML-Datei wurde erstellt und befindet sich hier: {}".format(output_file))

if __name__ == "__main__":
    main()
