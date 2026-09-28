# AirMouse Pro Website — SEO Ready

Responsive landing/documentation website for AirMouse Pro, prepared for GitHub Pages and Google Search.

## Recommended GitHub Pages URL

Create the repository with this exact name if you want to use the preconfigured canonical URL:

`https://github.com/manofrancis-dev/airmousepro`

The published site URL will be:

`https://manofrancis-dev.github.io/airmousepro/`

If you choose a different repository name or a custom domain, update the same site URL in:

- `index.html` — canonical, Open Graph, Twitter and JSON-LD URLs
- `sitemap.xml` — `<loc>`
- `robots.txt` — `Sitemap:`

## Run locally

Open `index.html` in a modern browser.

## GitHub Pages deployment

1. On GitHub, create a new repository named `airmousepro` under `manofrancis-dev`.
2. Upload the contents of this folder to the repository root. The repository should contain `index.html`, `robots.txt`, `sitemap.xml` and the `assets/` folder at the top level.
3. Open the repository's **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select the `main` branch and the `/ (root)` folder, then save.
6. Wait for GitHub Pages to publish the site.
7. Open `https://manofrancis-dev.github.io/airmousepro/` and verify the page.
8. In **Settings → Pages**, enable **Enforce HTTPS** when it is available.

## Replace the final download link

The website currently keeps the installer URL blank so it cannot point to a fake file.

In `index.html`, find:

`const DOWNLOAD_URL = "";`

Replace it with the real HTTPS URL to your `AirMousePro_Setup_v1.0.0.exe` file.

A GitHub Release is a practical option. Example format:

`https://github.com/manofrancis-dev/<YOUR-REPO>/releases/download/v1.0.0/AirMousePro_Setup_v1.0.0.exe`

Do not invent the URL; use the exact release asset URL GitHub provides.

## Replace GitHub / LinkedIn / portfolio links

The current footer uses:

- GitHub: `https://github.com/manofrancis-dev`
- LinkedIn: `https://in.linkedin.com/in/manofrancis-dev`
- Portfolio: `https://dev-portfolio-one-silk.vercel.app/`

Edit the corresponding `<a href="...">` values in `index.html` if you want different links.

## Google Search Console + indexing

1. Open Google Search Console and add the deployed site as a property.
2. Complete the ownership verification method Google gives you.
3. Use **URL Inspection** to inspect the full published homepage URL.
4. Run the live test and fix any indexability issue it reports.
5. Use **Request indexing** for the homepage.
6. Submit this sitemap:
   `https://manofrancis-dev.github.io/airmousepro/sitemap.xml`
7. Keep the site live and linked from other relevant public pages. Re-crawling is not instant.

Google says indexing can take a day or longer, and a request does not guarantee inclusion or a particular ranking position.

## SEO targeting used here

The page uses natural, relevant wording around:

- AirMouse Pro
- AirMousePro
- Windows hand gesture mouse
- hand gesture control
- gesture mouse
- mouse control with hand gestures
- Mano Francis

The page does **not** stuff unrelated keywords such as `anti theft` simply to manipulate rankings. Add that phrase only if the product actually provides a documented anti-theft feature.

## Important ranking note

No HTML change can guarantee that Google will rank this site #1 for broad searches such as `francis`, `gesture`, or `anti theft`. Google evaluates relevance, content quality, indexing, links, competition and many other signals. The strongest early targets are branded searches such as `AirMouse Pro`, `AirMousePro`, and `Mano Francis AirMouse Pro`.
