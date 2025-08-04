from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path
from typing import Tuple, List


class AnswerSheetGenerator:
    def __init__(self):
        self.width, self.height = A4
        self.line_height = 18
        self.circle_radius = 6
        self.bubble_spacing = 20
        self.start_y = self.height - 110

    def _setup_page(self, c: canvas.Canvas, num_questions: int) -> None:
        """Setup the page with title and header."""
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, self.height - 50,
                     f"Cartão-Resposta – {num_questions} Questões (A, B, C, D)")
        c.setFont("Helvetica", 12)
        c.drawString(50, self.height - 80,
                     "Nome: ____________________________________________")
        c.drawString(400, self.height - 80, "Data: ___/___/______")

    def _get_column_positions(self, num_columns: int) -> List[int]:
        """Calculate x-positions for columns based on number of columns."""
        if num_columns == 4:
            return [50, 180, 310, 440]
        return [50, 220, 390]  # 3 columns

    def _draw_question(self, c: canvas.Canvas, x: int, y: int,
                       number: int) -> None:
        """Draw a single question with its bubbles."""
        c.setFont("Helvetica", 10)
        c.drawString(x, y, f"{number:02}")
        for i, letter in enumerate("ABCD"):
            cx = x + 25 + i * self.bubble_spacing
            cy = y + 4
            c.circle(cx, cy, self.circle_radius, stroke=1, fill=0)
            c.drawCentredString(cx, cy - 3, letter)

    def generate(self, output_path: str, num_questions: int,
                 num_columns: int) -> None:
        """Generate an answer sheet PDF with specified configuration."""
        output_path = Path(output_path)
        c = canvas.Canvas(str(output_path), pagesize=A4)

        self._setup_page(c, num_questions)
        column_x = self._get_column_positions(num_columns)

        questions_per_column = -(-num_questions // num_columns)  # Ceiling division

        for i in range(questions_per_column):
            y = self.start_y - i * self.line_height
            for col in range(num_columns):
                question_num = i + (col * questions_per_column) + 1
                if question_num <= num_questions:
                    self._draw_question(c, column_x[col], y, question_num)

        c.save()
        return output_path

    def generate_all(self, output_dir: str = ".") -> List[Path]:
        """Generate all three standard answer sheet variants."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        configurations = [
            ("Cartao_Resposta_100.pdf", 100, 4),
            ("Cartao_Resposta_120.pdf", 120, 4),
            ("Cartao_Resposta_75.pdf", 75, 3)
        ]

        generated_files = []
        for filename, num_questions, num_columns in configurations:
            output_path = output_dir / filename
            self.generate(output_path, num_questions, num_columns)
            generated_files.append(output_path)

        return generated_files


if __name__ == "__main__":
    generator = AnswerSheetGenerator()
    generator.generate_all()
