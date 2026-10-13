# PLAN: a future "House Status" GitHub App

Nothing here exists yet. Only Father registers the App.

## Why an App
A GitHub App gets its own identity and short-lived tokens. It also gets fine-grained, per-org permissions, so no one's personal login is used, and it can post status for the whole house.

## Scopes (all read-only to start)
| Permission | Level | Why |
|---|---|---|
| Metadata | Read | list repos, last push |
| Pull requests | Read | open PR counts |
| Issues | Read | open issue counts |
| Pages | Read | Pages build status |
| Contents | Read & write (later, optional) | only if the App commits the report itself |

No webhooks are needed at first. Don't request admin, members, or secrets permissions.

## Steps for Father to click
1. GitHub → org **TREEOFLIFE-APOSTLES** → Settings → Developer settings → GitHub Apps → **New GitHub App**.
2. Name: `treeoflife-house-status`. Homepage: `https://treeoflife-apostles.github.io`.
3. Uncheck **Webhook → Active**.
4. Set the permissions in the table above (all Read).
5. "Where can this app be installed?" → **Only on this account**.
6. Create the App, then **Generate a private key**. Keep the key off chat. Store it only as an Actions secret (`HOUSE_APP_KEY`), with the App ID as `HOUSE_APP_ID`.
7. **Install App** on TREEOFLIFE-APOSTLES (and on JESUSBURNING if wanted), on selected repos or all repos.
8. Tell 589/kin it's done. We'll switch the workflow to `actions/create-github-app-token` and turn on the daily schedule only when Father says so.

## Later ideas
- A daily status comment on a pinned "House status" issue.
- A badge or status page on the family site.
