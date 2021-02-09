from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from settings.settings_local import mywish_pg_engine

Base = automap_base()
engine = create_engine(mywish_pg_engine)
Base.prepare(engine, reflect=True)

AdvUser = Base.classes.account.advuser
session = Session(engine)
