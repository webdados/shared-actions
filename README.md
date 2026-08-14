# Webdados / Naked Cat Plugins shared GitHub actions

Shared GitHub Actions to use on several WordPress Free and Premium Plugins by Webdados / Naked Cat Plugins.

Although this repository is public (due to GitHub limitations), using these actions in 3rd-party projects is not recommended.



## Create Release Zip

Create a zip file for the GitHub release and for eventual upload to a server.

### Usage:

Assumes a `.distignore` file exists containing the files and folders to exclude.
If `env.SLUG` is set (which is recommended, as it's shared by several of our actions), `plugin-slug` and `zip-filename` are not required and will default to it (which should apply in most cases: the folder name and the main file are the same).

```yaml
name: Build release zip when pushing tag

on:
  push:
    tags:
    - '*'

permissions:
  contents: write  # needed to create releases and upload assets

env:
  SLUG: the-plugin-slug

jobs:
  build:
    name: Build release zip
    runs-on: ubuntu-latest
    steps:
    
    # Checkout the code from the repository
    - name: ⬇️ Checkout
      uses: actions/checkout@v4
    
    # Create the zip file excluding files and directories listed in .distignore
    - name: 📦 Zip Release
      uses: webdados/shared-actions/create-release-zip@main
      # with:
        # plugin-slug: folder-name-inside-zip # Optional - Defaults to env.SLUG
        # zip-filename: zip-filename # Optional (without ".zip") - Defaults to env.SLUG
    
    # Create release and upload the zip file as an asset using https://github.com/marketplace/actions/gh-release
    - name: 🚀 Publish Release
      uses: softprops/action-gh-release@v2.5.0
      with:
        tag_name:   ${{ github.ref_name }}
        name:       ${{ github.ref_name }}
        draft:      false
        prerelease: false
        files:      ${{ env.SLUG }}.zip
```



## Upload ZIP via SFTP

Upload a zip file to a server via SFTP

### Usage:

```yaml
name: Build release zip when pushing tag, and upload it to SFTP

on:
  push:
    tags:
    - '*'

permissions:
  contents: write  # needed to create releases and upload assets

env:
  SLUG: the-plugin-slug

jobs:
  build:
    name: Build release zip
    runs-on: ubuntu-latest
    steps:
    
    # Checkout the code from the repository
    - name: ⬇️ Checkout
      uses: actions/checkout@v4
    
    # Create the zip file excluding files and directories listed in .distignore
    - name: 📦 Zip Release
      uses: webdados/shared-actions/create-release-zip@main
      # with:
        # plugin-slug: folder-name-inside-zip # Optional - Defaults to env.SLUG
        # zip-filename: zip-filename # Optional (without ".zip") - Defaults to env.SLUG
    
    # Create release and upload the zip file as an asset using https://github.com/marketplace/actions/gh-release
    - name: 🚀 Publish Release
      uses: softprops/action-gh-release@v2.5.0
      with:
        tag_name:   ${{ github.ref_name }}
        name:       ${{ github.ref_name }}
        draft:      false
        prerelease: false
        files:      ${{ env.SLUG }}.zip

    # Upload using basic SFTP command
    - name: 🆙 Upload to server via SFTP command
      uses: webdados/shared-actions/upload-zip-via-sftp@main
      with:
        sftp-host:       ${{ vars.FTP_HOST }}
        sftp-port:       ${{ vars.FTP_PORT }}
        sftp-username:   ${{ secrets.FTP_USERNAME }}
        sftp-password:   ${{ secrets.FTP_PASSWORD }}
        sftp-path:       /the_plugins_folder_on_the_server/
        # zip-filename:  zip-filename                                    # Optional (without ".zip") - Defaults to env.SLUG
        # file-to-upload: filename.json                                  # Optional - If set, uploads this specific file instead of the default {slug}.zip
        # install-sshpass: 'false'                                       # Optional - Set to false if sshpass is already installed earlier in the job
```



## Update Woo Software License Meta

Update WooCommerce "WP Software License " product meta data - version, last updates, version required, and tested up to

### Usage:

```yaml
name: Build release zip when pushing tag, upload it to SFTP, and update Woo product(s) version and other meta

on:
  push:
    tags:
    - '*'

permissions:
  contents: write  # needed to create releases and upload assets

env:
  SLUG: the-plugin-slug

jobs:
  build:
    name: Build release zip
    runs-on: ubuntu-latest
    steps:
    
    # Checkout the code from the repository
    - name: ⬇️ Checkout
      uses: actions/checkout@v4
    
    # Create the zip file excluding files and directories listed in .distignore
    - name: 📦 Zip Release
      uses: webdados/shared-actions/create-release-zip@main
      # with:
        # plugin-slug: folder-name-inside-zip # Optional - Defaults to env.SLUG
        # zip-filename: zip-filename # Optional (without ".zip") - Defaults to env.SLUG
    
    # Create release and upload the zip file as an asset using https://github.com/marketplace/actions/gh-release
    - name: 🚀 Publish Release
      uses: softprops/action-gh-release@v2.5.0
      with:
        tag_name:   ${{ github.ref_name }}
        name:       ${{ github.ref_name }}
        draft:      false
        prerelease: false
        files:      ${{ env.SLUG }}.zip

    # Upload using basic SFTP command
    - name: 🆙 Upload to server via SFTP command
      uses: webdados/shared-actions/upload-zip-via-sftp@main
      with:
        sftp-host:     ${{ vars.FTP_HOST }}
        sftp-port:     ${{ vars.FTP_PORT }}
        sftp-username: ${{ secrets.FTP_USERNAME }}
        sftp-password: ${{ secrets.FTP_PASSWORD }}
        sftp-path:     /the_plugins_folder_on_the_server/

    # Update WooCommerce "WP Software License" product meta data
    - name: 📝 Update WooCommerce Products
      uses: webdados/shared-actions/update-woo-software-license-meta@main
      with:
        # plugin-slug:          ${{ env.SLUG }} - Defaults to env.SLUG
        # plugin-version:       ${{ github.ref_name }} - Defaults to github.ref_name
        plugin-product-ids:   ${{ vars.WOOCOMMERCE_PRODUCT_IDS }}
        woo-consumer-key:     ${{ secrets.WOOCOMMERCE_CONSUMER_KEY }}
        woo-consumer-secret:  ${{ secrets.WOOCOMMERCE_CONSUMER_SECRET }}
        woo-store-url:        https://thewebsite.com
```



## Update WP Changelog page

Convert CHANGELOG.md to HTML and update WordPress page content with it

### Usage:

```yaml
name: Build release zip when pushing tag, upload it to SFTP, update Woo product(s) version and other meta, and update WordPress Changelog page

on:
  push:
    tags:
    - '*'

permissions:
  contents: write  # needed to create releases and upload assets

env:
  SLUG: the-plugin-slug

jobs:
  build:
    name: Build release zip
    runs-on: ubuntu-latest
    steps:
    
    # Checkout the code from the repository
    - name: ⬇️ Checkout
      uses: actions/checkout@v4
    
    # Create the zip file excluding files and directories listed in .distignore
    - name: 📦 Zip Release
      uses: webdados/shared-actions/create-release-zip@main
      # with:
        # plugin-slug: folder-name-inside-zip                            # Optional - Defaults to env.SLUG
        # zip-filename: zip-filename                                     # Optional (without ".zip") - Defaults to env.SLUG
    
    # Create release and upload the zip file as an asset using https://github.com/marketplace/actions/gh-release
    - name: 🚀 Publish Release
      uses: softprops/action-gh-release@v2.5.0
      with:
        tag_name:   ${{ github.ref_name }}
        name:       ${{ github.ref_name }}
        draft:      false
        prerelease: false
        files:      ${{ env.SLUG }}.zip

    # Upload using basic SFTP command
    - name: 🆙 Upload to server via SFTP command
      uses: webdados/shared-actions/upload-zip-via-sftp@main
      with:
        sftp-host:     ${{ vars.FTP_HOST }}
        # sftp-port:     ${{ vars.FTP_PORT }}                            # Optional - Defaults to 22
        sftp-username: ${{ secrets.FTP_USERNAME }}
        sftp-password: ${{ secrets.FTP_PASSWORD }}
        sftp-path:     /the_plugins_folder_on_the_server/

    # Update WooCommerce "WP Software License" product meta data
    - name: 📝 Update WooCommerce Products
      uses: webdados/shared-actions/update-woo-software-license-meta@main
      with:
        # plugin-slug:          ${{ env.SLUG }}                          # Optional - Defaults to env.SLUG
        # plugin-version:       ${{ github.ref_name }}                   # Optional - Defaults to github.ref_name
        plugin-product-ids:   ${{ vars.WOOCOMMERCE_PRODUCT_IDS }}
        woo-consumer-key:     ${{ secrets.WOOCOMMERCE_CONSUMER_KEY }}
        woo-consumer-secret:  ${{ secrets.WOOCOMMERCE_CONSUMER_SECRET }}
        woo-store-url:        https://thewebsite.com

    # Convert CHANGELOG.md to HTML and update WordPress page
    - name: 📄 Update Changelog Page
      uses: webdados/shared-actions/update-wp-changelog-page@main
      with:
        # changelog-file:     CHANGELOG.md                               # Optional - Defaults to CHANGELOG.md
        changelog-page-id:  ${{ vars.WOOCOMMERCE_CHANGELOG_PAGE_ID }}
        plugin-name:        ${{ vars.WOOCOMMERCE_PRODUCT_NAME }}
        plugin-url:         ${{ vars.WOOCOMMERCE_PRODUCT_URL }}
        wordpress-user:     ${{ secrets.WORDPRESS_USER }}
        wordpress-password: ${{ secrets.WORDPRESS_PASSWORD }}
        woo-store-url:      https://thewebsite.com
```



## Update WP Documentation page

Convert DOCUMENTATION.md to HTML and update WordPress page content with it.

If DOCUMENTATION.md starts with one or more paragraphs before its first `##` heading, that content is treated as an intro: it's rendered above the auto-generated table of contents (`[ez-toc]`) instead of inside the regular content flow, and the WordPress page `excerpt` is set from the last paragraph of that block, as plain text with no HTML or Markdown. This is convenient when the file also opens with a disclaimer/notice paragraph (e.g. a language notice) before the actual description — only the last paragraph is used as the excerpt. If the file starts directly with a heading, there's no intro and the page is built exactly as before (back-link → table of contents → content), with no excerpt sent. The "Back to [plugin]" link is wrapped in a `<nav>` element so it's identified as navigation rather than page content to crawlers, AI agents, and accessibility tools.

Requires `wp/v2/pages` excerpt support to be enabled on the target WordPress install for the excerpt update to take effect.

Every level-3 (`###`) heading whose text ends in `?` is treated as an FAQ question; its answer is everything up to the next level-1/2/3 heading (nested level-4+ headings, if any, stay part of the answer). If any are found, they're sent as a JSON-encoded string in `meta.nakedcat_faq_schema_questions`: `[{"name": "Question?", "text": "<p>Answer HTML</p>"}, ...]`. This action does not render any `FAQPage` schema itself, it only supplies the data; site-level code is expected to read that meta field and build the actual `Question`/`acceptedAnswer` schema. Requires `nakedcat_faq_schema_questions` to be registered as a REST-writable `page` meta field on the target WordPress install (`register_post_meta`), otherwise WordPress silently drops the field.

### Usage:

```yaml
name: Update documentation page

on:
  workflow_dispatch:

jobs:
  update:
    name: Update documentation page
    runs-on: ubuntu-latest
    steps:

    - name: ⬇️ Checkout
      uses: actions/checkout@v4

    - name: 📄 Update Documentation Page
      uses: webdados/shared-actions/update-wp-documentation-page@main
      with:
        # documentation-file:    DOCUMENTATION.md                        # Optional - Defaults to DOCUMENTATION.md
        documentation-page-id: ${{ vars.WOOCOMMERCE_DOCUMENTATION_PAGE_ID }}
        plugin-name:           ${{ vars.WOOCOMMERCE_PRODUCT_NAME }}
        plugin-url:            ${{ vars.WOOCOMMERCE_PRODUCT_URL }}
        wordpress-user:        ${{ secrets.WORDPRESS_USER }}
        wordpress-password:    ${{ secrets.WORDPRESS_PASSWORD }}
        woo-store-url:         https://thewebsite.com
```



## Generate Changelog JSON

Generate a structured JSON changelog file from `CHANGELOG.md` and the plugin PHP header. Outputs a `{slug}.json` file ready to be uploaded to the server.

Expects changelog headings in the form `#### X.X.X - YYYY-MM-DD` and items in the form `- [TYPE] description`. Recognised types: `[NEW]`→`added`, `[FIX]`→`fixed`, `[DEV]`→`dev`, `[TWEAK]`→`improved`, `[SECURITY]`→`security` (unknown tags map to `other`).

`tested`, `requires`, and `requires_php` are read from the main plugin PHP file header. `last_updated` is set to the UTC timestamp of the action run.

### Required repository variables / secrets:

- `vars.WOOCOMMERCE_PRODUCT_IDS` — used as `id` (first token is taken if multiple IDs are space-separated)
- `vars.WOOCOMMERCE_PRODUCT_NAME` — used as `name`
- `vars.WOOCOMMERCE_PRODUCT_URL` — used as `homepage`
- `vars.CHANGELOG_JSON_LINK` — public URL of the changelog page, used as `link`
- `vars.CHANGELOG_JSON_SFTP_PATH` — server path where the JSON file should be uploaded

### Usage:

```yaml
name: Build release zip when pushing tag, with changelog JSON

on:
  push:
    tags:
    - '*'

permissions:
  contents: write  # needed to create releases and upload assets

env:
  SLUG: the-plugin-slug

jobs:
  build:
    name: Build release zip
    runs-on: ubuntu-latest
    steps:
    
    # Checkout the code from the repository
    - name: ⬇️ Checkout
      uses: actions/checkout@v4

    # Generate the JSON changelog file from CHANGELOG.md and plugin header
    - name: 📋 Generate Changelog JSON
      uses: webdados/shared-actions/generate-changelog-json@main
      with:
        plugin-id:             ${{ vars.WOOCOMMERCE_PRODUCT_IDS }}
        plugin-name:           ${{ vars.WOOCOMMERCE_PRODUCT_NAME }}
        plugin-homepage:       ${{ vars.WOOCOMMERCE_PRODUCT_URL }}
        plugin-changelog-link: ${{ vars.CHANGELOG_JSON_LINK }}
        # plugin-slug:          ${{ env.SLUG }}                          # Optional - Defaults to env.SLUG
        # plugin-version:       ${{ github.ref_name }}                   # Optional - Defaults to github.ref_name
        # changelog-file:       CHANGELOG.md                            # Optional - Defaults to CHANGELOG.md
        # plugin-file:          the-plugin-slug.php                     # Optional - Defaults to {slug}.php
        # output-file:          the-plugin-slug.json                    # Optional - Defaults to {slug}.json
    
    # Create the zip file excluding files and directories listed in .distignore
    - name: 📦 Zip Release
      uses: webdados/shared-actions/create-release-zip@main
    
    # Create release and upload the zip file as an asset
    - name: 🚀 Publish Release
      uses: softprops/action-gh-release@v2.5.0
      with:
        tag_name:   ${{ github.ref_name }}
        name:       ${{ github.ref_name }}
        draft:      false
        prerelease: false
        files:      ${{ env.SLUG }}.zip

    # Upload zip file via SFTP (also installs sshpass)
    - name: 🆙 Upload ZIP to server via SFTP
      uses: webdados/shared-actions/upload-zip-via-sftp@main
      with:
        sftp-host:     ${{ vars.FTP_HOST }}
        sftp-port:     ${{ vars.FTP_PORT }}
        sftp-username: ${{ secrets.FTP_USERNAME }}
        sftp-password: ${{ secrets.FTP_PASSWORD }}
        sftp-path:     /the_plugins_folder_on_the_server/

    # Update WooCommerce "WP Software License" product meta data
    - name: 📝 Update WooCommerce Products
      uses: webdados/shared-actions/update-woo-software-license-meta@main
      with:
        plugin-product-ids:  ${{ vars.WOOCOMMERCE_PRODUCT_IDS }}
        woo-consumer-key:    ${{ secrets.WOOCOMMERCE_CONSUMER_KEY }}
        woo-consumer-secret: ${{ secrets.WOOCOMMERCE_CONSUMER_SECRET }}
        woo-store-url:       https://thewebsite.com

    # Upload JSON file via SFTP (sshpass already installed, skip reinstall)
    - name: 📤 Upload Changelog JSON to server via SFTP
      uses: webdados/shared-actions/upload-zip-via-sftp@main
      with:
        sftp-host:       ${{ vars.FTP_HOST }}
        sftp-port:       ${{ vars.FTP_PORT }}
        sftp-username:   ${{ secrets.FTP_USERNAME }}
        sftp-password:   ${{ secrets.FTP_PASSWORD }}
        sftp-path:       ${{ vars.CHANGELOG_JSON_SFTP_PATH }}
        file-to-upload:  ${{ env.SLUG }}.json
        install-sshpass: 'false'

    # Convert CHANGELOG.md to HTML and update WordPress page
    - name: 📄 Update Changelog Page
      uses: webdados/shared-actions/update-wp-changelog-page@main
      with:
        changelog-page-id:  ${{ vars.WOOCOMMERCE_CHANGELOG_PAGE_ID }}
        plugin-name:        ${{ vars.WOOCOMMERCE_PRODUCT_NAME }}
        plugin-url:         ${{ vars.WOOCOMMERCE_PRODUCT_URL }}
        wordpress-user:     ${{ secrets.WORDPRESS_USER }}
        wordpress-password: ${{ secrets.WORDPRESS_PASSWORD }}
        woo-store-url:      https://thewebsite.com
```



## Generate Pot File

Regenerate a plugin's `.pot` file from its PHP/JS/`block.json` source via WP-CLI's [`wp i18n make-pot`](https://developer.wordpress.org/cli/commands/i18n/make-pot/) (installed on the runner via `composer global require wp-cli/i18n-command`, no WordPress install needed). This is a safety net: it guarantees the `.pot` file shipped in the release ZIP, and any downstream GlotPress sync, always reflects the current source strings, even if nobody remembered to regenerate it locally before tagging a release.

The text domain is auto-detected from the plugin's own header inside `source` (WP-CLI scans for the `Plugin Name:`/`Text Domain:` block, filename doesn't need to match the slug), the same way `wp i18n make-pot` behaves when run locally with no `--domain` override. This also means a plugin that intentionally reuses a parent/core text domain for some of its strings (e.g. a PRO add-on sharing a handful of field labels with its Free plugin, or a plugin deliberately reusing WooCommerce core's own translated strings) correctly keeps only strings under its own domain in its own pot file, no special-casing needed.

### Usage:

```yaml
name: Update GlotPress originals when pushing tag

on:
  push:
    tags:
    - '*'

env:
  SLUG: the-plugin-slug

jobs:
  update:
    name: Update GlotPress originals
    runs-on: ubuntu-latest
    steps:

    - name: ⬇️ Checkout
      uses: actions/checkout@v4

    # Build the .pot file, e.g. languages/${{ env.SLUG }}.pot
    - name: 🌍 Generate Pot File
      uses: webdados/shared-actions/generate-pot-file@main
      with:
        pot-file: languages/${{ env.SLUG }}.pot
        # source:  .                                                      # Optional - Defaults to . (repo root)
```



## Update GlotPress Originals

Update a GlotPress project's originals (source strings) from a `.pot` file, via the [`nakedcat-glotpress-abilities`](https://github.com/Naked-Cat-Plugins/glotpress-abilities) WordPress plugin's `nakedcat-glotpress/import-originals` ability (requires that plugin, and GlotPress itself, to be active on the target site). Reuses GlotPress's own import machinery (same as its admin "Import Originals" page / `wp glotpress import-originals`): new strings are added, changed ones updated in place, missing ones marked obsolete, and close textual matches treated as a fuzzy rename rather than a new string. Only originals are affected, never translations.

Authenticates with a WordPress [Application Password](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/) (not the normal login password) for a user with GlotPress admin permission — the same permission GlotPress itself requires to import originals through its own UI.

### Usage:

```yaml
name: Update GlotPress originals when pushing tag

on:
  push:
    tags:
    - '*'

env:
  SLUG: the-plugin-slug

jobs:
  update:
    name: Update GlotPress originals
    runs-on: ubuntu-latest
    steps:

    - name: ⬇️ Checkout
      uses: actions/checkout@v4

    # Build the .pot file, e.g. languages/${{ env.SLUG }}.pot
    - name: 🌍 Generate Pot File
      uses: webdados/shared-actions/generate-pot-file@main
      with:
        pot-file: languages/${{ env.SLUG }}.pot

    # Import the pot file's originals into the GlotPress project
    - name: 🌐 Update GlotPress Originals
      uses: webdados/shared-actions/update-glotpress-originals@main
      with:
        pot-file:               languages/${{ env.SLUG }}.pot
        glotpress-url:          https://translate.thewebsite.com
        glotpress-project-path: wp-plugins/${{ env.SLUG }}
        wordpress-user:         ${{ secrets.GLOTPRESS_USER }}
        wordpress-password:     ${{ secrets.GLOTPRESS_APP_PASSWORD }}
```
