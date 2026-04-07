import ast

# The raw data string from your file/output
raw_data_string = "{'adm_in_groups': 0, 'is_bot': False, 'last_msg_date': '2026-04-07T02:12:16Z', 'names_count': 2, 'total_groups': 10, 'total_msg_count': 724}"

# Safely evaluate the string into a Python dictionary
user_data = ast.literal_eval(raw_data_string)

# Extract specific details to use in your bot
is_bot = user_data.get('is_bot')
total_messages = user_data.get('total_msg_count')
total_groups = user_data.get('total_groups')
last_active = user_data.get('last_msg_date')

# Format the response message for the bot to send
bot_reply = (
    f"📊 **User Statistics:**\n"
    f"🤖 Is Bot: {is_bot}\n"
    f"💬 Total Messages: {total_messages}\n"
    f"👥 Groups: {total_groups}\n"
    f"📅 Last Message: {last_active}"
)

print(bot_reply)
