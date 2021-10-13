from sqlalchemy import create_engine

engine = create_engine('sqlite:///name.db?check_same_thread=False', echo=True)
