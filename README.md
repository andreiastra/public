---
layout: default
title: README
---

# Underwater Photography Resources

This repository contains comprehensive documentation and guides for underwater photography using OM System cameras.

## 🚀 Quick Start

This site is built with Jekyll and automatically deployed via GitHub Pages.

### Viewing the Site

Visit: [https://andreiastra.github.io/public/](https://andreiastra.github.io/public/)

### Local Development

To run the site locally:

1. Install Ruby and Bundler (if not already installed)
2. Navigate to the repository directory:
   ```bash
   cd /Users/astra/github/public
   ```

3. Install dependencies:
   ```bash
   bundle install
   ```

4. Run Jekyll locally:
   ```bash
   bundle exec jekyll serve
   ```

5. Open your browser to `http://localhost:4000/public/`

## 📁 Repository Structure

```
.
├── _config.yml                 # Jekyll configuration
├── _layouts/                   # Custom layouts
│   └── default.html           # Main layout template
├── index.md                    # Home page
├── underwater-photography/     # Main content directory
│   ├── aperture/              # Aperture settings & techniques
│   ├── competitions/          # Competition guides
│   ├── gems/                  # Tips & tricks
│   ├── info/                  # Equipment & settings
│   ├── manuals/               # PDF manuals
│   ├── overview-guides/       # Complete setup guides
│   ├── tele/                  # Telephoto lens guides
│   └── viewfinder/            # Viewfinder setup
├── Gemfile                     # Ruby dependencies
└── README.md                   # This file
```

## 📝 Adding New Content

### Adding a New Markdown File

1. Create a new `.md` file in the appropriate directory
2. Add front matter at the top:
   ```yaml
   ---
   layout: default
   title: Your Page Title
   ---
   ```
3. Write your content in Markdown
4. Commit and push to GitHub

### Adding a New Category

1. Create a new directory under `underwater-photography/`
2. Add your markdown files
3. Update `index.md` to include links to the new category

## 🎨 Customization

### Changing the Theme

Edit `_config.yml` to change the theme or modify `_layouts/default.html` for custom styling.

### Updating Site Information

Edit these fields in `_config.yml`:
- `title`: Site title
- `description`: Site description
- `baseurl`: Base URL path
- `url`: Full site URL

## 🔧 Jekyll Configuration

The site uses:
- **Markdown processor**: Kramdown with GitHub Flavored Markdown (GFM)
- **Syntax highlighter**: Rouge
- **Plugins**: jekyll-feed, jekyll-seo-tag

## 📦 Deployment

The site automatically deploys to GitHub Pages when you push to the main branch. GitHub Pages will:
1. Detect the Jekyll configuration
2. Build the site
3. Deploy to `https://andreiastra.github.io/public/`

## 🌊 Content Categories

- **Aperture Settings**: Master f-stops and depth of field
- **Competitions**: Photography competition guides
- **Tips & Gems**: Helpful tricks and diagnostic tools
- **Equipment Info**: Camera settings and gear lists
- **Manuals**: PDF equipment manuals
- **Setup Guides**: Complete underwater photography setup
- **Telephoto**: Telephoto lens guides
- **Viewfinder**: Viewfinder installation and setup

## 📄 License

Personal documentation repository.

---

*Last Updated: May 2026*
