# ERA-Engine Documents

Document website for ERA‑Engine.

ERA‑Engine 的文档网站存储库。

## Project Detail

ERA‑Engine: [GitHub Repository](https://github.com/Zhen-LinHuo/ERA-Engine)

*The project repository is currently private, so you might not able to visit.
It will be public after its first release.*

*该存储库目前为私有，在第一次发布 release 后将会公开。*

### Contributors

- [Zhen‑LinHuo](https://github.com/Zhen-LinHuo)

## How to Contribute

This project uses **MkDocs** with the **Material for MkDocs** theme,
deployed via **GitHub Pages** with **GitHub Actions**.

本项目使用 **MkDocs** + **Material for MkDocs** 主题编写，通过 **GitHub Actions** 自动部署到 **GitHub Pages**。

### Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) (recommended — single command, no venv needed)

### Preview Locally

Clone the repo and run:

```bash
# Install uv if needed: curl -LsSf https://astral.sh/uv/install.sh | sh
uvx --with mkdocs-material mkdocs serve
```

Open `http://127.0.0.1:8000` in your browser. The server auto‑reloads when
you edit any source file.

### Editing

All documentation source files live under the `docs/` directory.
Write in **Markdown** — no special tooling required.

| Section | Path | Description |
|:--------|:-----|:------------|
| Introduction | `docs/introduction/` | Project overview and core concepts |
| Guide | `docs/guide/` | Architecture, data system, view system |
| Tutorial | `docs/tutorial/` | Step‑by‑step walkthrough |
| Advanced | `docs/advanced/` | Debugging, save/load, Kojo format, custom UI |
| API Reference | `docs/api/` | Auto‑generated from C# XML doc comments |
| Project | `docs/project/` | Roadmap, release notes, credits |

### API Documentation

API pages are generated from XML doc comments in the ERA‑Engine source code.
To regenerate:

```bash
# Point to your local ERA‑Engine checkout
uv run python3 scripts/gen_api_docs.py /path/to/ERA-Engine docs/api
```

The script is designed to track the `main` branch of the ERA‑Engine repository.

### Build & Commit

For significant changes, preview locally first:

```bash
uvx --with mkdocs-material mkdocs build
# Check the output in site/
```

Then commit your changes and open a pull request.
**GitHub Actions** will automatically build and deploy the site to
**GitHub Pages** from the `main` branch.

## Tech Stack

- **Framework**: [MkDocs](https://www.mkdocs.org/)
- **Theme**: [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- **CI/CD**: GitHub Actions
- **API doc generation**: Custom Python script (`scripts/gen_api_docs.py`)
