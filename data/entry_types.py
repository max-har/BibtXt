# -*- coding: utf-8 -*-
"""This module contains information on entry types.

Contains a dict with all valid entry types and their required and optional
fields, a set of possible fields and a list of valid entry types.
"""
entry_types = {"article":
               {"required": {"author", "title", "journal", "year", "volume"},
                "optional": {"number", "pages", "month", "note", "key"}},
               "book":
               {"required": {"author/editor", "title", "publisher", "year"},
                "optional": {"volume/number", "series", "address", "edition",
                             "month", "note", "key", "url"}},
               "booklet":
               {"required": {"title"},
                "optional": {"author", "howpublished", "address", "month",
                             "year", "note", "key"}},
               "conference":
               {"required": {"author", "title", "booktitle", "year"},
                "optional": {"editor", "volume/number", "series", "pages",
                             "address", "month", "organization", "publisher",
                             "note", "key"}},
               "inbook":
               {"required": {"author/editor", "title", "chapter/pages",
                             "publisher", "year"},
                "optional": {"volume/number", "series", "type", "address",
                             "edition", "month", "note", "key"}},
               "incollection":
               {"required": {"author", "title", "booktitle", "publisher",
                             "year"},
                "optional": {"editor", "volume/number", "series", "type",
                             "chapter", "pages", "address", "edition", "month",
                             "note", "key"}},
               "inproceedings":
               {"required": {"author", "title", "booktitle", "year"},
                "optional": {"editor", "volume/number", "series", "pages",
                             "address", "month", "organization", "publisher",
                             "note", "key"}},
               "manual":
               {"required": {"title"},
                "optional": {"author", "organization", "address", "edition",
                             "month", "year", "note", "key"}},
               "mastersthesis":
               {"required": {"author", "title", "school", "year"},
                "optional": {"type", "address", "month", "note", "key"}},
               "misc":
               {"required": {},
                "optional": {"author", "title", "howpublished", "month",
                             "year", "note", "key"}},
               "phdthesis":
               {"required": {"author", "title", "school", "year"},
                "optional": {"type", "address", "month", "note", "key"}},
               "proceedings":
               {"required": {"title", "year"},
                "optional": {"editor", "volume/number", "series", "address",
                             "month", "publisher", "organization", "note",
                             "key"}},
               "techreport":
               {"required": {"author", "title", "institution", "year"},
                "optional": {"type", "number", "address", "month", "note",
                             "key"}},
               "unpublished":
               {"required": {"author", "title", "note"},
                "optional": {"month", "year", "key"}}}
fields = {"address", "annote", "author", "booktitle", "chapter", "crossref",
          "edition", "editor", "howpublished", "institution", "journal", "key",
          "month", "note", "number", "organization", "pages", "publisher",
          "school", "series", "title", "type", "volume", "year"}
types = list(entry_types.keys())
