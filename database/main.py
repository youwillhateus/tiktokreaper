import os
import re
from typing import Dict, List, Union, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


from Database.models import TikTokAccount

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(CURRENT_FILE_DIR, '..', ".env"))

DATABASE_HOST=os.getenv("DATABASE_HOST")
DATABASE_PORT=os.getenv("DATABASE_PORT")
DATABASE_USERNAME=os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_DBNAME")

EMAIL_RE_SIMPLE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

for _ in [DATABASE_PASSWORD,DATABASE_USERNAME,DATABASE_PORT,DATABASE_HOST, DATABASE_NAME]:
    if _ is None:
        print('ERROR',"Missing environment variable for Database Credentials. Some variables are None, there might be a misconfiguration with .env file or it is not loaded correctly!")
        raise Exception()


class Database(object):
    def __init__(self, db_credentials: dict | None = None) -> None:

        if db_credentials:
            global DATABASE_HOST, DATABASE_PORT, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME
            DATABASE_USERNAME = db_credentials['username']
            DATABASE_PASSWORD = db_credentials['password']
            DATABASE_HOST  = db_credentials['host']
            DATABASE_PORT = db_credentials['port']
            DATABASE_NAME = db_credentials['name']

        engine = create_engine(f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.connection_response = self.get_connection()

    def get_connection(self) -> Dict[str, Union[int, Dict[str, str], Session]]:
        """
        Tests database connectivity.
        Returns a dictionary with status and either a session or an error message.
        """
        try:
            db_session = self.SessionLocal()
            db_session.execute(text('SELECT 1'))  # simple query to validate connection

            return {
                "status": 200,
                "connection": db_session
            }
        except Exception as error:
            return {
                'status': 400,
                'data': {
                    'message': str(error)
                }
            }
        
    def get_all_tiktok_accounts(
        self,
        id: Optional[int] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Union[int, str, List[TikTokAccount]]]:
        """
        Retrieves all tiktok accounts or filters by provided fields.
        Each parameter is optional. If a parameter is not None and has the
        correct type, it is added as a filter condition to the query.
        """
        try:
            session: Session = self.SessionLocal()
            query = session.query(TikTokAccount)

            # Type checks and filters
            if id is not None:
                if not isinstance(id, int):
                    return {
                        "status": 400,
                        "data": {"message": "Invalid type for 'id', expected int."}
                    }
                query = query.filter(TikTokAccount.id == id)

            if username is not None:
                if not isinstance(username, str):
                    return {
                        "status": 400,
                        "data": {"message": "Invalid type for 'username', expected str."}
                    }
                query = query.filter(TikTokAccount.username == username)

            if email is not None:
                if not isinstance(email, str):
                    return {
                        "status": 400,
                        "data": {"message": "Invalid type for 'email', expected str."}
                    }
                query = query.filter(TikTokAccount.email == email)

            if password is not None:
                if not isinstance(password, str):
                    return {
                        "status": 400,
                        "data": {"message": "Invalid type for 'password', expected str."}
                    }
                query = query.filter(TikTokAccount.password == password)

            if token is not None:
                if not isinstance(token, str):
                    return {
                        "status": 400,
                        "data": {"message": "Invalid type for 'token', expected str."}
                    }
                query = query.filter(TikTokAccount.token == token)

            if status is not None:
                if not isinstance(status, str):
                    return {
                        "status": 400,
                        "data": {"message": "Invalid type for 'status', expected str."}
                    }
                query = query.filter(TikTokAccount.status == status)

            accounts: List[TikTokAccount] = query.all()

            return {
                "status": 200,
                "data": accounts
            }
        except Exception as error:
            return {
                "status": 400,
                "data": {
                    "message": str(error)
                }
            }
        finally:
            session.close()

    def insert_tiktok_account(self, account_data: Dict) -> Dict[str, Union[int, str, TikTokAccount]]:
        """
        Inserts a single account into the database.
        `account_data` must contain keys matching TikTokAccount table:
        e.g. username, email, password, and so on.
        """
        try:
            session: Session = self.SessionLocal()
            account = TikTokAccount(**account_data)

            session.add(account)
            session.commit()
            session.refresh(account)

            return {
                "status": 201,
                "data": account
            }
        except Exception as error:
            session.rollback()
            return {
                "status": 400,
                "data": {
                    "account": str(error)
                }
            }
        finally:
            session.close()