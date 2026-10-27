import ast
import pytest
from generate import ROOT, render_job

JOB_DIRS = [p.parent for p in (ROOT / "jobs").glob("*/parameters.py")]

@pytest.mark.parametrize("job_dir", JOB_DIRS, ids= lambda p: p.name)
def test_generated_code_is_valid_python(job_dir):
    code = render_job(job_dir)
    ast.parse(code)


def test_key_column_block_is_optional(tmp_path):
    job_dir = tmp_path / "p_no_key"
    job_dir.mkdir()
    (job_dir / "parameters.py").write_text(
        'class JobParameters:\n'
        '   template = "silver_batch"\n'
        '   source_table = "a.b"\n'
        '   sink_table = "c.d"\n'
    )
    code = render_job(job_dir)
    assert "row_number" not in code