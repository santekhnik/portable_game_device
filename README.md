# portable_game_device

## Additional features
-Other games
-Difficulties
-Settings
-Bot
-Second player
-Speed increase
-Field size
-Restart, pause, esc
-Smooth button

## Rules of development

1. All push requests Finik observes
2. README.md can be changed only by Finik
3. One task - one branch
4. You can't push to main branch by GitHub rules, so watch to your branches to prevent errors
5. If task needs changes from two people in one file - that will be conflicts, so do it alternately

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

### How to update main branch locally
1. Get everything done in your branch
2. Push this changes to github
3. Create pull request
4. Wait until someone approve your request
5. In git switch to main branch by "git switch main"
6. Merge branch with main by "git merge 'branch_name'"
7. Delete branch by inctructions if you are done
