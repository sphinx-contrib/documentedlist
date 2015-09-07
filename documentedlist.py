# -*- coding: utf-8 -*-

# Copyright (c) 2015, Chintalagiri Shashank
#
# This Sphinx Extension is made available under the BSD 2-clause License. See
# sphinxcontrib's LICENSE file for the full text.

import shlex
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import Table


class DocumentedListDirective(Table):

    option_spec = {'listobject': directives.unchanged,
                   'header': directives.unchanged}

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

        table_headers = shlex.split(self.options.get('header', 'Item Description'))
        table_body = member
        max_cols = len(table_headers)

        col_widths = self.get_column_widths(max_cols)

        title, messages = self.make_title()
        table_node = self.build_table(table_body,
                                      col_widths,
                                      table_headers)
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [table_node] + messages

    @staticmethod
    def build_table(table_data, col_widths, headers):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(headers))
        table += tgroup

        tgroup.extend(nodes.colspec(colwidth=col_width) for
                      col_width in col_widths)

        thead = nodes.thead()
        tgroup += thead

        row_node = nodes.row()
        thead += row_node
        row_node.extend(nodes.entry(h, nodes.paragraph(text=h))
                        for h in headers)

        tbody = nodes.tbody()
        tgroup += tbody

        rows = []
        for row in table_data:
            trow = nodes.row()
            for cell in row:
                entry = nodes.entry()
                para = nodes.paragraph(text=unicode(cell))
                entry += para
                trow += entry
            rows.append(trow)
        tbody.extend(rows)

        return table


def setup(app):
    app.add_directive('documentedlist', DocumentedListDirective)
    return {'version': '0.1'}
