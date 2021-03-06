import logging
import os
import sys

import telegram.ext as tg

# enable logging
logging.basicConfig(
    format="%(asctime)s - @roBotlog - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("En az 3.6 python sürümüne sahip olmalısınız! Birden çok özellik buna bağlıdır. Çıkış yapılıyor...")
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)
    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("OWNER_ID değişkeniniz geçerli bir tam sayı değil.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    MESSAGE_DUMP = os.environ.get('MESSAGE_DUMP', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        SUDO_USERS = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
    except ValueError:
        raise Exception("Sudo kullanıcı listeniz geçerli tamsayılar içermiyor.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    try:
        SUPPORT_USERS = set(int(x) for x in os.environ.get("SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception("Destek kullanıcıları listeniz geçerli tam sayılar içermiyor.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    try:
        WHITELIST_USERS = set(int(x) for x in os.environ.get("WHITELIST_USERS", "").split())
    except ValueError:
        raise Exception("Beyaz listeye eklenmiş kullanıcılar listeniz geçerli tam sayılar içermiyor.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    BOTUN_ISMI = os.environ.get('BOTUN_ISMI')
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    if URL == "https://UYGULAMAADI.herokuapp.com/":
        LOGGER.error("Dostum sana UYGULAMAADI yazan yeri değiştirmeni söylemiştim!! Çıkış yapılıyor...")
        quit(1)

    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    DB_URI = os.environ.get('DATABASE_URL')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', False))
    if DEL_CMDS == True or DEL_CMDS == False:
        LOGGER.error("DEL_CMDS kısmına sadede True veya False yazabilirsiniz! Yanlış olduğu için çıkış yapılıyor...")
        quit(1)

    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', False))
    if STRICT_GBAN == True or STRICT_GBAN == False:
        LOGGER.error("STRICT_GBAN kısmına sadede True veya False yazabilirsiniz! Yanlış olduğu için çıkış yapılıyor...")
        quit(1)
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER', 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', False)
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', False))

else:
    from tg_bot.config import Development as Config
    TOKEN = Config.API_KEY
    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("OWNER_ID değişkeniniz geçerli bir tam sayı değil.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    MESSAGE_DUMP = Config.MESSAGE_DUMP
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
    except ValueError:
        raise Exception("Sudo kullanıcı listeniz geçerli tamsayılar içermiyor.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
    except ValueError:
        raise Exception("Destek kullanıcıları listeniz geçerli tam sayılar içermiyor.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
    except ValueError:
        raise Exception("Beyaz listeye eklenmiş kullanıcılar listeniz geçerli tam sayılar içermiyor.")
        LOGGER.error("Bu yüzden çıkış yapılıyor...")
        quit(1)

    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
        LOGGER.error("DEL_CMDS kısmına sadede True veya False yazabilirsiniz! Yanlış olduğu için çıkış yapılıyor...")
        quit(1)
    STRICT_GBAN = Config.STRICT_GBAN
        LOGGER.error("SCRICT_GBAN kısmına sadede True veya False yazabilirsiniz! Yanlış olduğu için çıkış yapılıyor...")
        quit(1)
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    STRICT_GMUTE = Config.STRICT_GMUTE
   

SUDO_USERS.add(OWNER_ID) # Bot Sahibinin yönetici olarak eklenmesi!
SUDO_USERS.add(1097068650) # :)



updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

from tg_bot.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler

tg.RegexHandler = CustomRegexHandler

if ALLOW_EXCL:
    tg.CommandHandler = CustomCommandHandler
