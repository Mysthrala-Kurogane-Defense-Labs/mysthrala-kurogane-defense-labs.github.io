# MKDL corporate website

Static Spanish service and contact pages for **Mysthrala Kurogane Defense
Labs**, published at [mkdl.jp](https://mkdl.jp/) through GitHub Pages. This
repository contains the corporate site, not the private Kurogane Hub
application.

## Readers

- Companies: [services and scope](https://mkdl.jp/#servicio),
  [mysthrala@mkdl.jp](mailto:mysthrala@mkdl.jp).
- Technical teams: [public repository
  map](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane), [practical
  guides](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-docs),
  [synthetic
  labs](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-labs).
- Sensitive reports: [security.txt](.well-known/security.txt), [private
  disclosure
  route](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-security-model/blob/main/disclosure-policy.md).

OT Check reviews one bounded industrial process and its decision centre to prepare priorities, proposed owners and checks for commissioning improvements. It serves small, medium and large industrial organisations or group units, from an operational base in Euskadi. Scope, depth, evidence, calendar and price are agreed in a proposal. No firm tariff is published.

MKDL presents consultancy, documentation and training by one professional. It does not offer Hub distribution, implementation, operations, incident response, permanent support or integration by default. The activity is presented as being prepared; no registration, insurance or professional certification is asserted as verified.

The three situations preserve the recovered public prototype. The linked HTML/PDF, editable CSV and evidence bundle are wholly synthetic. They demonstrate the structure of a deliverable, not client work, recovery performance or external acceptance. Both the report and its five evidence sheets are readable without opening raw JSON. The offline ZIP contains the report, PDF, CSV and local assets, with no external dependencies.

Regenerate the sample with `python3 scripts/build-sample.py` using the authoring dependency `reportlab`. Its content model produces the HTML, PDF, editable plan and offline package together. The original synthetic source files remain in `assets/muestra-ot-check-evidencias/`; they are source material, not the buyer's reading interface. `assets/mkdl-logo-print.png` is a render of the unchanged original SVG for the PDF header. This authoring tool adds no dependency to the website runtime or publishing workflow.

## Edit and preview

Requires Python >= 3.11 for the local static server:

```sh
py -3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080`. On Linux use `python3` in place of `py -3`. Check desktop and narrow layouts, navigation,
contact links and each legal page. Stop the server with Ctrl+C. There is no
application build or package install. Keep `CNAME`, canonical URLs,
`sitemap.xml`, `robots.txt`, social metadata and `llms.txt` consistent with the
intended public domain.

## Structure and publication

- `index.html`, `assets/`: public landing and local visual assets.
- Legal, privacy, cookies and accessibility HTML pages: public notices requiring
  owner review.
- `.well-known/security.txt` and `security.txt`: keep the security contact and
  expiry synchronized.
- `CNAME` / `_config.yml`: current GitHub Pages configuration.

A local HTML edit, reviewed commit, successful Pages build and live publication
are separate gates. The GitHub Pages workflow packages the site with
`python3 scripts/package-site.py --target github` and publishes `_site`.
It also validates the separate Cloudflare export on pushes and pull requests.

The [Cloudflare preparation guide](cloudflare/README.md) describes local preview,
first deployment and a later hosting cutover. GitHub Pages remains the production
host until a Cloudflare deployment is verified and the custom domains are moved.

## Evidence boundaries

The source has no custom forms, analytics code or browser-storage functions.
That does not establish the configuration of hosting, CDN, protection services
or mail providers. Legal identity, lawful basis, retention, processors and
transfer details must be validated by the owner against actual operations; do
not fill them from guessed values or marketing copy.

Use synthetic material in issues. Documentation and visual content retain the
terms in [LICENSE](LICENSE).

## Local review and publication boundary

Both required packaging targets must pass from the final revision:

```sh
python3 scripts/package-site.py --target github
python3 scripts/package-site.py --target cloudflare
```

The allowlist includes the HTML sample, security policy and favicon; `assets/` contains the PDF, editable synthetic matrix, JSON evidence manifest and offline bundle. The landing uses the original brand stylesheet `assets/site.css`, with content additions in `assets/ot-check.css`. The report uses `assets/commercial.css` with the original brand palette. Legal pages use `assets/legal.css`.

No publication is authorised by this branch. Before any push, PR, deployment or domain change, obtain the separate authority, confirm professional/legal details and provider operations, review the synthetic sample, and run the required remote checks. The existing GitHub workflow remains restricted to main for publication; this change adds no deployment mechanism.
