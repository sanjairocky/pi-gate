from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, text
from utils.env import get_env_variable

engines = {}
current_e = []


def gen_session(url="sqlite:///anomaly.db") -> scoped_session:
    if url not in engines:
        engine = create_engine(
            str(url), echo=get_env_variable('log.verbose', False))
        session_factory = sessionmaker(bind=engine)
        # Here we are initializing a new session
        session_maker = scoped_session(session_factory)
        session = session_maker()
        current_e.append(engine)
        engines[url] = session
    return engines[url]


with gen_session() as con:
    with open("tables.sql") as file:
        for sql in file.read().split(';'):
            con.execute(text(sql))
