import os

def get_directory_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 ** 3)  # Konvertiere Bytes in Gigabytes

def create_html_file(file_paths, output_file):
    total_size_gb = 0  # Variable zur Speicherung der Gesamtgröße
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>Luna Project Search</title>\n')
        f.write('<style>\n')
        f.write('body { font-family: Arial, sans-serif; }\n')
        f.write('table { width: 100%; border-collapse: collapse; }\n')
        f.write('th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }\n')
        f.write('th { background-color: #f2f2f2; }\n')
        f.write('tr:nth-child(even) { background-color: #f9f9f9; }\n')
        f.write('button { padding: 5px 10px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }\n')
        f.write('</style>\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Luna Project Search</h1>\n')
        f.write('<table>\n')
        f.write('<tr><th>Projektname</th><th>Größe (GB)</th><th>Aktion</th><th>Finder</th></tr>\n')
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            size = get_directory_size(file_path)
            total_size_gb += size
            f.write(f'<tr><td>{file_name}</td><td>{size:.2f} GB</td><td><button onclick="openLuna(\'{file_path}\')">Öffnen</button></td><td><button onclick="openInFinder(\'{file_path}\')">Im Finder anzeigen</button></td></tr>\n')
        f.write('</table>\n')
        f.write(f'<h2>Gesamtgröße aller Projekte: {total_size_gb:.2f} GB</h2>\n')
        f.write('<script>\n')
        f.write('function openLuna(path) {\n')
        f.write('  fetch("/open_luna", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded", }, body: "path=" + encodeURIComponent(path) })\n')
        f.write('  .then(response => response.json()).then(data => alert(data.message)).catch(error => console.error("Error:", error));\n')
        f.write('}\n')
        f.write('function openInFinder(path) {\n')
        f.write('  fetch("/open_in_finder", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded", }, body: "path=" + encodeURIComponent(path) })\n')
        f.write('  .then(response => response.json()).then(data => alert(data.message)).catch(error => console.error("Error:", error));\n')
        f.write('}\n')
        f.write('</script>\n')
        f.write('</body>\n</html>')

output_directory = '/Users/thomas/110_days_python/Test_Scripts/templates'
output_file = os.path.join(output_directory, 'treffer.html')

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open('/Users/thomas/110_days_python/Test_Scripts/treffer.txt', 'r', encoding='utf-8') as file:
    file_paths = file.read().splitlines()
    create_html_file(file_paths, output_file)
