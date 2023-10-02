# Caching-Github-Auth-Tokens.md

If you ever want to `git push` or `git pull` or etc. from the cluster, you used to just have to give them your password. For some reason, they decided to make the process more complicated by creating these authentication tokens that are randomly generated and impossible to remember. You'll have to generate your own personal access token and cache it to make sure that you don't have to input the token every time

Largely following instructions from [this link](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories)


Step-by-step guide
------------------

1. Go to [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. In the top right, click `Generate new token` and click the `Generate new token (Classic)` option
3. Here, we'll make the token
	- You'll need to specify an expiration date for the token, make it whatever you want. Once the token expires, you'll have to do all of this again :( 
	- You are also recquired to add a note
	- You then need to give it specific permissions. The most basic ones are `repo`, `read:org` (under `admin:org`), and `workflow` for basic github operations. Click those boxes and any other specific permissions you may need

This is what my settings look like:
![](/img/github_auth_settings.png?raw=true)

4. Click `generate token` when you're done
5. You'll be taken to a page with the newly generated token. Copy it to your clipboard
6. Log into midway/beagle3 
7. Install [`Github CLI`](https://github.com/cli/cli#installation), would recommend doing this through anaconda.
	- `conda install gh --channel conda-forge`
8. Enter `gh auth login` into the command prompt and follow instructions
	- You'll get a list of different options
	- Account --> GitHub.com
	- Protocol --> HTTPS
	- Authentication --> Paste an authentication token
9. Paste the token
10. `git push` and `git pull` to your heart's content 



