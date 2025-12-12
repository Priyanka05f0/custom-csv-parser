"""
custom_csv.py

Simple custom CSV reader and writer implemented from scratch
(without using Python's built-in csv module for parsing/writing).

Classes
-------
CustomCsvReader  - iterator over rows in a CSV file
CustomCsvWriter  - writes lists of rows to a CSV file
"""


class CustomCsvReader:
    """
    A simple CSV reader that parses comma-separated files.

    Features
    --------
    - Handles fields enclosed in double quotes.
    - Handles escaped quotes inside fields ("" -> ").
    - Supports newlines inside quoted fields.
    - Returns each row as a list of strings.
    - Works as an iterator: for row in CustomCsvReader(file_obj): ...
    """

    def __init__(self, file_obj, delimiter=",", quotechar='"'):
        """
        Parameters
        ----------
        file_obj : file object
            An already opened file object in text mode, e.g.
            open("data.csv", "r", encoding="utf-8")
        delimiter : str
            Character that separates fields (default: comma).
        quotechar : str
            Character used to quote fields (default: double quote).
        """
        self.file = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self._buffer = ""  # for one-character pushback
        self._eof = False

    def __iter__(self):
        return self

    def _read_char(self):
        """Return the next character from buffer or file."""
        if self._buffer:
            ch = self._buffer
            self._buffer = ""
            return ch
        return self.file.read(1)

    def _unread_char(self, ch):
        """Push a single character back into the buffer."""
        self._buffer = ch

    def __next__(self):
        """
        Read and parse the next row from the CSV file.

        Returns
        -------
        list[str]
            The next row as a list of string fields.

        Raises
        ------
        StopIteration
            When no more data is available.
        """
        if self._eof:
            raise StopIteration

        row = []
        field_chars = []
        in_quotes = False

        while True:
            ch = self._read_char()

            # End of file
            if ch == "":
                self._eof = True

                # If we collected something, return the last row
                if field_chars or row:
                    row.append("".join(field_chars))
                    return row
                raise StopIteration

            if ch == self.quotechar:
                if in_quotes:
                    # Could be end of quoted field or an escaped quote
                    next_ch = self._read_char()
                    if next_ch == self.quotechar:
                        # Escaped quote ("")
                        field_chars.append(self.quotechar)
                    else:
                        # End of quoted field; push back the char we read
                        in_quotes = False
                        self._unread_char(next_ch)
                else:
                    # Start of quoted field
                    in_quotes = True

            elif ch == self.delimiter and not in_quotes:
                # End of field
                row.append("".join(field_chars))
                field_chars = []

            elif ch in ("\n", "\r") and not in_quotes:
                # End of row
                if ch == "\r":
                    next_ch = self._read_char()
                    if next_ch not in ("\n", ""):
                        self._unread_char(next_ch)

                row.append("".join(field_chars))
                return row

            else:
                # Normal character (including delimiter/newline inside quotes)
                field_chars.append(ch)


class CustomCsvWriter:
    """
    A simple CSV writer that writes rows to a file.

    Features
    --------
    - Takes rows as lists of values (converted to strings).
    - Quotes fields that contain comma, double quote, or newline.
    - Escapes internal double quotes by doubling them.
    """

    def __init__(self, file_obj, delimiter=",", quotechar='"', line_terminator="\n"):
        """
        Parameters
        ----------
        file_obj : file object
            An already opened file object in text mode, e.g.
            open("output.csv", "w", encoding="utf-8", newline="")
        delimiter : str
            Character that separates fields (default: comma).
        quotechar : str
            Character used to quote fields (default: double quote).
        line_terminator : str
            String appended at the end of each row (default: "\n").
        """
        self.file = file_obj
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.line_terminator = line_terminator

    def _quote_field(self, value):
        """Return a correctly escaped/quoted field as a string."""
        text = "" if value is None else str(value)
        must_quote = (
            self.delimiter in text
            or self.quotechar in text
            or "\n" in text
            or "\r" in text
        )

        if must_quote:
            escaped = text.replace(self.quotechar, self.quotechar * 2)
            return f"{self.quotechar}{escaped}{self.quotechar}"
        return text

    def writerow(self, row):
        """Write a single row (list or tuple of values) to the file."""
        parts = [self._quote_field(value) for value in row]
        line = self.delimiter.join(parts) + self.line_terminator
        self.file.write(line)

    def writerows(self, rows):
        """Write multiple rows (iterable of lists/tuples) to the file."""
        for row in rows:
            self.writerow(row)

    # Backward-compatible aliases (do not remove — safe to keep)
    def write_row(self, row):
        """Backward compatibility: old method name calls writerow."""
        return self.writerow(row)

    def write_rows(self, rows):
        """Backward compatibility: old method name calls writerows."""
        return self.writerows(rows)
