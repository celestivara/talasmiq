# YouTube Subscriber Notifier Bot

## Description

This is a Telegram bot that notifies you about the changes in the subscriber count of a given YouTube channel.

## Features

- **Real-time notification** of subscriber count changes
- **Customizable update interval**
- Can be used in **individual and group chats**
- **Secure setup** with a secret code (optional)

## Prerequisites

- Python 3.x
- `telegram` package
- `google-api-python-client` package

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/celestivara/talasmiq.git
    ```

2. **Install required packages**

    ```bash
    pip install python-telegram-bot google-api-python-client
    ```

3. **Run the bot**

    ```bash
    python main.py
    ```

## Usage

1. **Start the bot** in a Telegram chat with the `/start` command. Optionally, provide a secret code if you've set one.

    ```
    /start SECRET_CODE
    ```

    *This command can be used in individual and group chats.*

2. **Set the update interval** in seconds using the `/set_interval` command. For example, to set the interval to 10 minutes:

    ```
    /set_interval 600
    ```
