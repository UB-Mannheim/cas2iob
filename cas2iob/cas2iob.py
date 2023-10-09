import typer
from cassis import load_typesystem, load_cas_from_xmi
from pathlib import Path
from tqdm import tqdm
from typing import List
from typing_extensions import Annotated

cli = typer.Typer()


def get_tags(input_file: Path, typesystem_xml: Path) -> List:
    """It returns annotated sentences, tokens and entities from an UIMA CAS XMI file"""
    with open(typesystem_xml, 'rb') as xml:
        typesystem = load_typesystem(xml)
    with open(input_file, 'rb') as xmi:
        cas = load_cas_from_xmi(xmi, typesystem=typesystem)
    sentences = list(cas.select('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence'))
    tokens = list(cas.select('de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token'))
    entities = list(cas.select('de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity'))
    return [sentences, tokens, entities]


def get_id(identifier: str) -> str:
    """It returns either Wikidata-QID or 'O'"""
    if identifier:
        return identifier.split('http://www.wikidata.org/entity/')[1]
    else:
        return 'O'


def convert(sentences, tokens, entities, filename: Path = '', metadata=bool) -> List:
    """Converts UIMA CAS annotations into IOB format and returns a list with IOB-content and errors"""
    if metadata:
        iob_tsv = ['TOKEN\tNE-COARSE\tNE-FINE\tNE-FINE-COMP\tNE-NESTED\tNEL-WikidataQID']
    else:
        iob_tsv = []
    errors = []

    for sentence in sentences:
        sbegin = sentence.begin
        send = sentence.end
        tokens_for_this_sentence = [t for t in tokens if (t.begin >= sbegin and t.end <= send)]

        for token in tokens_for_this_sentence:
            try:
                tbegin = token.begin
                tend = token.end
                ttext = token.get_covered_text()

                entities_for_this_token = [e for e in entities if (e.begin <= tbegin and e.end >= tend)]
                if len(entities_for_this_token) == 0:
                    ne_coarse = 'O'
                    ne_fine = 'O'
                    identifier = 'O'
                    nested = 'O'
                    component = 'O'
                if len(entities_for_this_token) >= 1:
                    min_begin = min([e.begin for e in entities if (e.begin <= tbegin and e.end >= tend)])
                    max_end = max([e.end for e in entities if (e.begin <= tbegin and e.end >= tend)])
                    for entity in entities_for_this_token:
                        ner_type = entity.value
                        begin = entity.begin
                        end = entity.end
                        covered_text = entity.get_covered_text()
                        identifier = get_id(entity.identifier)
                        if begin == min_begin and end == max_end:
                            nested = 'O'
                        elif not ner_type.startswith('COMP'):
                            nested = 'B-' + ner_type if tbegin == begin else 'I-' + ner_type
                        if ner_type.startswith('COMP'):
                            component = ner_type
                        else:
                            component = 'O'
                        if nested == 'O' and component == 'O':
                            nertype = ner_type
                            b = begin

                    if begin <= end:
                        ne_coarse = 'B-' + nertype.split('.')[0] if tbegin == b else 'I-' + nertype.split('.')[0]
                        ne_fine = 'B-' + nertype if tbegin == b else 'I-' + nertype
            except:
                err = [filename, sentence.get_covered_text()[begin - sbegin:end - sbegin], str(begin), str(end)]
                if len(errors) > 0:
                    if err != errors[-1]:
                        errors.append(err)
                else:
                    errors.append(err)

            iob_tsv.append(f"{ttext}\t{ne_coarse}\t{ne_fine}\t{component}\t{nested}\t{identifier}")

        iob_tsv.append('') # empty line between sentences

    return [iob_tsv, errors]


def file(input_file: Path, output_file: Path, typesystem_xml: Path = './TypeSystem.xml', metadata=True):
    """For the given input UIMA CAS XMI file and TypeSystem.xml-file it
    converts it into IOB TSV file"""
    [sentences, tokens, entities] = get_tags(input_file, typesystem_xml)
    [iob_tsv, errors] = convert(sentences, tokens, entities, Path(input_file).name)
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write('\n'.join(iob_tsv))
    with open('./entities_without_tags.txt', 'a', encoding='utf-8') as errs:
        for error in errors:
            errs.write('\t'.join(error) + "\n")


def folder(input_folder: Path, output_folder: Path, typesystem_xml: Path = './TypeSystem.xml', metadata=True):
    """For the given input folder and TypeSystem.xml-file it converts all UIMA 
    CAS XMI files from the input folder into IOB TSV files in the output folder"""
    file_paths = Path(input_folder).glob('*.xmi')
    for file_path in tqdm(file_paths):
        print(file_path, flush=True)
        output_file = Path(output_folder, file_path.stem + '.tsv').as_posix()
        file(file_path.as_posix(), output_file, typesystem_xml)


@cli.command()
def load(input_path: Path, output_path: Path, typesystem_xml: Annotated[str, typer.Argument()] = './TypeSystem.xml', metadata: Annotated[bool, typer.Argument()] = True):
    if Path(input_path).is_file() and Path(output_path).is_file():
        file(input_path, output_path, typesystem_xml, metadata)
    elif Path(input_path).is_dir() and Path(output_path).is_dir():
        folder(input_path, output_path, typesystem_xml, metadata)
    else:
        print("ERROR: Specify the paths for files OR the paths for folders.")
