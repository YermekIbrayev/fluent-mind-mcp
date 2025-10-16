# GitHub

**Category**: DevTools | **Back to**: [Index](../../CLAUDE.md)

---

## Purpose

Complete GitHub repository operations including files, branches, issues, and pull requests.

---

## Capabilities

**File Operations**: Create, update, read files
**Repository Management**: Create, fork, search repos, manage branches
**Issues**: Create, list, update, comment
**Pull Requests**: Create, review, merge, manage
**Search**: Code, issues, users across GitHub

---

## Key Function Groups

### File Operations

- `create_or_update_file` - Single file commit (requires SHA when updating)
- `push_files` - Multiple files in single commit
- `get_file_contents` - Read files/directories from repo

### Repository Management

- `create_repository` - Create new repo
- `fork_repository` - Fork to account/org
- `search_repositories` - Search GitHub repos
- `create_branch` - Create new branch from base
- `list_commits` - View commit history

### Issues

- `create_issue` - Create new issue
- `list_issues` - Filter and list issues (by state, labels, etc.)
- `get_issue` - Get issue details
- `update_issue` - Update existing issue
- `add_issue_comment` - Comment on issue

### Pull Requests

**Creation & Info**:
- `create_pull_request` - Create PR (head, base, title, body)
- `get_pull_request` - Get PR details
- `list_pull_requests` - Filter PRs (state, sort, etc.)
- `get_pull_request_files` - View changed files
- `get_pull_request_status` - Check CI status

**Review & Merge**:
- `get_pull_request_comments` - Read review comments
- `get_pull_request_reviews` - Get reviews
- `create_pull_request_review` - Submit review (APPROVE, REQUEST_CHANGES, COMMENT)
- `merge_pull_request` - Merge PR (merge, squash, rebase methods)
- `update_pull_request_branch` - Update with base branch

### Search

- `search_code` - Search code across repos (with filters)
- `search_issues` - Search issues and PRs (with sorting)
- `search_users` - Find GitHub users

---

## Common Use Cases

**Creating PRs**:
```
1. push_files or create_or_update_file
2. create_pull_request (head branch, base branch)
3. Monitor with get_pull_request_status
4. get_pull_request_reviews for feedback
5. merge_pull_request when approved
```

**Managing Issues**:
```
1. create_issue with labels
2. list_issues to track
3. add_issue_comment for updates
4. update_issue to change state/labels
```

**Code Review**:
```
1. get_pull_request_files to see changes
2. create_pull_request_review with comments
3. APPROVE or REQUEST_CHANGES
4. Track with get_pull_request_reviews
```

---

## Important Notes

- **SHA Required**: When updating files, must provide file's SHA
- **Branch Management**: Create branches before pushing
- **Review Comments**: Can comment on specific lines using `position` or `line`
- **Merge Methods**: Choose merge, squash, or rebase based on workflow

---

## Related

- [IDE](ide.md) - For code diagnostics before commit
- [Workflows](../workflows.md) - Git workflow integration
