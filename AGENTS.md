# Repository Guidelines

## Project Structure & Module Organization
- Entry point: `master_wizard.py` orchestrates setup flows.
- Scenario logic lives in `wizards/`; shared helpers in `tools/` (detectors, scanners, validators).
- Configuration templates are in `configs/`; documentation in `docs/` (English/Czech); tests reside in `tests/` with the current focus on `impossible_scenarios/`.
- Keep new data files and logs out of version control; the wizard writes `unification.log` at runtime.

## Setup, Build & Test Commands
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 master_wizard.py            # Run interactive setup
python -m unittest discover tests   # Full test suite
flake8                              # Lint (if installed)
```
- Prefer Python 3.8+; keep dependencies minimal (see `requirements.txt`).

## Coding Style & Naming Conventions
- Follow PEP 8, 4-space indentation, and type hints where practical (mirrors `master_wizard.py`).
- Use descriptive class/module names tied to scenarios (`WorkstationSetup`, `DependencyResolver`); new wizards go in `wizards/` and share utilities in `tools/`.
- Tests use `test_*.py` naming and `unittest.TestCase`; mirror module names for clarity.
- Log via `logging` instead of `print` for new runtime output.

## Testing Guidelines
- Framework: `unittest`; run with `python -m unittest discover tests`.
- Aim for the project’s stated goal of near-100% coverage, especially for error paths and “impossible” cases.
- Use temp dirs/mocks to avoid touching real `~/.ssh` or network state (see `tests/impossible_scenarios/test_ssh_chaos.py`).
- When adding scenarios, include regression tests that prove failures are handled gracefully rather than skipped.

## Commit & Pull Request Guidelines
- Commit style follows Conventional Commits seen in history (e.g., `fix(tests): correct mocking`, `chore: update git email configuration`); use a scope when it clarifies impact.
- Keep commits focused and documented; note repro steps and expected outcomes in the message or PR body.
- PRs should link relevant issues, summarize behavior changes, list test commands run, and attach screenshots/log snippets if user-visible output changes.

## Security & Configuration Tips
- Never commit real SSH keys, secrets, or machine-specific configs; treat `configs/` as templates.
- Validate network-affecting changes with mock/stubbed calls before touching live environments.
- Keep bilingual docs in sync (`docs/en` and `docs/cz`) when altering user flows.
