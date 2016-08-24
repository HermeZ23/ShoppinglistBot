import sys
import time
import telepot

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
    	if "get" in msg['text'].lower():
    		bot.sendMessage( chat_id, getValue( msg['text'].lower() ) )  
    	elif "show" in msg['text'].lower():
    		bot.sendMessage( chat_id, getFhemObjects( msg['text'].lower() ) )
    	elif "register" in msg['text'].lower():
    		bot.sendMessage( chat_id, registerChat( ) )
    	elif "delete" in msg['text'].lower():
    		bot.sendMessage( chat_id, unregisterChat( ) )	
    	elif "info" in msg['text'].lower():
    		bot.sendMessage( chat_id, showInfo( ) )


#returns value of a fhem object
def getValue(text):
	fhemObject = text.split()[-1]
	return "getValue"

#returns all fhem objects
def getFhemObjects(text):
	fhemObject = text.split()[-1]
	#TODO: get FHEM objects containing
	return "showObjects"

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



TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)