# Polymarket AI Lab

Hugo-powered static site for daily Polymarket/NBA experiment logs and automation:
- Content: `content/posts/` (daily logs), `content/notes/` (guides)
- Deployment: GitHub Actions builds Hugo and publishes to `gh-pages` for GitHub Pages
- Automation: n8n pulls Google Sheets, computes metrics, generates Markdown via Perplexity, writes to GitHub via REST API

## Quick start

1. Install Hugo and clone/pull this repo
2. Run `hugo server -D` locally
3. Push to `main` to trigger Actions deployment to `gh-pages`

## n8n & GitHub API

Use PUT `/repos/{owner}/{repo}/contents/{path}` with Base64 markdown content to add posts under `content/posts/`.
See `static/samples/` for prompt and templates.