Keybase SSH Auth Service
==

Purpose
--

This project is meant to allow anyone to secure their SSH sessions across multiple servers by enforcing an additional factor of authentication. When a user attempts to make a new SSH connection, a message is posted to a team channel over Keybase chat. By reacting to that message with either "Approve" or "Deny", the connection will either be completed or immediately closed. This means that, even if your SSH keys are somehow compromised, you can secure your SSH connections. Furthermore, a log of connections will always be available and searchable in Keybase chat as well as accessible in database form on the authentication server. Overall, this project just aims to improve SSH security in general by combining it with [Keybase](https://keybase.io).

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
- A regular user logged in to a reserved Keybase bot user (super duper important)
- A Keybase team with a subteam named `.ssh_auth` (also super duper important) (make sure the bot user is a member)

Because of the way this service works, you **cannot** (and I really cannot stress this enough), run the authentication server under the same Keybase user that you will try be trying to approve/deny requests with. Reactions **must** come from a separate user. I am trying to be as explicit and clear as I can be here, I am completely absolved of any fault if you lock yourself out of your server. Any member of `{TEAM}.ssh_auth` (other than the bot user) will be able to approve/deny SSH requests.

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

Other Info
--

If you need any help with this at all, feel free to reach out to me @donaldkbrown on Keybase or create an issue/pull request here.