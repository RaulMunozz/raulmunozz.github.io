# Portfolio — Raúl Muñoz López

A simple static page that lists six projects. No frameworks, no build step.

## View it

Double-click `index.html`, or serve the folder:

```powershell
cd "C:\Users\raul3\OneDrive\Documentos\Default Project\portfolio"
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Edit it

- `index.html` — all text and links (served at the site root).
- `portfolio/index.html` — the same page served at `/portfolio/`, with relative asset paths.
- `CV.pdf` — the downloadable CV linked from the hero and contact section.
- `styles.css` — layout and colours.
- `script.js` — only sets the footer year.

Keep `index.html` and `portfolio/index.html` in sync when editing copy; only their asset/CV paths differ.

## Project links

All six projects have public repositories:

- https://github.com/RaulMunozz/asteroid-destroyer
- https://github.com/RaulMunozz/autoescuela-demo
- https://github.com/RaulMunozz/ray-tracer-cpp
- https://github.com/RaulMunozz/flask-reservas
- https://github.com/RaulMunozz/student-performance-analysis
- https://github.com/RaulMunozz/employee-task-manager

## Publish with GitHub Pages

```powershell
git init
git add .
git commit -m "Portfolio"
git branch -M main
git remote add origin https://github.com/RaulMunozz/<repo-name>.git
git push -u origin main
```

Then in the repo: **Settings → Pages → Source: Deploy from a branch → main / root**.
