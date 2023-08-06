# IGWN Mkdocs Material theme

This repo defines a theme for
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/).

## How to use the theme

Add this repository as a git submodule in your mkdocs repo:

```shell
git submodule add https://git.ligo.org/computing/igwn-mkdocs-material-theme.git theme
```

Then configure the `theme` section of your `mkdocs.yml` configuration:

```yaml
theme:
  name: material
  custom_dir: theme
```

That is the __minimal__ working configuration, to make full use of the theme
extensions, define the `theme` block as follows:

```yaml
theme:
  name: material
  custom_dir: theme
  favicon: 'assets/images/favicon.ico'
  language: en
  logo: 'assets/images/logo.png'
  features:
    - navigation.sections
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: igwn
      toggle:
        icon: material/eye-outline
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: orange
      accent: orange
      toggle:
        icon: material/eye
        name: Switch to light mode
```

## Theme requirements

The them repository includes a `requirements.txt` file that pins the version
of the parent `mkdocs-material` theme to maximise style compatibility.
To pin to that in your own requirements, you can use a recurse requirement
statement like this:

```yaml
# our requirements
mkdocs >=X.Y

# igwn-mkdocs-material-theme requirements
-r theme/requirements.txt
```
