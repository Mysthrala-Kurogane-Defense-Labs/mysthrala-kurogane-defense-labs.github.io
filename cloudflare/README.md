# Prepare the static website for Cloudflare

GitHub Pages is the current production host. This repository also prepares a
Workers Static Assets deployment called `mkdl-web`, with no Worker script,
framework, database or application dependencies. The Wrangler configuration has
no production routes or custom domains.

## Export and local preview

Use Python 3.11+ to export either target. Both use the same public-file allowlist
and link/fragment checks; each command recreates only its generated directory:

```sh
python3 scripts/package-site.py --target github
python3 scripts/package-site.py --target cloudflare
```

GitHub output is `_site/`. Cloudflare output is `_site-cloudflare/`, with the
additional `_headers` and `_redirects` configuration. Keep those files out of
the GitHub Pages artifact. Never store hand-authored files in the two generated
directories.

For a local Workers preview, use Node.js 22+ and the tested Wrangler version:

```sh
npm exec --yes --package=wrangler@4.147.0 -- wrangler dev --local --ip 127.0.0.1 --port 8787
```

Open `http://127.0.0.1:8787/`. This command starts a local runtime; it does not
publish a Worker. Stop it with Ctrl+C. Node and npm are deployment tooling only;
the website itself remains static HTML and CSS.

Before a remote deployment, check `/`, the four legal `.html` pages, CSS and
images, `/robots.txt`, `/sitemap.xml`, `/security.txt` and
`/.well-known/security.txt`. Both exported security files must match. If the
Cloudflare security.txt feature also serves this path after the domain cutover,
check its contact, canonical URL and expiry separately. Check that
`/index.html?x=1` redirects once to `/?x=1`, that `/privacidad` redirects to
`/privacidad.html`, and that an unknown path returns the custom `404.html` with
HTTP status 404. Confirm the security headers on served files.

`html_handling: "none"` preserves the existing `.html` canonical URLs. The
`/ /index.html 200` rule serves the root page without changing the browser URL;
Workers applies one proxy rule, so the `/index.html / 301` rule does not create
a loop. These behaviors were checked locally with Wrangler 4.147.0. The
`workers.dev` header rule discourages search indexing of remote preview hosts.

## First remote deployment

The first remote deployment is a separate action. Authenticate Wrangler to the
intended Cloudflare account and verify the account and `mkdl-web` name first.
Create the account's `workers.dev` subdomain if it does not yet exist. After
exporting the Cloudflare target, an authorized operator can deploy with:

```sh
npm exec --yes --package=wrangler@4.147.0 -- wrangler deploy
```

Validate the resulting `workers.dev` URL before adding a custom domain. A local
preview does not verify Cloudflare account permissions, certificates, edge rules
or production DNS.

For Git-based deployments, first authorize the Cloudflare GitHub App for the
MKDL organization and this repository. Configure Workers Builds as follows:

| Setting | Value |
| --- | --- |
| Worker name | `mkdl-web` |
| Repository root | `/` |
| Production branch | `main` |
| Build command | `python3 scripts/package-site.py --target cloudflare` |
| Deploy command | `npm exec --yes --package=wrangler@4.147.0 -- wrangler deploy` |
| Preview command | `npm exec --yes --package=wrangler@4.147.0 -- wrangler preview` |
| Static assets directory | `_site-cloudflare`, from `wrangler.jsonc` |

The existing GitHub Actions workflow validates both exports and still deploys
only GitHub Pages. It contains no Cloudflare credentials or deployment step.

## Domain cutover and rollback

1. Export the current apex/www DNS records and record the active GitHub Pages
   configuration. Keep the GitHub deployment and verification TXT available.
2. Verify the populated Worker on its temporary URL, including the HTTP checks
   above. Record its deployment/version identifier.
3. When performing the hosting cutover, associate the exact hostname `mkdl.jp`
   using a Workers Custom Domain. Plan `www.mkdl.jp` separately: its existing
   CNAME must be handled before a Custom Domain can use that hostname. Transfer
   the www-to-apex redirect to Cloudflare and preserve paths and query strings.
4. Check both public hostnames and certificate status, then retire only the
   GitHub web-origin records that have been replaced. Leave mail, verification
   records, Hub/API and every other Tunnel hostname intact.
5. Keep the previous GitHub hosting arrangement available until the new service
   has been checked. A cutover is not complete merely because a build succeeded.

For an application-version regression, use Workers' deployment rollback to the
previous verified version. Returning hosting to GitHub is a different rollback:
restore the saved DNS and domain associations and remove the Workers association
for the affected hostname. Recheck the site after either operation. DNS changes
can be cached; do not promise an instantaneous hosting rollback.

## References

- [Static assets and routing](https://developers.cloudflare.com/workers/static-assets/)
- [HTML handling](https://developers.cloudflare.com/workers/static-assets/routing/advanced/html-handling/)
- [Redirects and proxying](https://developers.cloudflare.com/workers/static-assets/redirects/)
- [Workers Builds configuration](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/)
- [GitHub App prerequisite](https://developers.cloudflare.com/workers/ci-cd/builds/api-reference/)
- [Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [Rollbacks](https://developers.cloudflare.com/workers/versions-and-deployments/rollbacks/)
