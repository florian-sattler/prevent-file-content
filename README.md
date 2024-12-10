# Prevent File Content

This is a [pre-commit hook](https://pre-commit.com/) to check that given patterns are not present in files.

## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/florian-sattler/prevent-file-content
  rev: ""
  hooks:
    - id: prevent-file-content
      args:
        - -p
        - "TODO"
      types_or:
        - python
        - javascript
        - yaml
```

## Configuration

Specify the patterns to prevent in the `args` section by using the `-p` / `--pattern` option. A pattern is interpreted as a python regular expression.

Use `types`, `types_or` or `files` to specify the file types to check. See [pre-commit's documentation](https://pre-commit.com/#filtering-files-with-types) for more information.

### Examples

Prevent `TODO` in all files:

```yaml
- id: prevent-file-content
  args:
    - -p
    - "TODO"
```

Prevent importing `os` in all python files:

```yaml
- id: prevent-file-content
  args:
    - --pattern
    - "import os"
    - --pattern
    - "from os import"
    - --pattern
    - "from os\\.[^\\s]+ import"
  types: [python]
```

Multiple configurations can be specified by repeating the hook id with different parameters:

```yaml
- repo: https://github.com/floriandejonckheere/preventfilecontent
  rev: ""
  hooks:
    # Prevent FIXME, HACK and TODO in all yaml and html files
    - id: prevent-file-content
      args:
        - -p
        - "TODO"
        - -p
        - "FIXME"
        - -p
        - "HACK"
      types_or:
        - yaml
        - html

    # Prevent some linting exceptions in python files
    - id: prevent-file-content
      args:
        - --pattern
        - "# noqa"
        - --pattern
        - "# pragma: no cover"
        - --pattern
        - "# type: ignore"
      types: [python]
```
