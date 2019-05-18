# Date: 05/05/2018
# Author: Mohamed
# Description: Session Handler

import json
import sqlite3
from os import remove
from sys import version_info
from lib.const import db_path
from os.path import exists as path
from csv import DictWriter, DictReader


class DatabaseWrapper:

    def __init__(self, db_name):
        self.db_name = db_name

    def db_query(self, cmd, args=[], fetchone=True):
        database = sqlite3.connect(self.db_name)
        sql = database.cursor().execute(cmd, args)
        data = sql.fetchone()[0] if fetchone else sql.fetchall()
        database.close()
        return data

    def db_execute(self, cmd, args=[]):
        database = sqlite3.connect(self.db_name)
        database.cursor().execute(cmd, args)
        database.commit()
        database.close()


class Session(DatabaseWrapper):

    is_busy = False

    def __init__(self, fingerprint):
        super().__init__(db_path)
        self.fingerprint = fingerprint
        self.create_tables()

    def create_tables(self):
        self.db_execute('''
        CREATE TABLE IF NOT EXISTS
        Session(
            session_id TEXT,
            attempts INTEGER,
            list TEXT,

            PRIMARY KEY(session_id)
        );
        ''')

    @property
    def exists(self):
        return self.db_query('SELECT COUNT(*) FROM Session WHERE session_id=?;', [self.fingerprint])

    def read(self):

        if not self.exists:
            return 0, []

        attempts, list = self.db_query('''
        SELECT attempts, list
        FROM Session
        WHERE session_id=?
        ''', args=[self.fingerprint], fetchone=False)[0]

        return attempts, json.loads(list)

    def _write(self, attempts, _list):

        if not self.exists:
            self.db_execute('''
            INSERT INTO Session(session_id, attempts, list)
            VALUES(?, ?, ?);
            ''', args=[self.fingerprint, attempts, json.dumps(_list)])
            return

        self.db_execute('''
            UPDATE Session 
            SET attempts=?, list=?
            WHERE session_id=?;
            ''', args=[attempts, json.dumps(_list), self.fingerprint])

    def write(self, attempts, _list):
        if not attempts:
            return

        while Session.is_busy:
            pass

        try:
            Session.is_busy = True
            self._write(attempts, _list)
        except:
            pass
        finally:
            Session.is_busy = False

    def delete(self):
        if self.exists:
            self.db_execute('''
            DELETE FROM Session
            WHERE session_id=?;
            ''', args=[self.fingerprint])
