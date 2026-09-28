from app import create_app
import click

app = create_app()

@app.cli.command('db-init')
def init_db():
    """Initialize database with tables."""
    with app.app_context():
        from app.models import db
        db.create_all()
        print('Database initialized successfully.')

@app.cli.command('db-migrate')
@click.argument('message')
def migrate(message):
    """Stub for migration."""
    print(f'Migration stub - message: {message}')

@app.cli.command('db-upgrade')
def upgrade():
    """Stub for upgrade."""
    print('Upgrade stub ready.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
