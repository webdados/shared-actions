# Webdados / Naked Cat Plugins shared GitHub actions

Shared GitHub Actions to use on several projects by Webdados / Naked Cat Plugins

Altought this repository is public (because of GitHub limitations), the usage of these actions by 3rd party projects is not recommended.



## Create Release Zip

Create a zip file for the GitHub release and for eventual upload to a server.

### Usage:

Assumes a `.distignore` file exists containig the files and folders to exclude.
If `env.SLUG` is set, `plugin-slug` and `zip-filename` are not required and will default to that (most of the cases).

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
      with:
        plugin-slug: folder-name-inside-zip # Optional - Defaults to env.SLUG
        zip-filename: zip-filename # Optional (without ".zip") - Defaults to env.SLUG
```