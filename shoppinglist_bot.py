import sys
import time
import telepot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)
gc = gspread.authorize(credentials)
document = gc.open("test")
worksheet = document.get_worksheet(0)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        if "write" in msg['text'].lower():
            writeToSpread(chat_id, msg['text'])  
        elif "get" in msg['text'].lower():
            bot.sendMessage( chat_id, getList( ) )
        elif "unregister" in msg['text'].lower():
            bot.sendMessage( chat_id, unregisterChat( ) )	
        elif "info" in msg['text'].lower():
            bot.sendMessage( chat_id, showInfo( ) )
        elif "delete" in msg['text'].lower():
            bot.sendMessage( chat_id, newList( ) )

def newList():
    worksheetNew = document.add_worksheet(title=str(time.time()), rows="300", cols="1")
    worksheetNew.update_cell(1, 1, "---Einkaufsliste---")
    document.del_worksheet(worksheet)

    return "Neue Liste angelegt"

#saves all chat ids that should be informed of events
def getList():
    ekList = worksheet.col_values(1)
    msg = ""
    for cell in ekList:
        msg += str(cell) + "\n"
    return msg

#deletes chat id from inform list
def unregisterChat():
	#TODO: remove chatID from persistent list
	return "Chat gelöscht"

def showInfo():
	infoText = "get [Name des Objekts] --- Zeigt den aktuellen Wert des Fhem Objekts \nshow [Suchbegriff] --- Zeigt alle Fhem Objekte, die den Suchbegriff beinhalten \nregister --- Registriert den Benutzer als zukünftigen Empfänger von Ereignissen \ndelete --- Entfernt den Benutzer aus der Liste der Empfänger von Ereignissen \ninfo --- Zeigt diese Hilfe an \n "
	return infoText

def writeToSpread(ID, text):
    entry = text.replace('write ','')
    values_list = worksheet.col_values(1)
    
    found = 0
    items = []
    for value in values_list:
        #rint(entry.lower() + " : " + str(value).lower())
        if entry.lower() in str(value).lower():
            found = 1
            cell = worksheet.find(str(value))
            items.append(cell)
    
    if found == 1:
        for item in items:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text=item.value, callback_data='replace' + str(item.row) + " " + str(item.col))],
               ])           
            bot.sendMessage( ID, "Ersetzen?" , reply_markup=keyboard )
    
    i=2
    while( worksheet.cell(i, 1).value ):
        i = i+1
        cell = worksheet.cell(i, 1).value

    worksheet.update_cell(i, 1, entry)

    bot.sendMessage( ID, "Eingetragen")

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': handle,'callback_query': on_callback_query})
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)