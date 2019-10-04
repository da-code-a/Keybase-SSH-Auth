"""
This module is used to simplify the main module a bit.
This will hold functions to send messages, react to them, and
check reactions when needed.
Used for the whole authorization-over-chat flow.
"""

from pykeybase import KeybaseChat as chat
from dotenv import load_dotenv
from os import environ
from msgpack import packb
from base64 import b64encode

load_dotenv()

channel = {
    "name" : environ["KB_TEAM"] + ".ssh_auth",
    "members_type" : "team"
}

bot_name = chat._get_username(chat)

def send_auth_request(server: str, remote: str, username: str) -> int:
    """
    This function sends the authorization request
    to the .ssh_auth subteam of the specified
    Keybase Team. Then, it reacts to the message
    with "Approve" and "Deny" so that those reactions
    can be checked for changes later.
    """
    msg_payload = {
        "method" : "send",
        "params" : {
            "options" : {
                "channel" : channel,
                "message" : {
                    "body" : f"`{username}` is requesting access to `{server}` from `{remote}`."
                }
            }
        }
    }
    msg = chat._send_chat_api(chat, msg_payload)
    msg_id = msg["result"]["id"]
    chat._send_chat_api(chat, {
        "method" : "reaction",
        "params" : {
            "options" : {
                "channel" : channel,
                "message_id" : msg_id,
                "message" : {
                    "body" : "Approve"
                }
            }
        }
    })
    chat._send_chat_api(chat, {
        "method" : "reaction",
        "params" : {
            "options" : {
                "channel" : channel,
                "message_id" : msg_id,
                "message" : {
                    "body" : "Deny"
                }
            }
        }
    })
    return msg_id

def find_first_reaction(id: int) -> tuple:
    """
    This function finds the first Approve or Deny
    reaction to a request message and returns
    the decision. If no valid reactions are
    found, return nothing.
    Thanks to @dxb on Keybase for teaching
    about the msgpack method of getting
    messages by ID in Keybase's chat API.
    """
    encoded = b64encode(packb(id)).decode()
    msgs_since = chat._send_chat_api(chat,{
        "method" : "read",
        "params" : {
            "options" : {
                "channel" : channel,
                "pagination" : {
                    "previous" : encoded,
                    "num" : 9999999 #A ridiculous number because we need all messages
                }
            }
        }
    })['result']['messages']
    for msg in msgs_since:
        if msg['msg']['sender']['username'] == bot_name:
            continue
        if msg['msg']['content']['type'] == 'reaction':
            reaction = msg['msg']['content']['reaction']
            if reaction['m'] == id and reaction['b'] == 'Approve':
                return ('approved', msg['msg']['sender']['username'])
            elif reaction['m'] == id and reaction['b'] == "Deny":
                return ('denied', msg['msg']['sender']['username'])
    return (None, None)

def send_decision(timed: bool, decider: str, decision: str, user: str, host: str, remote: str, msgid: int) -> None:
    """
    This function will send the message about the
    decision on a connection request as well as delete
    the original request message.
    """
    chat._send_chat_api(chat, {
        "method" : "delete",
        "params" : {
            "options" : {
                "channel" : channel,
                "message_id" : msgid
            }
        }
    })
    if timed:
        message_content = f"`{user}`'s request to connect to `{host}` from `{remote}` timed out and was not approved."
    else:
        message_content = f"`{user}`'s request to connect to `{host}` from `{remote}` was `{decision}` by `{decider}`."
    chat._send_chat_api(chat, {
        "method" : "send",
        "params" : {
            "options" : {
                "channel" : channel,
                "message" : {
                    "body" : message_content
                }
            }
        }
    })
    return None

if __name__ == "__main__":
    import sys
    print("This module should only be imported.")
    sys.exit(1)