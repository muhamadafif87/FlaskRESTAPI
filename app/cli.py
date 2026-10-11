import click

from app.extensions import db
from app.models.user import User


@click.command("create-admin")
@click.option("--username", prompt=True)
@click.option("--email", prompt=True)
@click.password_option()
def create_admin(username, email, password):
    """Untuk membuat akun admin.  Jalankan: flask --app run create-admin"""
    ada = db.session.scalar(
        db.select(User).where((User.username == username) | (User.email == email))
    )
    if ada:
        click.echo("Username atau email sudah dipakai.")
        return

    user = User(username=username, email=email, role="admin")
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Admin '{username}' berhasil dibuat.")
