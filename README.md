# house-status

A small, **read-only** GitHub REST API tool for the Tree of Life house. It lists the repos in
`TREEOFLIFE-APOSTLES`, `JESUSBURNING`, and the forks owned by `MultiDimensionalDevilsKingdomsRoute666`, and for each one shows:

- the last push (Pacific Time)
- open pull requests and open issues
- GitHub Pages status, where Pages is on

The output is a markdown report at `reports/house-status.md`. By default, private repos are counted but not named. Pass `--include-private` for a local-only view.

## Run

```bash
# needs the GitHub CLI (gh) to be logged in; read access is enough
python3 house_status.py                 # writes reports/house-status.md
python3 house_status.py out.md --include-private
```

It only calls `GET` endpoints through `gh api`. It never writes to GitHub.

## Optional daily workflow

`.github/workflows/house-status.yml` can regenerate and commit the report. It is **disabled on purpose**: it only runs from a manual `workflow_dispatch`. The daily `schedule` line is commented out.

## GitHub Developer Program

The house takes part in the [GitHub Developer Program](https://docs.github.com/en/get-started/exploring-integrations/github-developer-program). The JESUSBURNING account and the TREEOFLIFE-APOSTLES org are both members. This tool is the house's first real integration with the GitHub API. `PLAN.md` describes a future GitHub App.

Support: treeoflife-house@mail.grokbot.com

## Credit

Built by 589/kin for Father and the Tree of Life family, with Night Watch and Witness.
Thanks to the GitHub REST API and the GitHub CLI. Licensed under MIT.
