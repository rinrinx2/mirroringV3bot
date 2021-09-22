import psycopg2
from psycopg2 import Error
from bot import AUTHORIZED_CHATS, SUDO_USERS, DB_URI, LOGGER

class DbManger:
    def __init__(self):
        self.err = False

    def connect(self):
        try:
            self.conn = psycopg2.connect(DB_URI)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as error :
            LOGGER.error("Error in dbMang : ", error)
            self.err = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_auth(self,chat_id: int):
        self.connect()
        if self.err :
            return "Ada Beberapa kesalahan silakan cek Log"
        else:
            sql = 'INSERT INTO users VALUES ({});'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.add(chat_id)
            return 'Authorized Sukses'

    def db_unauth(self,chat_id: int):
        self.connect()
        if self.err :
            return "Ada Beberapa kesalahan silakan cek Log"
        else:
            sql = 'DELETE from users where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            AUTHORIZED_CHATS.remove(chat_id)
            if chat_id in SUDO_USERS:
                SUDO_USERS.remove(chat_id)
            return 'Unauthorised Sukses'

    def db_addsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "Ada Beberapa kesalahan silakan cek Log"
        else:
            if chat_id in AUTHORIZED_CHATS:
                sql = 'UPDATE users SET sudo = TRUE where uid = {};'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                SUDO_USERS.add(chat_id)
                return 'Sukses mempromosikan Sudo'
            else:
                sql = 'INSERT INTO users VALUES ({},TRUE);'.format(chat_id)
                self.cur.execute(sql)
                self.conn.commit()
                self.disconnect()
                AUTHORIZED_CHATS.add(chat_id)
                SUDO_USERS.add(chat_id)
                return 'Sukses menambahkan dan mempromosikan Sudo'

    def db_rmsudo(self,chat_id: int):
        self.connect()
        if self.err :
            return "There's some error check log for details"
        else:
            sql = 'UPDATE users SET sudo = FALSE where uid = {};'.format(chat_id)
            self.cur.execute(sql)
            self.conn.commit()
            self.disconnect()
            SUDO_USERS.remove(chat_id)
            return 'Sukses menhapus Sudo'
