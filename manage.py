# -*- coding: utf-8 -*-
from flask_script import Manager, Shell
from flask_migrate import MigrateCommand

from videona_platform.api.factory import create_app
from videona_platform.core import db
from videona_platform.promo_codes.commands import GeneratePromoCodesCommand
from videona_platform.users import models

app = create_app()


def make_shell_context():
    app.debug = True
    return dict(app=app, db=db, models=models)


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('generate_promo_codes', GeneratePromoCodesCommand())


if __name__ == '__main__':
    manager.run()
