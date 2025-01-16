# portable_game_device

## Rules

1. DO NOT MAIN FORCE PUSH
2. All push requests Finik observes
3. If you pushed main - you must say about it and we do uncommit
4. Only README.md can be main pushed and only by Finik

### How to commit and push

0. 'git pull' for updating repo
1. Do things you have to do
2. Open git bash in folder
3. Do 'git add "name of file/files"' or "." if you want to add all changes
4. Do 'git commit -m "message"'
5. Do 'git push'

### How to create and add branch to github

1. git branch "branch_name"
2. git switch "branch_name"
3. Do things you have to do
4. git add "name of file/files"' or "." if you want to add all changes
5. Do 'git commit -m "message"'
6. git push --set-upstream origin "branch_name"

### How to delete branch from local and remote

1. Checkout if you are on main branch
2. If not write "git switch main"
3. To delete branch which merged locally "git branch -d 'branch_name'"
4. To delete branch which isn't merged "git branch -D 'branch_name'"
5. To delete remote branch write "git push origin --delete 'branch_name'"

### How to pull request:

1. git switch "Branch_name"
2. Do things you have to do
3. Commit and 'git push'
4. Open github/repo/pull_requests
5. Choose branches
6. Ensure that everything is OK
7. Press button "Create pull request"
8. Create pull request
