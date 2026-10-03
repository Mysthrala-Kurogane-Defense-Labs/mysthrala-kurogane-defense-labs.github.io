# MKDL corporate website

Static Spanish service and contact pages for **Mysthrala Kurogane Defense
Labs**, published at [mkdl.jp](https://mkdl.jp/) through GitHub Pages. This
repository contains the corporate site, not the private Kurogane Hub
application.

## Readers

- Companies: [services and scope](https://mkdl.jp/#trabajo),
  [info@mkdl.jp](mailto:info@mkdl.jp).
- Technical teams: [public repository
  map](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane), [practical
  guides](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-docs),
  [synthetic
  labs](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-labs).
- Sensitive reports: [security.txt](.well-known/security.txt), [private
  disclosure
  route](https://github.com/Mysthrala-Kurogane-Defense-Labs/kurogane-security-model/blob/main/disclosure-policy.md).

MKDL's public focus is bounded industrial cybersecurity work for small
businesses in Bajo Deba / Euskadi. Hub availability, deployment capabilities and
commercial conditions need separate evidence and agreement; public examples do
not establish production readiness.

## Edit and preview

Requires Python >= 3.11 for the local static server:

```sh
python -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080`. Check desktop and narrow layouts, navigation,
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
