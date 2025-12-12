from custom_csv import CustomCsvWriter as _Original

class CustomCsvWriter(_Original):
    """
    Compatibility wrapper so tests expecting writerow() / writerows()
    work even if original class used different method names.
    """

    def writerow(self, row):
        # try parent implementation first
        try:
            return super().writerow(row)
        except AttributeError:
            pass

        # fallbacks checking class or instance methods
        if hasattr(self, "write_row"):
            return self.write_row(row)
        if hasattr(self, "write_rows"):
            return self.write_rows([row])
        raise AttributeError("No writerow or write_row found in original class")

    def writerows(self, rows):
        # try parent implementation first
        try:
            return super().writerows(rows)
        except AttributeError:
            pass

        if hasattr(self, "write_rows"):
            return self.write_rows(rows)
        if hasattr(self, "write_row"):
            for r in rows:
                self.write_row(r)
            return
        raise AttributeError("No writerows or write_rows found in original class")
