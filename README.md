# qiskit-extensions.github.io

This repository allows us to set up client-side redirects in GitHub Pages for repositories that moved from the qiskit-extensions organization to qiskit-community.

## How to add a new project

```bash
./generate-redirects.py <repo-name>
```

`<repo-name>` should be a value like `qiskit-dynamics` or `arraylias`. This script assumes that the repository name has not changed, only the GitHub organization.
