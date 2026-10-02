# MKDL · Public website

Static corporate website for **Mysthrala Kurogane Defense Labs**, published at **[mkdl.jp](https://mkdl.jp/)** through GitHub Pages.

MKDL focuses on practical industrial cybersecurity for small industrial companies and micro-SMEs in Bajo Deba / Euskadi: scoped diagnosis, technical and documentary organization, evidence preparation, and agreed follow-up. Kurogane Hub supports this work.

## Where to start

- **Services and scope:** [mkdl.jp/#trabajo](https://mkdl.jp/#trabajo).
- **Consulting enquiries:** [info@mkdl.jp](mailto:info@mkdl.jp).
- **Public technical ecosystem:** [Kurogane](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane).
- **Organization and repository map:** [MKDL on GitHub](https://github.com/Mysthrala-Kurogane-Defense-Labs).

## Repository contents

- `index.html`: corporate landing page.
- `assets/`: logo, stylesheet and website assets.
- Legal, privacy, cookie and accessibility pages.
- `security.txt` and `.well-known/`: security contact information.
- `CNAME`: GitHub Pages custom domain configuration.

## Local preview

This is a static site with no application build step. From the repository directory, serve it locally with Python 3:

```sh
python -m http.server 4173 --bind 127.0.0.1
```

Open <http://127.0.0.1:4173/>. Stop the server with `Ctrl+C`.

For public website defects, use this repository's issues. For confidential enquiries or security reports, use the contact channel published on the website.
