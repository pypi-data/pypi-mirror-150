import spacy

LANG_MODEL_NAME = 'en_core_web_md'

nlp = None
for i in range(2):
    try:
        nlp = spacy.load(LANG_MODEL_NAME)
    except IOError:
        spacy.cli.download(LANG_MODEL_NAME)
    if nlp is not None:
        break
