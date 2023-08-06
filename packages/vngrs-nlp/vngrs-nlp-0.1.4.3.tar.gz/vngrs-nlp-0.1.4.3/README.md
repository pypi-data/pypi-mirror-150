<img src="https://github.com/vngrs-ai/vnlp/blob/main/img/logo.png?raw=true" width="256">

## VNLP: Turkish NLP Tools
State of the art, lightweight NLP tools for Turkish language.

Developed by VNGRS.

https://vngrs.com/


[![PyPI version](https://badge.fury.io/py/vngrs-nlp.svg)](https://badge.fury.io/py/vngrs-nlp)
[![Docs](<https://readthedocs.org/projects/vnlp/badge/?version=latest&style=plastic>)](https://vnlp.readthedocs.io/)
[![License](<https://img.shields.io/badge/license-AGPL%203.0-green.svg>)](https://github.com/vngrs-ai/vnlp/blob/main/LICENSE)

### Functionality:
- Sentence Splitter
- Normalizer
	- Spelling/Typo correction
	- Convert numbers to word form
	- Deasciification
- Stopword Remover:
	- Static
	- Dynamic
- Stemmer: Morphological Analyzer & Disambiguator
- Named Entity Recognizer (NER) 
- Dependency Parser
- Part of Speech (POS) Tagger
- Sentiment Analyzer
- Turkish Word Embeddings
	- FastText
	- Word2Vec
	- SentencePiece Unigram Tokenizer
- Text Summarization: In development progress...

### Demo:
- Try the [Demo](https://demo.vnlp.io).

### Installation
```
pip install vngrs-nlp
```

### Documentation:
- See the [Documentation](https://vnlp.readthedocs.io) for the details about usage, classes, functions, datasets and evaluation metrics.

### Usage Example:
**Dependency Parser**
```
from vnlp import DependencyParser
dep_parser = DependencyParser()

dep_parser.predict("Onun için yol arkadaşlarımızı titizlikle seçer, kendilerini iyice sınarız.")
[(1, 'Onun', 5, 'obl'),
(2, 'için', 1, 'case'),
(3, 'yol', 1, 'nmod'),
(4, 'arkadaşlarımızı', 5, 'obj'),
(5, 'titizlikle', 6, 'obl'),
(6, 'seçer', 7, 'acl'),
(7, ',', 10, 'punct'),
(8, 'kendilerini', 10, 'obj'),
(9, 'iyice', 8, 'advmod'),
(10, 'sınarız', 0, 'root'),
(11, '.', 10, 'punct')]

# Spacy's submodule Displacy can be used to visualize DependencyParser result.
import spacy
from vnlp import DependencyParser
dependency_parser = DependencyParser()
result = dependency_parser.predict("Oğuz'un kırmızı bir Astra'sı vardı.", displacy_format = True)
spacy.displacy.render(result, style="dep", manual = True)
```
<img src="https://raw.githubusercontent.com/vngrs-ai/vnlp/main/img/dp_vis_sample.png" width="512">
