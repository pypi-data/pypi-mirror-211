"""Outline prompt setup and placeholders."""


CHANGE_FILE = """Apply the following change to the file contents:

${prompt}

Please only return the resulting code of the entire file with the
specified changes applied. If appropriate, you may also return it
with code comments to the new changes.

File contents:

${file_contents}
"""


EXPLAIN_FILE = """Explain the contents of the following file.
Return the answer in only markdown format.

File contents:

${file_contents}
"""


FIX_FILE = """Give the following file contents, please fix
what is wrong with the code.

Please only return the resulting code of the entire file with the
specified changes applied. If appropriate, you may also return it
with code comments to the new changes.

File contents:

${file_contents}
"""


UNIT_TEST_FILE = """Give the following file contents, please only
return the unit test code for this code. Use the appropriate unit
test framework for the language.

Please only return the resulting code. If appropriate, you may
also return it with code comments to the new changes.

File contents:

${file_contents}
"""
