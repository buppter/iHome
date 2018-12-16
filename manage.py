from ihome import creat_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


# 创建flask应用对象
app = creat_app('development')
manager = Manager(app)

Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
