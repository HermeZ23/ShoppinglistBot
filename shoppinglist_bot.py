import sys
import time
import telepot
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
    	if "write" in msg['text'].lower():
    		writeToSpread(chat_id, msg['text'])  
    	elif "register" in msg['text'].lower():
    		bot.sendMessage( chat_id, registerChat( ) )
    	elif "delete" in msg['text'].lower():
    		bot.sendMessage( chat_id, unregisterChat( ) )	
    	elif "info" in msg['text'].lower():
    		bot.sendMessage( chat_id, showInfo( ) )



#saves all chat ids that should be informed of events
def registerChat():
	#TODO: persistent list of all chatIDs
	return "Chat Registriert"

#deletes chat id from inform list
def unregisterChat():
	#TODO: remove chatID from persistent list
	return "Chat gelöscht"

def showInfo():
	infoText = "get [Name des Objekts] --- Zeigt den aktuellen Wert des Fhem Objekts \nshow [Suchbegriff] --- Zeigt alle Fhem Objekte, die den Suchbegriff beinhalten \nregister --- Registriert den Benutzer als zukünftigen Empfänger von Ereignissen \ndelete --- Entfernt den Benutzer aus der Liste der Empfänger von Ereignissen \ninfo --- Zeigt diese Hilfe an \n "
	return infoText

def writeToSpread(ID, text):
    gc = gspread.authorize(credentials)
    wks = gc.open("test").sheet1

    i=1
    while( wks.cell(i, 1).value ):
        i = i+1
        cell = wks.cell(i, 1).value
        print("i: " + str(i) + str(cell))

    wks.update_cell(i, 1, text.replace('write ',''))

    bot.sendMessage( ID, "Eingetragen"  )



TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)