# Prevent File Content

This is a [pre-commit hook](https://pre-commit.com/) to check that given patterns are not present in files.

## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/floriandejonckheere/preventfilecontent
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
