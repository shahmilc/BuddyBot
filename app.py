import logging
from slack_bolt import App

# Initialize a Bolt for Python app
app = App()


def send_msg(client, msg):
    """
    Send out the message
    :param client: slack client
    :param msg: the message in slack format
    :return: none
    """
    response = client.chat_postMessage(**msg)
    logger.info(f"Send the message at {response['ts']}")


def unknown_cmd(user, channel, client):
    """
    Echo the command back
    :param user: user id
    :param channel: channel id
    :param client: slack client
    :param text: text of the message
    :return: none
    """
    msg = {
        "ts": "",
        "channel": channel,
        "username": user,
        "blocks": [
            {
                "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": f"Hello, *{user}*, I'm EchoBot. I can echo your messages back to you."
			    }
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": "Try adding `echo` somewhere in your message."
			}
		}
        ],
    }

    send_msg(client, msg)


def echo_cmd(user, channel, client, text):
    """
    Echo the command back
    :param user: user id
    :param channel: channel id
    :param client: slack client
    :param text: text of the message
    :return: none
    """
    msg = {
        "ts": "",
        "channel": channel,
        "username": user,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"Hello, *{user}*. Thanks for your message, let me echo it back to you:\n"
                            f"> {text}"
                }
            },
            {
			    "type": "divider"
		    },
            {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": "I can also echo the reverse of your message, trying adding `revecho` somewhere in your message."
			    }
		    }
        ],
    }

    send_msg(client, msg)


def reverse_echo(user, channel, client, text):
    msg = {
        "ts": "",
        "channel": channel,
        "username": user,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"The reverse of your message is:\n"
                            f"> {text[:21:-1]}"
                }
            },
        ],
    }

    send_msg(client, msg)

# when bot name is mentioned
@app.event("app_mention")
def message(event, client):
    """
    :param event: event payload
    :param client: slack client
    :return: none
    """

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")

    if text and "revecho" in text:
        return reverse_echo(user_id, channel_id, client, text)
    elif text and "echo" in text:
        return echo_cmd(user_id, channel_id, client, text)
    else:
        return unknown_cmd(user_id, channel_id, client)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)  # port 3000