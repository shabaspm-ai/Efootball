import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# നിങ്ങളുടെ ബോട്ട് ടോക്കൺ ഇവിടെ നൽകുക
TOKEN = '8316569646:AAGi6vLJdPpqUD34P9NC8Z_OSlAc_kz-wXQ'

# നിങ്ങളുടെ ടെലിഗ്രാം യൂസർനെയിം (ഇതിൽ മാറ്റം വരുത്തരുത്)
ADMIN_USERNAME = 'PEARL_OF_TG' 

bot = telebot.TeleBot(TOKEN)

# eFootball ടീമുകളുടെ ലിസ്റ്റ് (നിങ്ങൾക്ക് ആവശ്യമുള്ള ടീമുകൾ ചേർക്കാം/മാറ്റാം)
teams = {
    "Argentina": None,
    "Brazil": None,
    "France": None,
    "England": None,
    "Spain": None,
    "Portugal": None,
    "Germany": None,
    "Netherlands": None
}

admin_state = {}

def generate_team_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for team, player in teams.items():
        if player is None:
            # ഒഴിവുള്ള ടീമുകൾ
            btn_text = f"✅ {team}"
            callback_data = f"select_{team}"
        else:
            # എടുത്ത ടീമുകൾ
            btn_text = f"❌ {team} ({player})"
            callback_data = f"taken_{team}"
        buttons.append(InlineKeyboardButton(text=btn_text, callback_data=callback_data))
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['teams'])
def send_teams(message):
    if message.from_user.username != ADMIN_USERNAME:
        bot.reply_to(message, "ഈ കമാൻഡ് ഉപയോഗിക്കാൻ നിങ്ങൾക്ക് അനുമതിയില്ല.")
        return
    bot.send_message(message.chat.id, "ടീമുകൾ താഴെ നൽകുന്നു. അഡ്മിന് മാത്രം ടീം സെലക്ട് ചെയ്യാം:", reply_markup=generate_team_markup())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    # അഡ്മിൻ അല്ലെങ്കിൽ വാണിംഗ് നൽകുക
    if call.from_user.username != ADMIN_USERNAME:
        bot.answer_callback_query(call.id, "ക്ഷമിക്കണം, അഡ്മിന് മാത്രമേ ടീം സെലക്ട് ചെയ്യാൻ സാധിക്കൂ!", show_alert=True)
        return

    data = call.data
    if data.startswith("select_"):
        team = data.split("_")[1]
        admin_state['pending_team'] = team
        admin_state['chat_id'] = call.message.chat.id
        admin_state['message_id'] = call.message.message_id
        
        msg = bot.send_message(call.message.chat.id, f"നിങ്ങൾ **{team}** സെലക്ട് ചെയ്തു. ഈ ടീം ആർക്കാണ് നൽകേണ്ടത്? (പ്ലെയറുടെ പേര് ടൈപ്പ് ചെയ്ത് അയക്കുക):", parse_mode="Markdown")
        bot.register_next_step_handler(msg, assign_team)
        bot.answer_callback_query(call.id)
        
    elif data.startswith("taken_"):
        bot.answer_callback_query(call.id, "ഈ ടീം മാറ്റൊരാൾ എടുത്തു കഴിഞ്ഞു!", show_alert=True)

def assign_team(message):
    if message.from_user.username != ADMIN_USERNAME:
        return
    
    team = admin_state.get('pending_team')
    player_name = message.text

    if team:
        teams[team] = player_name
        bot.reply_to(message, f"✅ {team} എന്ന ടീം **{player_name}**-ന് നൽകിയിരിക്കുന്നു!", parse_mode="Markdown")
        
        # പഴയ മെസ്സേജിലെ ബട്ടൺ അപ്ഡേറ്റ് ചെയ്യുന്നു
        chat_id = admin_state.get('chat_id')
        message_id = admin_state.get('message_id')
        try:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=generate_team_markup())
        except:
            pass
        
        admin_state.clear()

@bot.message_handler(commands=['list'])
def send_final_list(message):
    if message.from_user.username != ADMIN_USERNAME:
        return
    
    text = "🏆 **eFootball ടൂർണമെന്റ് ലിസ്റ്റ്:**\n\n"
    for team, player in teams.items():
        status = player if player else "ഒഴിവുണ്ട്"
        text += f"⚽ {team} : {status}\n"
    
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

# --- Render-ൽ 24/7 റൺ ചെയ്യാനുള്ള Flask കോഡ് ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running 24/7!"

def run():
    app.run(host='0.0.0.0', port=8000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Flask വെബ് സെർവറും ബോട്ടിനെയും ഒരുമിച്ച് സ്റ്റാർട്ട് ചെയ്യുന്നു
keep_alive()
bot.infinity_polling()
