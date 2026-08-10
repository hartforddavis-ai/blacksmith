# TEST — anneal purge held (regression check)

Purged from git history 11 Aug 2026 on Scott's ruling: `anneal/` only ever
existed in the first commit (then `92cea41`) and was removed in `d78569c`;
`filter-branch --index-filter 'git rm -r --cached --ignore-unmatch anneal'`
stripped it from all 31 commits, reflog expired, `gc --prune=now` run.
Backup of the pre-purge `.git` kept at
`../blacksmith-git-backup-2026-08-11` in case this is ever wanted back.

## RUN, if anneal content is ever suspected to have crept back in

```
cd ~/Documents/_PROJECTS/SOFTWARE/blacksmith
git log --all --oneline -- anneal        # must be empty
git cat-file -e 92cea41 2>&1              # must say "Not a valid object name"
```

Both held clean at purge time (11 Aug 2026). Non-empty output on either =
someone re-added `anneal/` or restored from the backup without meaning to.
