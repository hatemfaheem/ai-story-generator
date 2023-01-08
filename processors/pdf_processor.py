import os

from fpdf import FPDF

from data_models import Story


class PdfProcessor:
    _FILENAME: str = "final_story.pdf"
    _FORMAT: str = "A5"
    _ORIENTATION: str = "L"
    _SAVE_TO_LOCAL_FILE: str = "F"

    def create_pdf(self, workdir: str, story: Story) -> str:
        """Create PDF for the given story."""

        pdf = FPDF(orientation=self._ORIENTATION, format=self._FORMAT)
        pdf_filepath = os.path.join(workdir, self._FILENAME)
        for page in story.pages:
            pdf.add_page()
            pdf.image(page.page_filepath)
        pdf.output(pdf_filepath, self._SAVE_TO_LOCAL_FILE)
        return pdf_filepath
