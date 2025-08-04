import pytest
from pathlib import Path
from src.answer_sheet_generator.generator import AnswerSheetGenerator


@pytest.fixture
def generator():
    return AnswerSheetGenerator()


def test_generate_single_sheet(generator, tmp_path):
    output_path = tmp_path / "test_100.pdf"
    generator.generate(output_path, 100, 4)
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_generate_all_sheets(generator, tmp_path):
    generated_files = generator.generate_all(tmp_path)
    assert len(generated_files) == 3
    for file_path in generated_files:
        assert file_path.exists()
        assert file_path.stat().st_size > 0


@pytest.mark.parametrize("num_questions,num_columns", [
    (100, 4),
    (120, 4),
    (75, 3),
])
def test_different_configurations(generator, tmp_path, num_questions, num_columns):
    output_path = tmp_path / f"test_{num_questions}_{num_columns}.pdf"
    generator.generate(output_path, num_questions, num_columns)
    assert output_path.exists()
    assert output_path.stat().st_size > 0
