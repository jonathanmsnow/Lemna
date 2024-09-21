class Plate:
    def __init__(self, label, rows, cols, wells):
        self.label = label
        self.rows = rows
        self.cols = cols
        self.wells = wells

    def well_count(self):
        return self.rows * self.cols
    
    def get_well_label(self, index):
        well_row = index // self.cols
        well_col = index % self.cols   
        label = f"{chr(65 + well_col)}{well_row + 1}"
        return label