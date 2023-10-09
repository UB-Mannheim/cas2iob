# CAS2IOB

CAS2IOB is a converter of UIMA CAS XMI files using in the INCEpTION annotation platform into IOB TSV files. In contrast to the internal convertor in INCEpTION, it handles the nested NER tags, NEL tags and components, and saves them into multiple columns of a TSV-file:
```
TOKEN  NE-COARSE   NE-FINE NE-FINE-COMP    NE-NESTED   NEL-WikidataQID
```

It reads the UIMA CAS XMI files using [dkpro-cassis](https://github.com/dkpro/dkpro-cassis) library.

## Installation

```python
pip install cas2iob
```

## Using as a library

Import cas2iob:
```python
import cas2iob
```

Convert `./input.xmi` with `./TypeSystem.xml` into `./output.tsv`:
```python
cas2iob.file('./input.xmi', 'output.tsv')
```

Convert all files in `./input` folder with `./TypeSystem.xml` into `./output` folder:
```python
cas2iob.folder('./input', './output')
```

If `./TypeSystem.xml` is located in a different folder, add it to the commands above as the third argument.

If you don't want to include column names in a TSV-file, add the forth argument `metadata=False`.

## Using in CLI

```shell
% cas2iob --help
                                                                                
 Usage: cas2iob [OPTIONS] INPUT_PATH OUTPUT_PATH [TYPESYSTEM_XML] [METADATA]    
                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────╮
│ *    input_path          PATH              [default: None] [required]        │
│ *    output_path         PATH              [default: None] [required]        │
│      typesystem_xml      [TYPESYSTEM_XML]  [default: ./TypeSystem.xml]       │
│      metadata            [METADATA]        [default: True]                   │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.      │
│ --show-completion             Show completion for the current shell, to copy │
│                               it or customize the installation.              │
│ --help                        Show this message and exit.                    │
╰──────────────────────────────────────────────────────────────────────────────╯
```
