#!/usr/bin/env bash

python code/ch02/book_thief_sentence_split_graphviz.py
python code/ch01/NLU_NLG_graphviz.py
python code/scripts/render_html.py
firefox $(pwd)/manuscript/html
