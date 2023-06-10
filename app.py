import logging
from slack_bolt import App
import datetime
import time
import os
import openai

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


def help_cmd(user, channel, client, bot_id):
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
				    "text": f"Hello, <@{user}>, I'm BuddyBot. I can assist you in various ways.\n"
			    }
		    },
            {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": f"Use `echo` to repeat your message, e.g. `<@{bot_id}> echo hello`.\n"
                            f"Use `revecho` to repeat the reverse of your message, e.g. `<@{bot_id}> revecho hello`.\n"
                            f"Use `remind me` to set a same-day reminder, e.g. `<@{bot_id}> remind me at 1430`.\n"
                            f"Use `remind everyone` to ping everyone at a time, e.g. `<@{bot_id}> remind everyone at 1430`.\n"
                            f"Use `gpt` to get a response powered by GPT-3.5, e.g. `<@{bot_id}> gpt What is life?`.\n"
			    }
		    },
		    {
			    "type": "section",
			    "text": {
				    "type": "mrkdwn",
				    "text": f"See this message again at any time by using `<@{bot_id}> help`."
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

def remind_cmd(user, channel, client, text, bot_id):
    parse_time = [x for x in text.split(" ") if x.isdigit()]
    if len(parse_time) > 0 and len(parse_time[0]) == 4 and int(parse_time[0]) < 2400:
        hour = int(parse_time[0][:2])
        minute = int(parse_time[0][2:])
        target_time = datetime.time(hour, minute)
        target_time_string = target_time.strftime("%H:%M")

        if text.split()[2] == "me":
            body = f"<@{user}>, I will send you a reminder at {target_time_string}."
        elif text.split()[2] == "everyone":
            body = f"<@{user}>, I will send everyone a reminder at {target_time_string}."
        else:
            return help_cmd(user, channel, client, bot_id)

        msg = {
            "ts": "",
            "channel": channel,
            "username": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": body
                    }
                },
            ],
        }

        send_msg(client, msg)

        while datetime.datetime.now().time() < target_time:
            time.sleep(3)

        if text.split()[2] == "me":
            body = f"<@{user}>, this is your {target_time_string} reminder."
        elif text.split()[2] == "everyone":
            body = f"<!everyone>, this is your {target_time_string} reminder set by <@{user}>."
        
        msg = {
            "ts": "",
            "channel": channel,
            "username": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": body
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

# Command to get a response from OpenAI gpt-3.5-turbo
def gpt_cmd(user, channel, client, text):

    openai.api_key = os.environ['OPENAI_API_KEY']

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content" : "You’re a kind helpful bot assistant named BuddyBot in a Slack channel."},
            {"role": "user", "content": ''.join(text.split()[1:])}
        ]
    )

    reply = completion.choices[0].message.content

    msg = {
            "ts": "",
            "channel": channel,
            "username": user,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"<@{user}>, {reply}"
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

    # Get the id of the channel, user, bot, and the text of the message
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    bot_id = event.get("blocks")[0]["elements"][0]["elements"][0]["user_id"]

    print(f"\n\n\n\n {event} \n\n\n\n")

    if text and "revecho" in text:
        return reverse_echo(user_id, channel_id, client, text)
    elif text and "echo" in text:
        return echo_cmd(user_id, channel_id, client, text)
    elif text and ("remind me" in text or "remind everyone" in text):
        return remind_cmd(user_id, channel_id, client, text, bot_id)
    elif text and "gpt" in text:
        return gpt_cmd(user_id, channel_id, client, text)
    else:
        return help_cmd(user_id, channel_id, client, bot_id)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.start(3000)  # port 3000