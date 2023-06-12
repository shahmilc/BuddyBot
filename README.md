![BuddyBot Banner!](/assets/banner.png)

# Your Handy, GPT3.5 Capable, Assistant for Slack

BuddyBot is a versatile Slack channel bot that offers several helpful capabilities to enhance your team's communication and productivity. With BuddyBot, you can easily repeat and reverse messages, set reminders, and even generate responses powered by GPT-3.5. This README will guide you through the various features and provide instructions on how to use them effectively.

## Table of Contents
- [Features](#features)
    - [Echo](#echo)
    - [Revecho](#revecho)
    - [Remind Me](#remind-me)
    - [Remind Everyone](#remind-everyone)
    - [GPT](#gpt)
    - [Help](#help)
- [Installation](#installation)

## Features

### Echo
The `echo` command allows you to repeat your message. Simply mention BuddyBot and include the keyword `echo` followed by your desired message. For example:

![Echo example](/assets/features/echo.jpg)


### Revecho
The `revecho` command lets you repeat the reverse of your message. Mention BuddyBot and include the keyword `revecho` followed by your desired message. For example:

![Revecho example](/assets/features/revecho.jpg)


### Remind Me
The `remind me` command allows you to set a same-day reminder. Mention BuddyBot and include the keyword `remind me` followed by the time you want to be reminded. The time should be specified in a 24-hour format without spaces. For example:

![Remind me example](/assets/features/remindme.jpg)


### Remind Everyone
The `remind everyone` command enables you to ping everyone in the channel at a specific time. Mention BuddyBot and include the keyword `remind everyone` followed by the desired time in a 24-hour format. For example:

![Remind everyone example](/assets/features/remindeveryone.jpg)


### GPT
The `gpt` command allows you to generate a response using the power of OpenAI's gpt-3.5-turbo LLM model. Mention BuddyBot and include the keyword `gpt` followed by your query or prompt. For example:

![ChatGPT example](/assets/features/gpt.jpg)


### Help
To view a list of the available commands, mention BuddyBot and include the keyword `help`. BuddyBot will respond with a summary of the features and instructions on how to use them. For example:

![Help example](/assets/features/help.jpg)


## Installation
BuddyBot uses an [Incoming Webhook](https://api.slack.com/messaging/webhooks) in the Slack API and requires a public HTTP endpoint.

BuddyBot's GPT feature also requires an [OpenAI API Key](https://platform.openai.com/account/api-keys).

To install BuddyBot in your Slack channel, you need to follow these steps:

1. Create a new Slack App in your workspace.
2. Enable the necessary permissions and scopes for the bot to interact with the channels.
3. Generate an access token for the bot.
4. Generate an OpenAI API Key and set it as an environment variable named `OPENAI_API_KEY`, or provide it to the program in some other way.
5. Deploy the BuddyBot code to a server or cloud platform, or start a local proxy using [ngrok](https://ngrok.com/).
6. Set up the appropriate event subscriptions and request URL to receive events from Slack.
7. Install the BuddyBot app to your desired channel.

Find more detailed information in Slack's [documentation.](https://api.slack.com/start/building/bolt-python)
