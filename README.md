Keybase SSH Auth Service
==

Purpose
--

This project is meant to allow anyone to secure their SSH sessions across multiple servers by enforcing an additional factor of authentication. When a user attempts to make a new SSH connection, a message is posted to a team channel over Keybase chat. By reacting to that message with either "Approve" or "Deny", the connection will either be completed or immediately closed. This means that, even if your SSH keys are somehow compromised, you can secure your SSH connections. Furthermore, a log of connections will always be available and searchable in Keybase chat as well as accessible in database form on the authentication server. Overall, this project just aims to improve SSH security in general by combining it with [Keybase](https://keybase.io).

Why Make This?
--

I get it. There are other ways to secure your SSH sessions. Lots of other ways. However, nobody complains about a new flavor of ice cream, right? I made this because I wanted an easy way to keep an eye on my servers for my side-gig and I had previously made a similar application over Slack for the company I work for. This is a (relatively) simple way of adding an additional factor of authentication for any systems you plan on SSH'ing into.

Who Is This For?
--

This can be used for companies to control who is accessing servers through SSH when, and removing a user's access is as easy as removing them from a Keybase team. It's immediate, because nobody who still has access should be approving that user's sessions, and gives you time to remove the user and their keys from your systems. It also generates a nice log of every user that connected and where they connected from that can be searched whenever needed.

Additionally, it can be used for individuals just trying to keep an eye on their hobby servers. They'll be able to approve their own sessions and if they ever get a request when they're not expecting it, they know that their key or password (shame on you if you still use password-based SSH) has been compromised.

Basically, it's for anyone who wants to use it. Easy enough, right?

Docker Set-up
==

You can now run the autentication server in Docker. The target systems (servers/hosts you'd like to secure with this) still require copying of the pam client script, but that's easy enough and doesn't have any real dependencies. To get this going on Docker, simply run:

```
docker run \
-e KB_TYPE={team or private} \
-e KB_TEAM={your team name if using KB_TYPE team} \
-e KB_CHANNEL={your team channel if using KB_TYPE team, suggested: general} \
-e KB_USER={Target Keybase user to receive messages if using KB_TYPE private} \
-e AUTH_TOKEN={Your desired auth password for request} \
-e FLASK_ENV={development or production} \
-e KEYBASE_USERNAME={your bot's username} \
-e KEYBASE_PAPERKEY={a paperkey associated with your bot} \
-p 5000:5000 \
donaldkbrown214/keybasedmfa
```

Alternatively, you can use something like cockpit or any other front-end for managing Docker containers to set this up. Personally, I use cockpit because it just makes everything nice and easy.

Please note that not all environment variables are needed. Refer to the [environment](#environment) for more information.

Non-Docker Set-up
==

Requirements
--

The authentication server requires a few things. You need:

- Python 3.6+
- Development headers for your version of Python
- A C compiler (`gcc` or equivalent)
- Python Libraries:
  - flask
  - uwsgi
  - sqlalchemy
  - pykeybase (not pykeybasebot)
  - python-dotenv (if you are loading values through a file rather than setting them in systemd or similar)
- nginx (recommended, not required, for wrapping over flask)
- certbot (recommended, not required, for enabling SSL)
- A system user logged in to a reserved Keybase bot user (super duper important)
- A properly configured environment (see [environment](#environment) for more info)

Because of the way this service works, you **cannot** (and I really cannot stress this enough), run the authentication server under the same Keybase user that you will try be trying to approve/deny requests with. Reactions **must** come from a separate user. I am trying to be as explicit and clear as I can be here, I am completely absolved of any fault if you lock yourself out of your server. Any member (other than the bot user) of the team set in your environment variables, or the user that the bot is PM'ing will be able to approve/deny SSH requests.

For any server that you would like to protect with this, you just need standard utilities such as PAM (baked in every *nix I know of), bash, and cURL. Not all distributions come with cURL by default, so make sure it's installed before enabling this otherwise you might get locked out forever (don't say I didn't warn you).

Set-Up
--

Authentication Server:

1. Clone this repository
2. Establish a virtual environment (recommended)
3. Install all requirements with `pip install -r requirements.txt`
4. Modify `example.env` to include your desired values and rename it to just `.env` (if not setting env variables in another way)
5. Set-up the service to start at system start as the correct user (highly recommended)

Obviously, this also requires Keybase to be running at system start. See the [Keybase Linux User Guide](https://keybase.io/docs/linux-user-guide) for more information on getting that set-up. An example systemd service file was included here to help you get this running at system start.

Target Systems:

1. Copy `kb_pam_client.sh` to `/usr/bin` and make it executable
2. Modify `/usr/bin/kb_pam_client.sh` so that valid entries are entered where needed (I explain it all there)
3. Modify `/etc/pam.d/sshd` to include the line `session required pam_exec.so seteuid /usr/bin/kb_pam_client.sh` at the very end

Clients:

Nothing! You can connect from any regular SSH client as normal. As long as you have access to Keybase somewhere (phone, another computer, etc.) to react to the request messages, you're good to go.

Environment
--

When setting this up, you'll have to have some environment variables set-up, and some of those are dependent on where you want your authentication requests to go on Keybase. You can have it send the requests/responses to a personal channel (bot to user), a regular team, a subteam, or even a particular "big team" channel. There are also some global values that should be set.

Globals:

- `FLASK_ENV` : This can be set to `development`, `staging`, or `production`. I recommend setting it to `development` while you get set-up as it outputs some debug information if things go wrong. However, when you are ready to deploy for real, make sure you set it to `production`
- `AUTH_TOKEN` : This can be any string you want, so long as it does not contain spaces. This is the password that the server will check for when receiving requests from the client called by PAM. Prevents a bad actor from spamming your bot with fake requests.
- `KB_TYPE` : This can be set to `private` or `team`. This determines whether the bot will be sending those requests to a private message channel or a team chat. This will also determine which other variables will need to be set.

`private` type:

 - `KB_USER` : This should be set to the Keybase username that the bot sends request messages to.

 `team` type:

 - `KB_TEAM` : This is the name of the Keybase team that the bot should post to. This can be a regular "small" team with no channels, a subteam, or a "big" team with chat channels. You just need to make sure that the bot has access to the team in question.
 - `KB_CHANNEL` : This is optional and defaults to `general` if not given. This is the specific chat channel to post to in the case of the bot posting to a "big" team and you want the messages contained to a particular channel.

Other Info
--

If you need any help with this at all, feel free to reach out to me @donaldkbrown on Keybase or create an issue/pull request here.