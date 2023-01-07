import os

from fpdf import FPDF

from data_models import Story


class PdfProcessor:
	FILENAME: str = "final_story.pdf"

	def create_pdf(self, workdir: str, story: Story) -> str:
		"""
		Create PDF for the given story.
		"""
		pdf = FPDF(orientation="L", format="A5")
		pdf_file = os.path.join(workdir, self.FILENAME)
		for page in story.pages:
			pdf.add_page()
			pdf.image(page.page_filepath)
		pdf.output(pdf_file, "F")
		return pdf_file
