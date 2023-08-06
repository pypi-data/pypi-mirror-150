# multi-rename

[![PyPI Release](https://img.shields.io/pypi/v/multi-rename?color=blue)](https://img.shields.io/pypi/v/multi-rename?color=blue)
[![GitHub Release](https://img.shields.io/github/v/release/pshkrh/multi-rename)](https://img.shields.io/github/v/release/pshkrh/multi-rename)
[![License](https://img.shields.io/pypi/l/multi-rename)](https://img.shields.io/pypi/l/multi-rename)

A python module for renaming multiple files in a directory to a common format ending with incrementing numbers. The increment start and gap between increments is configurable, and a separator string can be specified to be inserted between the new name and the incrementing number.

It also supports adding a prefix or suffix to each file in a directory, with options for a separator strings.

For both full renaming and prefix / suffix renaming, a list of file extensions can be provided as a filter to ignore these files for renaming.

## Installation

Install using pip:

```sh
pip install multi-rename
```

## Usage

```Python
from multi_rename import renamer

# Fully rename all the files with incrementing file numbers, exlcuding any html files
renamer.full_rename(dir_path='/path/to/dir/here', new_name='new_file_name', filter_ext='html')

# Add a prefix to all the files with an underscore separator, excluding any txt files
renamer.add_prefix(dir_path='/path/to/dir/here', prefix='prefix_to_add', sep='_', filter_ext='txt')

# Add a suffix to all the files with a hyphen separator, excluding any pdf files
renamer.add_suffix(dir_path='/path/to/dir/here', suffix='suffix_to_add', sep='-', filter_ext='pdf')

```

## Example

### Folder structure with sample files
```md
expenses.xlsx
report.pdf
essay.docx
webpage.html
...
```

### Full rename
```Python
renamer.full_rename(dir_path='/home/dir_path/', new_name='print-this', sep='-')
```

This will rename all the file names in `dir_path` to `print-this` followed by a hyphen and incrementing numbers:

```md
print-this-1.xlsx
print-this-2.pdf
print-this-3.docx
print-this-4.html
...
```

### Adding a prefix
```Python
renamer.add_prefix(dir_path='/home/dir_path/', prefix='v1', sep='-')
```

This will rename all the file names in `dir_path` to start with `v1-`:

```md
v1-expenses.xlsx
v1-report.pdf
v1-essay.docx
v1-webpage.html
...
```

### Adding a suffix
```Python
renamer.add_suffix(dir_path='/home/dir_path/', suffix='old', sep='_')
```

This will rename all the file names in `dir_path` to end with `_old`:

```md
expenses_old.xlsx
report_old.pdf
essay_old.docx
webpage_old.html
...
```

### Changing file extensions
```Python
renamer.change_extension(dir_path='/home/dir_path/', new_ext='txt', filter_ext='html')
```

This will change all the file extensions in `dir_path` to `.txt`, except any `.html` files:

```md
expenses.txt
report.txt
essay.txt
webpage.html
...
```

## Contributing

If you have any bug fixes / useful feature additions, feel free to fork this repository, make your changes and drop in a pull request.

## License

[MIT](https://github.com/pshkrh/multi-rename/blob/master/LICENSE)
