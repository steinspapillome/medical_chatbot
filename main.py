from doctors_database import Database
from input_output import IO
from classifier import Classifier
from TelegramAPI import TelegramBot
# from dialoger import Dialoger
def main():
    PATH_DATABASE = 'data/database.db'
    PATH_SYMPTOMS = 'data/symptoms.json'
    BOT_TOKEN = input("please, write bot token:")
    
    db = Database(PATH_DATABASE)
    clf = Classifier(db.get_all_names(), db.get_symps_dict())
    bot = TelegramBot(BOT_TOKEN, clf, db)
    bot.dialog()

if __name__ == '__main__':
    main()
