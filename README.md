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