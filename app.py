import logging
from slack_bolt import App
import datetime
import time

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


def help_cmd(user, channel, client):
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
				    "text": f"Hello, <@{user}>, I'm BuddyBot. I can assist you in various ways."
                            f"Use `@BuddyBot echo` to echo your message back to you, e.g. `@Buddybot echo hello`."
                            f"Use `@BuddyBot revecho` to echo the reverse of your message back to you, e.g. `@Buddybot revecho hello`."
                            f"Use `@BuddyBot remind me at` to set a same-day reminder, e.g. `@Buddybot remind me at 1430`."
			    }
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": "See this message again at any time by using `@BuddyBot help`."
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
                    "text": f"Hello, <@{user}>. Thanks for your message, let me echo it back to you:\n"
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
                    "text": f"<@{user}>, the reverse of your message is:\n"
                            f"> {text[:21:-1]}"
                }
            },
        ],
    }

    send_msg(client, msg)

def remind_cmd(user, channel, client, text):
    parse_time = [x for x in text.split(" ") if x.isdigit()]
    if len(parse_time) > 0 and len(parse_time[0]) == 4 and int(parse_time[0]) < 2400:
        hour = int(parse_time[0][:2])
        minute = int(parse_time[0][2:])
        target_time = datetime.time(hour, minute)
        target_time_string = target_time.strftime("%H:%M")

        msg = {
            "ts": "",
            "channel": channel,
            "username": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user}>, I will send you a reminder at {target_time_string}."
                    }
                },
            ],
        }

        send_msg(client, msg)

        while datetime.datetime.now().time() < target_time:
            time.sleep(3)
        msg = {
            "ts": "",
            "channel": channel,
            "username": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user}>, this is your {target_time_string} reminder."
                    }
                },
            ],
        }

        send_msg(client, msg)
    else:
        msg = {
            "ts": "",
            "channel": channel,
            "username": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user}>, If you wish to set a same-day reminder, please use the format `remind me HHMM`, for instance, to set a reminder for 2:00pm, use `remind me 1400`."
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
    elif text and "remind me" in text:
        return remind_cmd(user_id, channel_id, client, text)
    else:
        return help_cmd(user_id, channel_id, client)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)  # port 3000