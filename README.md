# CenterPoint Association Management website

Static site for centerpointmgmt.com.

- `_build/build.py` generates every page into `dist/` from the content in `_build/source/`.
- `assets/` holds shared CSS, JS, logo and photos (copied into `dist/assets` on build).
- Deployed on Vercel as a static site from `dist/` (see `vercel.json`).

Rebuild after editing content or templates:

```
python _build/build.py
python _build/audit.py
```

Building photos: Warren LeMay and mindfrieze, CC BY-SA, via Wikimedia Commons.
