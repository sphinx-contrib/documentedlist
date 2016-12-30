# -*- coding: utf-8 -*-

# Copyright (c) 2015, Chintalagiri Shashank
#
# This Sphinx Extension is made available under the BSD 2-clause License. See
# sphinxcontrib's LICENSE file for the full text.

import shlex
from six import text_type
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table


class DocumentedListDirective(Table):

    option_spec = {'listobject': directives.unchanged,
                   'header': directives.unchanged,
                   'spantolast': directives.unchanged,
                   'descend': directives.flag}

    def __init__(self, *args, **kwargs):
        super(DocumentedListDirective, self).__init__(*args, **kwargs)
        self.descend = None
        self.spantolast = None
        self.headers = None
        self.max_cols = None
        self.col_widths = None

    def run(self):
        if self.content:
            error = self.state_machine.reporter.error(
                """The DocumentedList directive does not know what to do with
                provided content""",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]

        # Get the list containing the documentation
        memberpath = self.options.get('listobject', None)
        if memberpath is None:
            error = self.state_machine.reporter.error(
                "DocumentedList needs to be given the list object"
                "containing the documentations as the :listobject: parameter",
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]

        try:
            modstr, memberstr = memberpath.rsplit('.', 1)
            mod = __import__(modstr, fromlist=[memberstr])
            member = getattr(mod, memberstr)
        except ImportError:
            error = self.state_machine.reporter.error(
                "DocumentedList encountered an error importing the member "
                "specified by " + memberpath,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno
            )
            return [error]

        self.descend = 'descend' in self.options
        self.spantolast = 'spantolast' in self.options
        self.headers = shlex.split(self.options.get('header', 'Item Description'))
        self.max_cols = len(self.headers)

        # This works around am apparantly poorly documented change in docutils
        # v13.1. I _think_ this should work with both versions, but please file
        # a bug on github if it doesn't.
        rval = self.get_column_widths(self.max_cols)
        if len(rval) == 2 and isinstance(rval[1], list):
            self.col_widths = rval[1]
        else:
            self.col_widths = rval

        table_body = member
        title, messages = self.make_title()
        table_node = self.build_table(table_body)
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    def get_rows(self, table_data):
        rows = []
        groups = []
        for row in table_data:
            sub_table_data = None
            if self.descend:
                for elem in row:
                    if isinstance(elem, list):
                        sub_table_data = row.pop(row.index(elem))
                        break
            trow = nodes.row()
            ncols = len(row)
            for idx, cell in enumerate(row):
                if self.spantolast and \
                        ncols < self.max_cols and idx == ncols - 1:
                    morecols = self.max_cols - ncols
                    entry = nodes.entry(morecols=morecols)
                else:
                    entry = nodes.entry()
                para = nodes.paragraph(text=text_type(cell))
                entry += para
                trow += entry
            if self.descend and sub_table_data:
                subtgroup = nodes.tgroup(cols=len(self.headers))
                subtgroup.extend(
                    nodes.colspec(
                        colwidth=col_width, colname='c' + str(idx)
                    ) for idx, col_width in enumerate(self.col_widths)
                )
                subthead = nodes.thead()
                subtgroup += subthead
                subthead += trow
                subtbody = nodes.tbody()
                subtgroup += subtbody
                sub_rows, sub_groups = self.get_rows(sub_table_data)
                subtbody.extend(sub_rows)
                groups.append(subtgroup)
                groups.extend(sub_groups)
            else:
                rows.append(trow)
        return rows, groups

    def build_table(self, table_data):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(self.headers))
        table += tgroup

        tgroup.extend(
            nodes.colspec(colwidth=col_width, colname='c' + str(idx))
            for idx, col_width in enumerate(self.col_widths)
        )

        thead = nodes.thead()
        tgroup += thead

        row_node = nodes.row()
        thead += row_node
        row_node.extend(nodes.entry(h, nodes.paragraph(text=h))
                        for h in self.headers)

        tbody = nodes.tbody()
        tgroup += tbody

        rows, groups = self.get_rows(table_data)
        tbody.extend(rows)
        table.extend(groups)

        return table


def setup(app):
    app.add_directive('documentedlist', DocumentedListDirective)
    return {'version': '0.4'}
