Bib.tXt (c) Version 1.0 01/08/2018 (Python 2)
> Bib.tXt (c) Version 1.1 11/10/2020 (Python 3)

GENERAL USAGE NOTES
-------------------

+++ Execute BibtXt.py with Python 3 to run Bib.tXt. +++

A FILE MANIFEST:
- BibtXt.py (main file)
- doc.ipynb (documentation of this project; open with Jupyter Notebook)
In /data you can find all files which BibtXt.py requires to operate. The folder includes:
- entry_types.py (data concerning entry types)
- help.txt (information for user)
- __init__.py (technically needed)
In /xmp you can find example input files. The folder includes:
- additional_authors.bib
- author_editor_missing.bib
- author_missing.bib
- chapter_or_pages_missing.bib
- editor.bib
- entry_missing.bib
- multiple_authors.bib
- no_comma_author.bib
- no_comma_editor.bib
- reoccurrence.bib
- upper.bib
- whitespace.bib
- wrong_type.bib
- xmp.bib (main .txt file example)
- xmp.txt (main .bib file example)

\CITE COMMAND (.TXT FILE):
- \cite{key} for (author year)	
- \cite[suffix]{key} for (author year: suffix)
- \cite[prefix][]{key} for (prefix author year)
- \cite[prefix][suffix]{key} for (prefix author year suffix).

ENTRY TYPES (.BIB FILE):
- article
    An article from a journal or magazine.
    Required fields: author, title, journal, year, volume
    Optional fields: number, pages, month, note, key
- book
    A book with an explicit publisher.
    Required fields: author/editor, title, publisher, year
    Optional fields: volume/number, series, address, edition, month, note, key, url
- booklet
    A work that is printed and bound, but without a named publisher or sponsoring institution.
    Required fields: title
    Optional fields: author, howpublished, address, month, year, note, key
- conference
    The same as inproceedings, included for Scribe compatibility.
    Required fields: author, title, booktitle, year
    Optional fields: editor, volume/number, series, pages, address, month, organization, publisher, note, key
- inbook
    A part of a book, usually untitled. May be a chapter (or section, etc.) and/or a range of pages.
    Required fields: author/editor, title, chapter/pages, publisher, year
    Optional fields: volume/number, series, type, address, edition, month, note, key
- incollection
    A part of a book having its own title.
    Required fields: author, title, booktitle, publisher, year
    Optional fields: editor, volume/number, series, type, chapter, pages, address, edition, month, note, key
- inproceedings
    An article in a conference proceedings.
    Required fields: author, title, booktitle, year
    Optional fields: editor, volume/number, series, pages, address, month, organization, publisher, note, key
- manual
    Technical documentation.
    Required fields: title
    Optional fields: author, organization, address, edition, month, year, note, key
- mastersthesis
    A Master's thesis.
    Required fields: author, title, school, year
    Optional fields: type, address, month, note, key
- misc
    For use when nothing else fits.
    Required fields: none
    Optional fields: author, title, howpublished, month, year, note, key
- phdthesis
    A Ph.D. thesis.
    Required fields: author, title, school, year
    Optional fields: type, address, month, note, key
- proceedings
    The proceedings of a conference.
    Required fields: title, year
    Optional fields: editor, volume/number, series, address, month, publisher, organization, note, key
- techreport
    A report published by a school or other institution, usually numbered within a series.
    Required fields: author, title, institution, year
    Optional fields: type, number, address, month, note, key
- unpublished
    A document having an author and title, but not formally published.
    Required fields: author, title, note
    Optional fields: month, year, key

KNOWN BUGS:
- Multiple authors (cf. multiple_authors.bib): Please avoid multiple authors of one work in BibTeX database. Enter only one name for 'author'.
- Editor's name (cf. no_comma_editor.bib): Names of Editors are not analysed. Enter name in BibTeX database without comma.
- Optinal fields (cf. BibTeX key 'Goethe2000' in xmp.bib): Only required fields will be added to the bibliograpy. Please adjust your BibTeX database accordingly.

CREDITS AND ACKNOWLEDGEMENTS:
- Thanks to Johann Wolfgang von Goethe for "Faust: Der Tragödie erster Teil".
- Thanks to Gutenberg Project for free ebooks to download (Faust: Der Tragödie erster Teil by Johann Wolfgang von Goethe: https://www.gutenberg.org/cache/epub/2229/pg2229.txt).
==========================

Bib.tXt can be reached at:

Name: Max Harder
Student number: 2919411
E-mail: max.harder@uni-bielefeld.de

A Project for Mr Prof. Dr. David Schlangen's '230009 Einführung in die Programmierung: Python (S) (WiSe 2017/2018)' (23-TXT-BaCL3), Bielefeld University.

No Copyright 2018. All rights not reserved. Contrary information only by accident.
