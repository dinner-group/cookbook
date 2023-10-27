# How to use git


If you're developing code, it's best practice to use `git` to keep track of changes and previous versions
without driving yourself crazy.
There are many tutorials online if you just search for "How to use git", but here are
some tips and tricks that will make you experience a little bit cleaner.

You can create a `.gitconfig` file that set various configurations for commands,
alias, etc. 
Here's an example file that I use:
```
[user]
    email = spencerchenguo@gmail.com
    name = Spencer Guo

[alias]
    co = checkout
    st = status
    br = branch
    ci = commit
    lg = lg1
    lg1 = lg1-specific --all
    lg2 = lg2-specific --all
    lg3 = lg3-specific --all

    lg1-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold green)(%ar)%C(reset) %C(white)%s%C(reset) %C(dim white)- %an%C(reset)%C(auto)%d%C(reset)'
    lg2-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset)%C(auto)%d%C(reset)%n''          %C(white)%s%C(reset) %C(dim white)- %an%C(reset)'
    lg3-specific = log --graph --abbrev-commit --decorate --format=format:'%C(bold blue)%h%C(reset) - %C(bold cyan)%aD%C(reset) %C(bold green)(%ar)%C(reset) %C(bold cyan)(committed: %cD)%C(reset) %C(auto)%d%C(reset)%n''          %C(white)%s%C(reset)%n''          %C(dim white)- %an <%ae> %C(reset) %C(dim white)(committer: %cn <%ce>)%C(reset)'

[core]
    excludesFile = ~/.gitignore
[pull]
        rebase = true
[http]
        sslverify = false
[credential "https://github.com"]
        helper = 
        helper = !/beagle3/dinner/scguo/envs/md/bin/gh auth git-credential
[credential "https://gist.github.com"]
        helper = 
        helper = !/beagle3/dinner/scguo/envs/md/bin/gh auth git-credential
```
Some useful points:
- `git` aliases can be set under `[alias]` to shorten commands. The commands `lg*` allow you to visualize the graph of commits that have been made on difference branches.
- You almost *always* want to `rebase` when you `git pull` which essentially puts your local changes on top of the fetched remote changes.
- The last two lines have to do with authentication on the cluster - see [this troubleshooting guide](Caching-Github-Auth-Tokens.md) for more information.

Another useful resource I've found on how to think about git branches can be found [here](http://longair.net/blog/2009/04/16/git-fetch-and-merge/).
It gives a good overview of what exactly happens when you run commands like `git fetch`, `git pull`, and `git merge`, as well as how to use remote
and local branches.
