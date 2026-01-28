from fpdf import FPDF
from fpdf.enums import XPos, YPos
    
class SizainePDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "Suivi des Points - Semaine d'Activités", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("Helvetica", "", 12)
        self.cell(0, 10, "Sizaine Blanche, Sizaine Rouge, Sizaine Bleue", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(5)

    def add_sizaine_table(self, sizaine_name):
        self.add_page()
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"{sizaine_name}",new_x=XPos.LMARGIN, new_y=YPos.NEXT
)
        self.ln(5)

        # En-têtes
        self.set_font("Helvetica", "B", 10)
        col_widths = [50, 25, 25, 25, 25, 25, 25]
        headers = ["Activité / Comportement", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Total"]

        for i, header in enumerate(headers):
            self.cell(col_widths[i], 10, header, border=1, align="C")
        self.ln()

        # Contenu
        self.set_font("Helvetica", "", 10)
        activities = [
            "Ponctualité",
            "Travail en équipe",
            "Esprit scout",
            "Aide aux autres",
            "Propreté / rangement",
            "Activités terminées",
            "Total journalier"
        ]

        for activity in activities:
            for i, width in enumerate(col_widths):
                if i == 0:
                    self.cell(width, 10, activity, border=1)
                else:
                    self.cell(width, 10, "", border=1)
            self.ln()

# Génération du PDF
pdf = SizainePDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

for sizaine in ["Sizaine Blanche", "Sizaine Rouge", "Sizaine Bleue"]:
    pdf.add_sizaine_table(sizaine)

pdf.output("Suivi_Points_Sizaines.pdf")
