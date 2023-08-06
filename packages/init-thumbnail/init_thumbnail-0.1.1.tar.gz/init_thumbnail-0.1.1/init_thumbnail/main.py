import click
import os



@click.command(
        help="Creates template for youtube thumbnail"
        )
@click.option(
        '-i',
        '--inputpath',
        type=click.Path(),
        default="./",
        show_default=True,
        help="Input path"
        )
def main(inputpath):
    path_tikz = os.path.dirname(os.path.abspath(inputpath))
    os.makedirs(f'{path_tikz}/thumbnail', exist_ok=True)
    path_main = os.path.join(f'{path_tikz}/thumbnail', 'main.tex')
    
    with open(path_main, 'w') as file:
        file.write(f'\\documentclass{{article}}\n')
        file.write(f'\\usepackage{{v-equation}}\n')
        file.write(f'\\vgeometry[6][3.375]\n')

        file.write(f'\\begin{{document}}\n')
        file.write(f'\\vtitle[title]\n')
        file.write(f'\\vprofile\n')
        file.write(f'\\vspace*{{\\fill}}\n')
        file.write(f'\\begin{{center}}\n')
        file.write(f'\\begin{{tikzpicture}}\n')
        file.write(f'[remember picture, overlay]\n')
        file.write(r"""\tzcoor*(current page.center)(O){{$O$}}[bl]""")
        file.write(f'\n\\end{{tikzpicture}}\n')
        file.write(f'\\end{{center}}\n')

        file.write(f'\\vspace*{{\\fill}}\n')
        file.write(f'\\end{{document}}')













