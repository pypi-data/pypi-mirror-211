import os

from .parsers import code_reference_parser


class DocGenerator:
    parsers = []
    _default_parsers = [code_reference_parser]
    output_dirs = []

    def __init__(self, docs_folder, compiled_docs_folder):
        self.docs_folder = docs_folder
        self.compiled_docs_folder = compiled_docs_folder

    def _get_compiled_folder_path(self, path=None):
        cwd = os.getcwd()
        if path and path.startswith('/'):
            path = path[1:]
        return f'{cwd}/{self.compiled_docs_folder}/{path}' if path else f'{cwd}/{self.compiled_docs_folder}'

    def _write_file(self, lines, filepath):
        base = filepath.replace(self.docs_folder, '')
        path = self._get_compiled_folder_path(base)

        with open(path, 'w') as f:
            f.write(lines)

    def _parse_file(self, filepath):
        compiled_markdown = ''

        with open(filepath) as f:
            markdown = f.readlines()

        for line in markdown:
            for parser in self.parsers + self._default_parsers:
                parsed = parser(line)
                if parsed is not None:
                    compiled_markdown += parsed
                    break
            if parsed is None:
                compiled_markdown += line
        return compiled_markdown

    def _create_folder_structure(self):
        compiled_path = self._get_compiled_folder_path()
        os.makedirs(compiled_path, exist_ok=True)

        for root, dirs, files in os.walk(self.docs_folder):
            for dir in dirs:
                path = f'{compiled_path}/{root.replace(self.docs_folder, "")}/{dir}'
                os.makedirs(path, exist_ok=True)

    def generate(self):
        self._create_folder_structure()

        for root, dirs, files in os.walk(self.docs_folder):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith('.md'):
                    compiled_lines = self._parse_file(path)
                    self._write_file(compiled_lines, path)
                else:
                    os.system(f'cp {path} {self._get_compiled_folder_path()}/{root.replace(self.docs_folder, "")}')


if __name__ == '__main__':
    generator = DocGenerator('docs', 'docs_compiled')
    generator.generate()
