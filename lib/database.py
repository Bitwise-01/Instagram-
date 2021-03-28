# Date: 05/05/2018
# Author: Mohamed
# Description: Session Handler

import json
import sqlite3

# from os import remove
# from sys import version_info
from lib.const import db_path
from os.path import exists as path

# from csv import DictWriter, DictReader
import hashlib
import time
import typing


class DatabaseWrapper:
    def __init__(self, db_name):
        self.db_name = db_path

    def db_query(self, cmd, args=[], fetchone=True):
        database = sqlite3.connect(self.db_name, timeout=30)
        database.cursor().execute("PRAGMA FOREIGN_KEYS = ON;")
        sql = database.cursor().execute(cmd, args)
        data = sql.fetchone()[0] if fetchone else sql.fetchall()
        database.close()
        return data

    def db_execute(self, cmd, args=[]):
        database = sqlite3.connect(self.db_name, timeout=30)
        database.cursor().execute("PRAGMA FOREIGN_KEYS = ON;")
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
        self.db_execute(
            """
        CREATE TABLE IF NOT EXISTS
        Session(
            session_id TEXT,
            attempts INTEGER,
            list TEXT,

            PRIMARY KEY(session_id)
        );
        """
        )

    @property
    def exists(self):
        return self.db_query(
            "SELECT COUNT(*) FROM Session WHERE session_id=?;",
            [self.fingerprint],
        )

    def read(self):

        if not self.exists:
            return 0, []

        attempts, list = self.db_query(
            """
        SELECT attempts, list
        FROM Session
        WHERE session_id=?
        """,
            args=[self.fingerprint],
            fetchone=False,
        )[0]

        return attempts, json.loads(list)

    def _write(self, attempts, _list):

        if not self.exists:
            self.db_execute(
                """
            INSERT INTO Session(session_id, attempts, list)
            VALUES(?, ?, ?);
            """,
                args=[self.fingerprint, attempts, json.dumps(_list)],
            )
            return

        self.db_execute(
            """
            UPDATE Session 
            SET attempts=?, list=?
            WHERE session_id=?;
            """,
            args=[attempts, json.dumps(_list), self.fingerprint],
        )

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
            self.db_execute(
                """
            DELETE FROM Session
            WHERE session_id=?;
            """,
                args=[self.fingerprint],
            )


class Proxy(DatabaseWrapper):
    def __init__(self):
        super().__init__(db_path)
        self.create_tables()

    def create_tables(self) -> None:
        self.db_execute(
            """
        CREATE TABLE IF NOT EXISTS
        Proxy(
            proxy_id TEXT,
            ip TEXT,
            port INTEGER,
            
            PRIMARY KEY(proxy_id)
        );
        """
        )

        self.db_execute(
            """
        CREATE TABLE IF NOT EXISTS
        ProxyStatus(
            proxy_status_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            time_added FLOAT, 
            last_used FLOAT,
            last_updated FLOAT, 
            total_used INTEGER DEFAULT 1,
            total_passed INTEGER DEFAULT 0,
            proxy_id TEXT,

            FOREIGN KEY(proxy_id) REFERENCES Proxy(proxy_id) ON DELETE CASCADE
        );
        """
        )

    def __get_signature(self, *, ip: str, port: int) -> str:
        return hashlib.sha256(f"{ip}::{port}".encode()).hexdigest()

    def __exists(self, proxy_id: str) -> bool:
        """Returns True if a proxy by the given proxy id exists"""

        return (
            self.db_query(
                "SELECT COUNT(*) FROM Proxy WHERE proxy_id=?;",
                [proxy_id],
            )
            != 0
        )

    def add_proxy(self, *, ip: str, port: int) -> str:
        """Add a proxy into the database.

        Returns: proxy_id when successful
        """

        # preprocess
        ip = ip.strip()
        proxy_id = self.__get_signature(ip=ip, port=port)

        # check for existance
        if self.__exists(proxy_id):
            return None

        # add to database
        self.db_execute(
            """
        INSERT INTO Proxy(proxy_id, ip, port)
        VALUES(?, ?, ?);
        """,
            args=[proxy_id, ip, port],
        )

        self.db_execute(
            """
        INSERT INTO ProxyStatus(
            time_added, 
            proxy_id
        )
        VALUES(?, ?);
        """,
            args=[time.time(), proxy_id],
        )

        return proxy_id

    def delete_proxy(self, proxy_id: str) -> bool:
        """Delete a proxy from the database

        Returns:
            True: if proxy has been deleted
        """

        if not self.__exists(proxy_id):
            return False

        self.db_execute(
            """
        DELETE FROM Proxy
        WHERE proxy_id=?;
        """,
            args=[proxy_id],
        )

    def __parse_proxy(self, proxy_data: tuple) -> dict:
        """Get a tuple of proxy and turns it into a dict."""

        return {
            "ip": proxy_data[1],
            "port": proxy_data[2],
            "time_added": proxy_data[4],
            "last_used": proxy_data[5],
            "last_updated": proxy_data[6],
            "total_used": proxy_data[7],
            "total_passed": proxy_data[8],
            "score": proxy_data[10],
        }

    def get_proxy(self, proxy_id: str) -> dict:
        """Get details of a proxy with the given proxy id"""

        if not self.__exists(proxy_id):
            return {}

        proxy_data = self.db_query(
            """
        SELECT *, 
            (CAST(ProxyStatus.total_passed AS FLOAT) / CAST(ProxyStatus.total_used AS FLOAT)) AS score
        FROM Proxy
        INNER JOIN ProxyStatus on ProxyStatus.proxy_id = Proxy.proxy_id
        WHERE Proxy.proxy_id=?;
        """,
            args=[proxy_id],
            fetchone=False,
        )[0]

        return self.__parse_proxy(proxy_data)

    def get_proxies(
        self, offset: int = 0, limit: int = 256, min_score: float = 0.0
    ) -> typing.List[dict]:
        rows = self.db_query(
            """
        SELECT *, 
            (CAST(ProxyStatus.total_passed AS FLOAT) / CAST(ProxyStatus.total_used AS FLOAT)) AS score
            
        FROM Proxy
        INNER JOIN ProxyStatus on ProxyStatus.proxy_id = Proxy.proxy_id
        WHERE (CAST(ProxyStatus.total_passed AS FLOAT) / CAST(ProxyStatus.total_used AS FLOAT)) >= ?
        ORDER BY 
            score DESC,
            time_added DESC
        LIMIT ?, ?;
        """,
            fetchone=False,
            args=[min_score, offset, limit],
        )

        return [self.__parse_proxy(row) for row in rows]

    def update_status(
        self,
        ip: str,
        port: int,
        last_used: float,
        total_used: int,
        total_passed: int,
    ) -> bool:
        proxy_id = self.__get_signature(ip=ip, port=port)

        if not self.__exists(proxy_id):
            return False

        self.db_execute(
            """
            UPDATE ProxyStatus 
            SET 
                last_used = ?, 
                last_updated = ?,
                total_used = total_used + ?, 
                total_passed = total_passed + ?
            WHERE proxy_id=?;
            """,
            args=[last_used, time.time(), total_used, total_passed, proxy_id],
        )

        return True

    def prune(self, threshold: float) -> int:
        before_rows = self.db_query(
            """
            SELECT COUNT(*) 
            FROM Proxy;
        """
        )

        self.db_execute(
            """
        DELETE 
        FROM Proxy

        WHERE proxy_id IN (
            SELECT Proxy.proxy_id
            FROM Proxy
            INNER JOIN ProxyStatus on ProxyStatus.proxy_id = Proxy.proxy_id
            WHERE (CAST(ProxyStatus.total_passed AS FLOAT) / CAST(ProxyStatus.total_used AS FLOAT)) < ?
        );
        """,
            args=[threshold],
        )

        after_rows = self.db_query(
            """
        SELECT COUNT(*) 
        FROM Proxy;
        """
        )

        return before_rows - after_rows

    def calc_q1(self) -> float:
        """Calculate the first quartile of the scores."""

        scores = self.db_query(
            """
        SELECT score
        FROM 
            (
                SELECT 
                    (CAST(ProxyStatus.total_passed AS FLOAT) / CAST(ProxyStatus.total_used AS FLOAT)) AS score
                FROM Proxy
                INNER JOIN ProxyStatus on ProxyStatus.proxy_id = Proxy.proxy_id
            )
        ORDER BY 
            score ASC;
        """,
            fetchone=False,
        )

        q1 = 0.0

        if scores[0][0]:
            scores = [score[0] for score in scores]
            mid = len(scores) / 2

            if isinstance(mid, float):
                mid = int(mid)
                q1 = (scores[mid] + scores[mid + 1]) / 2
            else:
                q1 = (sum(scores[:mid]) / mid) if mid else q1

        return q1

    def stats(self) -> dict:
        data = {"total": 0, "q1": 0.0, "avg": 0.0, "min": 0, "max": 0}

        rows = self.db_query(
            """
        SELECT 
            COUNT(score) AS total_proxies, 
            AVG(score) AS avg_score, 
            MIN(score) AS min_score, 
            MAX(score) AS max_score
        FROM 
            (
                SELECT 
                    (CAST(ProxyStatus.total_passed AS FLOAT) / CAST(ProxyStatus.total_used AS FLOAT)) AS score
                FROM Proxy
                INNER JOIN ProxyStatus on ProxyStatus.proxy_id = Proxy.proxy_id
            );
        """,
            fetchone=False,
        )

        if rows[0][0]:
            row = rows[0]
            data["total"] = row[0]
            data["avg"] = row[1]
            data["min"] = row[2]
            data["max"] = row[3]
            data["q1"] = self.calc_q1()

        return data
