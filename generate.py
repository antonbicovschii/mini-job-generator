import importlib.util
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent

env = Environment(
    loader=FileSystemLoader(ROOT / "templates"),
    undefined=StrictUndefined,      # забыли параметр -> ошибка, а не пустое место
    keep_trailing_newline=True,
)
env.globals["now"] = lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def load_params(path: Path):
    """Загружает parameters.py и возвращает класс JobParameters."""
    spec = importlib.util.spec_from_file_location("parameters", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.JobParameters


def render_job(job_dir: Path) -> str:
    params = load_params(job_dir / "parameters.py")
    template = env.get_template(f"{params.template}.jinja2")
    return template.render(job=params, job_name=job_dir.name)


def generate(job_dir: Path, out_dir: Path) -> Path:
    code = render_job(job_dir)
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{job_dir.name}.py"
    out_file.write_text(code, encoding="utf-8")
    return out_file


def main():
    for job_dir in sorted((ROOT / "jobs").iterdir()):
        if (job_dir / "parameters.py").exists():
            print("generated:", generate(job_dir, ROOT / "out"))


if __name__ == "__main__":
    main()
