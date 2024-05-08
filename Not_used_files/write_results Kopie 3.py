import configparser
import os

def load_configuration(config_path):
    """Load the configuration file."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']['protected_dir']

def get_directory_size(directory):
    """Calculate the size of a directory in Gigabytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 ** 3)  # Convert Bytes to Gigabytes

def create_html_file(file_paths, output_file, protected_dir):
    """Creates an HTML file with information on the found projects."""
    total_size_gb = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n')
        f.write('<link rel="stylesheet" type="text/css" href="/static/css/style.css">\n')
        f.write('<title>Luna Project Search</title>\n</head>\n<body>\n')
        f.write('<header>\n<img src="/static/images/Neve.png" class="header-image">\n<h1>Luna Project Search</h1>\n</header>\n')
        f.write('<table>\n')
        f.write('<tr><th>Select</th><th>Project Name</th><th>Size (GB)</th><th>Open in Luna</th><th>Open in Finder</th></tr>\n')
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            size = get_directory_size(file_path)
            total_size_gb += size
            highlight_class = ' highlight' if protected_dir in file_path else ""
            f.write(f'<tr{highlight_class}><td><input type="checkbox" name="project" value="{file_path}"></td><td>{file_name}</td><td>{size:.2f}</td>')
            f.write(f'<td><button onclick="openLuna(\'{file_path}\')">Open</button></td>')
            f.write(f'<td><button onclick="openInFinder(\'{file_path}\')">Show in Finder</button></td></tr>\n')
        f.write('</table>\n')
        f.write(f'<h2>Total size of all projects: {total_size_gb:.2f} GB</h2>\n')
        f.write(f'<h3>Number of projects: {len(file_paths)}</h3>\n')
        f.write('<script src="/static/js/scripts.js"></script>\n')
        f.write('</body>\n</html>')

def main():
    config_path = '/Users/thomas/MyApps/Luna_Search/static/ini/import.ini'
    protected_dir = load_configuration(config_path)
    input_file = os.path.join(os.path.dirname(__file__), '../templates/treffer.txt')
    output_file = os.path.join(os.path.dirname(__file__), '../templates/treffer.html')

    with open(input_file, 'r', encoding='utf-8') as file:
        file_paths = file.read().splitlines()

    create_html_file(file_paths, output_file, protected_dir)
    print("HTML file has been created and is located here: {}".format(output_file))

if __name__ == "__main__":
    main()
