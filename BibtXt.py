#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This module contains the class BibTeX."""
import io
import os
import re
import sys
import time
from datetime import date

from data.entry_types import entry_types
from data.entry_types import types
from data.entry_types import fields

no_author = "n.a."
no_title = "n.a."
no_year = "n.d."


class BibTeX(object):
    """Take .txt and .bib file and return output file.

    .txt file includes references and the .bib file constitutes the
    database of all reference-list entries. Output file (.txt) includes
    author-year citations and reference list.
    """

    def __init__(self, txt=None, bib=None, output=None):
        """Initialize an instance of the class.

        txt -- user's .txt file (default None)
        bib --  user's .bib file (default None)
        output -- path to output file (default None)
        """
        welcome = ("----------------------------"
                   "\nBib.tXt (c) {} Max Harder.\n"
                   "----------------------------".format(date.today().year))
        help = "help"
        quit = "quit"
        introduction = ("\nPress Enter to continue or type \'{}\' for a brief "
                        "description of Bib.tXt. You can always use \'{}\' to "
                        "end the program: ".format(help, quit))
        error = "Error. Document name or path does not end with \'.{}\'."
        ioerror = "Error. The document name or path is not valid."
        path = "Enter relative path for desired .{} file: /"
        print(welcome)
        enter = input(introduction)
        if enter == help:
            try:
                # directory path of this file:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                with io.open(os.path.join(dir_path, 'data/help.txt'),
                             encoding="utf-8") as file:
                    information = file.read()
            except (IOError, NameError):
                with io.open(os.path.abspath('data/help.txt'),
                             encoding="utf-8") as file:
                    information = file.read()
            print(information)
            input("Press Enter to continue: ")
        elif enter == quit:
            return
        print("Your current working directory (cwd) is:")
        cwd = os.getcwd()
        print(cwd)
        while not txt:
            try:
                txt_rel_path = input(path.format("txt"))
                if txt_rel_path == quit:
                    return
                if txt_rel_path.endswith(".txt"):
                    txt_abs_path = os.path.join(cwd, txt_rel_path)
                    with io.open(txt_abs_path, encoding="utf-8") as file:
                        txt = file.read()
                else:
                    print(error.format("txt"))
            except IOError:
                print(ioerror)

        while not bib:
            try:
                bib_rel_path = input(path.format("bib"))
                if bib_rel_path == quit:
                    return
                if bib_rel_path.endswith(".bib"):
                    bib_abs_path = os.path.join(cwd, bib_rel_path)
                    with io.open(bib_abs_path, encoding="utf-8") as file:
                        bib = file.read()
                else:
                    print(error.format("bib"))
            except IOError:
                print(ioerror)

        while not output:
            try:
                path_question = input("Create output file in cwd (y/[n])?: ")
                if path_question == quit:
                    return
                elif path_question == "y":
                    out_name = input("Enter name of output file: ")
                    if out_name.endswith('.txt'):
                        out_full_path = os.path.join(cwd, out_name)
                    else:
                        out_full_path = os.path.join(cwd, out_name+".txt")
                else:
                    out_rel_path = input("Enter relative path "
                                         "for output file: /")
                    if out_rel_path == quit:
                        return
                    out_abs_path = os.path.join(cwd, out_rel_path)
                    if not os.path.exists(out_abs_path):
                        os.makedirs(out_abs_path)
                    out_name = input("Enter name of output file: ")
                    if out_name == quit:
                        return
                    if out_name.endswith('.txt'):
                        out_full_path = os.path.join(out_abs_path, out_name)
                    else:
                        out_full_path = os.path.join(out_abs_path,
                                                     out_name + ".txt")
                output_file = open(out_full_path, "w+")
                output_file.close()
                output = out_full_path
            except (OSError, IOError):
                print(ioerror)

            self.txt = txt
            self.bib = bib
            self.output = output

    def check_all_keys(self):
        """Check all occurrences of BibTeX keys.

        Return list of keys occurring in .bib but not in .txt file. Exit if
        multiple occurrences of key in .bib file exist or if key in .txt
        file is not specified in .bib file.
        """
        re_keys = r"\\cite(?:\[[^[\]]*\])?(?:\[[^[\]]*\])?{(\w+)}"
        all_keys_txt = re.findall(re_keys, self.txt)
        all_keys_bib = re.findall(r"@\w+\{(\w+),", self.bib)
        key_not_in_txt = [key for key in all_keys_bib if
                          key not in all_keys_txt]
        for txt_key in all_keys_txt:
            if all_keys_bib.count(txt_key) > 1:
                sys.exit("Error: Reoccurrence of the BibTeX key \'{}\'"
                         " detected. Please revise entered .bib file."
                         .format(txt_key))
            if txt_key not in all_keys_bib:
                sys.exit("Error: \'{}\' is not a specified BibTeX key."
                         " Please revise entered .txt or .bib file."
                         .format(txt_key))
        return key_not_in_txt

    def check_all_types(self):
        """Check all entry types in .bib file. Exit if type is not valid."""
        all_types = re.findall(r"@(\w+)\{", self.bib)
        for mytype in all_types:
            if mytype.lower() not in types:
                sys.exit("Error: \'{}\' is not a valid entry type."
                         " Please revise entered .bib file.".format(mytype))

    def bib_to_dict(self, key_not_in_txt):
        """Convert data of .bib file into dict and return dict.

        Three-layer dict: keys, fields, values.
        """
        re_bib = r"@\w+\{"+"(\w+)"+",([\w\s={}\/\.:,;-]+)(?=(?:@\w+\{)|\Z)"
        basis_dict, field_value_dict = {}, {}
        # tuple_list: [(key, field=value,\n etc.) etc.]
        tuple_list = [match.group(1, 2) for match in
                      re.finditer(re_bib, self.bib, re.UNICODE)]
        # key_val_tuple: (key, field=value,\n …)
        key_list = [key_val_tuple[0] for key_val_tuple in tuple_list]
        for key_val_tuple in tuple_list:
            basis_dict[key_val_tuple[0]] = key_val_tuple[1].splitlines()
        for key in key_list:
            # unsplit_data: field=value
            for unsplit_data in basis_dict[key]:
                # strip whitespace from the beginning of the string:
                unsplit_data = unsplit_data.lstrip()
                if any([unsplit_data.lower()
                        .startswith(field) for field in fields]):
                    split_data = re.split(r"\s+=\s+", unsplit_data)
                    final_value = re.search(r"{*([\w\s\/\.:,;-]+)}*",
                                            split_data[1], re.UNICODE).group(1)
                    # remove comma after digit and full stop after title etc.:
                    if final_value.endswith((",", ".")):
                        final_value = final_value[:-1]
                    field_value_dict[split_data[0].lower()] = final_value
            basis_dict[key] = {}
            basis_dict[key].update(field_value_dict)
            field_value_dict = {}
            if "author" in basis_dict[key]:
                if "," in basis_dict[key]["author"]:
                    split_name = basis_dict[key]["author"].split(",")
                    surname = split_name[0].strip()
                    forename = split_name[1].strip()
                    basis_dict[key]["author"] = {"surname": surname}
                    basis_dict[key]["author"].update({"forename": forename})
                else:
                    split_name = basis_dict[key]["author"].split()
                    surname = split_name[-1].strip()
                    forename = " ".join(split_name[:-1]).strip()
                    basis_dict[key]["author"] = {"surname": surname}
                    basis_dict[key]["author"].update({"forename": forename})
        # remove keys not occurring in .txt file
        for ghost_key in key_not_in_txt:
            basis_dict.pop(ghost_key)
        for key in basis_dict.keys():
            basis_dict[key]["author"] = basis_dict[key].get(
                                        "author", {"surname": no_author,
                                                   "forename": ""})
            basis_dict[key]["year"] = basis_dict[key].get("year", no_year)
        return basis_dict

    def check_required_fields(self, basis_dict):
        """Check if required fields are given in .bib file.

        Return dict of keys and their entry types. Exit if required field is
        not given.
        """
        field_error = ("Error: \'{}\' is a required field for \'{}\'. "
                       "Please revise entered .bib file.")
        field_error_2 = ("Error: \'{}\' or \'{}\' is a required field for "
                         "\'{}\'. Please revise entered .bib file.")
        key_type_tuples = [match.group(2, 1) for match
                           in re.finditer(r"@(\w+)\{(\w+),", self.bib)]
        for mytuple in key_type_tuples:
            for key in basis_dict.keys():
                if key in mytuple:
                    given = [field.lower() for field in basis_dict[key].keys()]
                    # remove generated entries for 'author':
                    if basis_dict[key]["author"]["surname"] == no_author:
                        given.remove("author")
                    for needed in entry_types[mytuple[1].lower()]["required"]:
                        split_fields = [element for element
                                        in needed.split("/")
                                        if re.findall(r"\w+/\w+", needed)]
                        if needed not in given:
                            if re.findall(r"\w+/\w+", needed):
                                if (split_fields[0] not in given
                                   and split_fields[1] not in given):
                                    sys.exit(field_error_2
                                             .format(split_fields[0],
                                                     split_fields[1],
                                                     mytuple[1]))
                            else:
                                sys.exit(field_error
                                         .format(needed, mytuple[1]))
        key_type_dict = dict(key_type_tuples)
        return key_type_dict

    def transfer(self, basis_dict):
        """Transfer (modified) content of .txt to output file.

        Transfer content and convert references into author-year citations.
        """
        all_varieties = r"(\\cite(?:\[([^[\]]*)\])?(?:\[([^[\]]*)\])?{(\w+)})"
        page_only = r"(\\cite(?:\[([^[\]]*)\]){(\w+)})"
        # quotes: [(u'\\cite[x][y]{z}', u'x', u'y', u'z') etc.]
        quotes = re.findall(all_varieties, self.txt)
        cite_start = ([match.start() for match in re.finditer
                      (r"\\cite(?:\[[^[\]]*\]){0,2}{\w+}", self.txt)])
        cite_end = ([match.end() for match in re.finditer
                    (r"\\cite(?:\[[^[\]]*\]){0,2}{\w+}", self.txt)])
        # cite_position: [(1st, 1st), (2nd, 2nd) etc.]
        cite_position = list(zip(cite_start, cite_end))
        start, count, num = 0, 1, 0
        for position in cite_position:
            with io.open(self.output, mode="a", encoding="utf-8") as file:
                file.write(self.txt[start:position[0]])
                # page(+suffix):
                if (re.match(page_only, quotes[num][0])
                   and quotes[num][1] and not quotes[num][2]):
                    file.write(u"({} {}: {})".format(
                               basis_dict[quotes[num][3]]["author"]["surname"],
                               basis_dict[quotes[num][3]]["year"],
                               quotes[num][1]))
                # prefix:
                elif quotes[num][1] and not quotes[num][2]:
                    file.write(u"({} {} {})".format(
                               quotes[num][1],
                               basis_dict[quotes[num][3]]["author"]["surname"],
                               basis_dict[quotes[num][3]]["year"]))
                # prefix and page(+suffix):
                elif quotes[num][1] and quotes[num][2]:
                    file.write(u"({} {} {}: {})".format(
                               quotes[num][1],
                               basis_dict[quotes[num][3]]["author"]["surname"],
                               basis_dict[quotes[num][3]]["year"],
                               quotes[num][2]))
                # nothing:
                elif not quotes[num][1] and not quotes[num][2]:
                    file.write(u"({} {})".format(
                               basis_dict[quotes[num][3]]["author"]["surname"],
                               basis_dict[quotes[num][3]]["year"]))
                if count == len(cite_position):
                    file.write(self.txt[position[1]:])
            start = position[1]
            count += 1
            num += 1

    def bibliography(self, data, key_type_dict):
        """Append bibliography to output file."""
        entitle = input("Entitle reference list \'Bibliography\' (y/[n])?")
        if entitle == "y":
            title = u"Bibliography"
            superscription = u"\n{}\n{}".format(title, len(title)*u"=")
        else:
            title = ""
            while not title:
                try:
                    title = (input("Enter title of reference list: ")
                             .decode("utf-8"))
                except UnicodeDecodeError:
                    print("Error. Please use \"UTF-8\" or avoid special "
                          "characters.")
            superscription = u"\n{}\n{}".format(title, len(title)*u"=")
        signature = u"\n\nGenerated with Bib.tXt (c) by Max Harder. {}."
        with io.open(self.output, mode="a", encoding="utf-8") as file:
            file.write(superscription)
            surname_key_tuples = [(data[element]["author"]["surname"],
                                  element) for element in data]
            surname_key_tuples.sort()
            for tuple in surname_key_tuples:
                # article
                if key_type_dict[tuple[1]].lower() == "article":
                    file.write(u"\n{}, {} ({}): {}. In: {} {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["year"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["journal"],
                               data[tuple[1]]["volume"]))
                # book
                elif key_type_dict[tuple[1]].lower() == "book":
                    if data[tuple[1]]["author"]["surname"] != no_author:
                        file.write(u"\n{}, {}; ed. {} ({}): {}. {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["author"]["forename"],
                                   data[tuple[1]].get("editor", no_author),
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"],
                                   data[tuple[1]]["publisher"]))
                    else:
                        file.write(u"\n{}; ed. {} ({}): {}. {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]].get("editor", no_author),
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"],
                                   data[tuple[1]]["publisher"]))
                # booklet
                elif key_type_dict[tuple[1]].lower() == "booklet":
                    if data[tuple[1]]["author"]["surname"] != no_author:
                        file.write(u"\n{}, {} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["author"]["forename"],
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"]))
                    else:
                        file.write(u"\n{} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"]))
                # conference
                elif key_type_dict[tuple[1]].lower() == "conference":
                    file.write(u"\n{}, {} ({}): {}. In: {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["year"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["booktitle"]))
                # inbook
                elif key_type_dict[tuple[1]].lower() == "inbook":
                    if data[tuple[1]]["author"]["surname"] != no_author:
                        if ("chapter" in data[tuple[1]]
                           and "pages" in data[tuple[1]]):
                            file.write(u"\n{}, {}; ed. {} ({}): {}, "
                                       "chapter {}, pages {}. {}.".format(
                                        data[tuple[1]]["author"]["surname"],
                                        data[tuple[1]]["author"]["forename"],
                                        data[tuple[1]].get("editor",
                                                           no_author),
                                        data[tuple[1]]["year"],
                                        data[tuple[1]]["title"],
                                        data[tuple[1]]["chapter"],
                                        data[tuple[1]]["pages"],
                                        data[tuple[1]]["publisher"]))
                        if ("chapter" in data[tuple[1]]
                           and "pages" not in data[tuple[1]]):
                            file.write(u"\n{}, {}; ed. {} ({}): {}, "
                                       "chapter {}. {}.".format(
                                        data[tuple[1]]["author"]["surname"],
                                        data[tuple[1]]["author"]["forename"],
                                        data[tuple[1]].get("editor",
                                                           no_author),
                                        data[tuple[1]]["year"],
                                        data[tuple[1]]["title"],
                                        data[tuple[1]]["chapter"],
                                        data[tuple[1]]["publisher"]))
                        if ("chapter" not in data[tuple[1]]
                           and "pages" in data[tuple[1]]):
                            file.write(u"\n{}, {}; ed. {} ({}): {}, "
                                       "pages {}. {}.".format(
                                        data[tuple[1]]["author"]["surname"],
                                        data[tuple[1]]["author"]["forename"],
                                        data[tuple[1]].get("editor",
                                                           no_author),
                                        data[tuple[1]]["year"],
                                        data[tuple[1]]["title"],
                                        data[tuple[1]]["pages"],
                                        data[tuple[1]]["publisher"]))
                    else:
                        if ("chapter" in data[tuple[1]]
                           and "pages" in data[tuple[1]]):
                            file.write(u"\n{}; ed. {} ({}): {}, "
                                       "chapter {}, pages {}. {}.".format(
                                        data[tuple[1]]["author"]["surname"],
                                        data[tuple[1]].get("editor",
                                                           no_author),
                                        data[tuple[1]]["year"],
                                        data[tuple[1]]["title"],
                                        data[tuple[1]]["chapter"],
                                        data[tuple[1]]["pages"],
                                        data[tuple[1]]["publisher"]))
                        if ("chapter" in data[tuple[1]]
                           and "pages" not in data[tuple[1]]):
                            file.write(u"\n{}; ed. {} ({}): {}, "
                                       "chapter {}. {}.".format(
                                        data[tuple[1]]["author"]["surname"],
                                        data[tuple[1]].get("editor",
                                                           no_author),
                                        data[tuple[1]]["year"],
                                        data[tuple[1]]["title"],
                                        data[tuple[1]]["chapter"],
                                        data[tuple[1]]["publisher"]))
                        if ("chapter" not in data[tuple[1]]
                           and "pages" in data[tuple[1]]):
                            file.write(u"\n{}; ed. {} ({}): {}, "
                                       "pages {}. {}.".format(
                                        data[tuple[1]]["author"]["surname"],
                                        data[tuple[1]].get("editor",
                                                           no_author),
                                        data[tuple[1]]["year"],
                                        data[tuple[1]]["title"],
                                        data[tuple[1]]["pages"],
                                        data[tuple[1]]["publisher"]))
                # incollection
                elif key_type_dict[tuple[1]].lower() == "incollection":
                    file.write(u"\n{}, {} ({}): {}. In: {}, {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["year"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["publisher"],
                               data[tuple[1]]["booktitle"]))
                # inproceedings
                elif key_type_dict[tuple[1]].lower() == "inproceedings":
                    file.write(u"\n{}, {} ({}): {}. In: {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["year"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["booktitle"]))
                # manual
                elif key_type_dict[tuple[1]].lower() == "manual":
                    if data[tuple[1]]["author"]["surname"] != no_author:
                        file.write(u"\n{}, {} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["author"]["forename"],
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"]))
                    else:
                        file.write(u"\n{} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"]))
                # mastersthesis
                elif key_type_dict[tuple[1]].lower() == "mastersthesis":
                    file.write(u"\n{}, {} ({}): {}. "
                               "Master's thesis, {}.".format(
                                data[tuple[1]]["author"]["surname"],
                                data[tuple[1]]["author"]["forename"],
                                data[tuple[1]]["year"],
                                data[tuple[1]]["title"],
                                data[tuple[1]]["school"]))
                # misc
                elif key_type_dict[tuple[1]].lower() == "misc":
                    if data[tuple[1]]["author"]["surname"] != no_author:
                        file.write(u"\n{}, {} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["author"]["forename"],
                                   data[tuple[1]]["year"],
                                   data[tuple[1]].get("title", no_title)))
                    else:
                        file.write(u"\n{} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["year"],
                                   data[tuple[1]].get("title", no_title)))
                # phdthesis
                elif key_type_dict[tuple[1]].lower() == "phdthesis":
                    file.write(u"\n{}, {} ({}): {}. PhD thesis, {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["year"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["school"]))
                # proceedings
                elif key_type_dict[tuple[1]].lower() == "proceedings":
                    if data[tuple[1]]["author"]["surname"] != no_author:
                        file.write(u"\n{}, {}; ed. {} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]]["author"]["forename"],
                                   data[tuple[1]].get("editor", no_author),
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"]))
                    else:
                        file.write(u"\n{}; ed. {} ({}): {}.".format(
                                   data[tuple[1]]["author"]["surname"],
                                   data[tuple[1]].get("editor", no_author),
                                   data[tuple[1]]["year"],
                                   data[tuple[1]]["title"]))
                # techreport
                elif key_type_dict[tuple[1]].lower() == "techreport":
                    file.write(u"\n{}, {} ({}): {}. {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["year"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["institution"]))
                # unpublished
                elif key_type_dict[tuple[1]].lower() == "unpublished":
                    file.write(u"\n{}, {}: {}. {}.".format(
                               data[tuple[1]]["author"]["surname"],
                               data[tuple[1]]["author"]["forename"],
                               data[tuple[1]]["title"],
                               data[tuple[1]]["note"]))
            file.write(signature.format(date.fromtimestamp(time.time())))
        print("Output successfully created.\n"
              "----------------------------")


def pipe():
    """Combine all methods of BibTeX()."""
    example = BibTeX()
    key_not_in_txt = example.check_all_keys()
    example.check_all_types()
    basis_dict = example.bib_to_dict(key_not_in_txt)
    key_type_dict = example.check_required_fields(basis_dict)
    example.transfer(basis_dict)
    example.bibliography(basis_dict, key_type_dict)


def run():
    """Run combined methods of BibTeX() as final program."""
    state = True
    while state is True:
        try:
            pipe()
            state = False
        except AttributeError:
            close = input("Close program (y/[n])? ")
            if close == "y":
                sys.exit()


if __name__ == '__main__':
    # code below is only executed when the module is run directly
    run()
