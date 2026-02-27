#!/bin/bash

# Script to send wakeup call message

CHAT_ID="telegram:8767222461"  # Replace with current chat ID

TIME=$(date +"%I:%M %p")
LOCATION="Bethel Island"  # You can update location dynamically if needed
WEATHER="clear sky, 20.4°C"  # Replace with dynamic weather fetching logic if available

MESSAGE="Good Morning. It’s $TIME. The weather in $LOCATION is $WEATHER."

# Send the message using the message tool CLI or API
openclaw message send --target "$CHAT_ID" --message "$MESSAGE"
