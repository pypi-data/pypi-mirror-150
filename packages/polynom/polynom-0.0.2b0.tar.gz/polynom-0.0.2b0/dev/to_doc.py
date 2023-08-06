from py_to_md import py_source_to_token, token_line_to_yaml, yaml_to_md

import pathlib


def main():
    for name in ('_base', 'chebyshev', 'gegenbauer', 'lagrange', 'legendre', 'monomial', 'newton', 'shared'):
        path = pathlib.Path(f'../src_py/polynom/{name}').with_suffix('.py')

        mds = yaml_to_md(name_of_md_file = name, struct = token_line_to_yaml(py_source_to_token(path_from = path)))
        for idx, (name, md) in enumerate(mds):
            _path: pathlib.Path = pathlib.Path(f'../docs/pages/polynom')
            _path.mkdir(parents = True, exist_ok = True)
            _path = (_path/f'{name}').with_suffix('.md')
            with open(_path, mode = 'w') as out_stream:
                out_stream.write(md)


if __name__ == '__main__': main()
