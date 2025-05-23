import os
import json
import secrets
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

# Rutas y archivos
PASSWORDS_DIR = 'passwords'
MASTER_FILE = os.path.join(PASSWORDS_DIR, 'master.txt')
FAVORITES_FILE = os.path.join(PASSWORDS_DIR, 'favorites.json')

# Asegurar existencia de carpetas y archivos
if not os.path.exists(PASSWORDS_DIR):
    os.makedirs(PASSWORDS_DIR)

if not os.path.exists(MASTER_FILE):
    with open(MASTER_FILE, 'wb') as f:
        pass

if not os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump([], f)

def cargar_clave():
    """Leer o crear clave de cifrado (usamos master password para derivar clave simple)"""
    if os.path.getsize(MASTER_FILE) == 0:
        return None
    with open(MASTER_FILE, 'rb') as f:
        master_password = f.read()
    # Para simplicidad, derivamos clave fija con Fernet usando master_password (debe tener 32 bytes)
    # Aquí simplificamos, solo codificamos master_password a base64 de 32 bytes
    key = (master_password * 32)[:32]  # aseguramos 32 bytes
    key = key.ljust(32, b'0')
    key_b64 = secrets.token_urlsafe(32).encode()  # Mejor: generamos una clave fija real si quieres
    # Pero para que funcione, usamos una clave fija:
    key = Fernet.generate_key()
    return key

# Para este demo, usaremos clave fija para cifrado. En producción se debe derivar de la master password
CIPHER_KEY = Fernet.generate_key()
fernet = Fernet(CIPHER_KEY)

@app.route('/')
def index():
    # Si no hay master, redirigir a registro
    if os.path.getsize(MASTER_FILE) == 0:
        return redirect(url_for('register'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Permite crear un nuevo master password (sobrescribe)
    if request.method == 'POST':
        new_master = request.form.get('master_password')
        if not new_master or len(new_master) < 6:
            flash("La contraseña maestra debe tener al menos 6 caracteres", "error")
            return redirect(url_for('register'))
        with open(MASTER_FILE, 'wb') as f:
            f.write(new_master.encode())
        # Limpia favoritos al crear nueva master para evitar confusión
        with open(FAVORITES_FILE, 'w') as f:
            json.dump([], f)
        flash("Contraseña maestra creada correctamente", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_master = request.form.get('master_password')
        with open(MASTER_FILE, 'rb') as f:
            stored_master = f.read()
        if entered_master.encode() == stored_master:
            return redirect(url_for('generator'))
        else:
            flash("Contraseña maestra incorrecta", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/generator', methods=['GET', 'POST'])
def generator():
    favorites = []
    with open(FAVORITES_FILE, 'r') as f:
        favorites = json.load(f)

    generated_password = None

    if request.method == 'POST':
        length = int(request.form.get('length', 12))
        include_upper = bool(request.form.get('uppercase'))
        include_lower = bool(request.form.get('lowercase'))
        include_digits = bool(request.form.get('digits'))
        include_symbols = bool(request.form.get('symbols'))
        add_to_fav = bool(request.form.get('add_to_fav'))

        chars = ''
        if include_upper:
            chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        if include_lower:
            chars += 'abcdefghijklmnopqrstuvwxyz'
        if include_digits:
            chars += '0123456789'
        if include_symbols:
            chars += '!@#$%^&*()-_=+[]{}|;:,.<>?'

        if not chars:
            flash("Selecciona al menos un tipo de caracter", "error")
            return redirect(url_for('generator'))

        generated_password = ''.join(secrets.choice(chars) for _ in range(length))

        if add_to_fav:
            if generated_password not in favorites:
                favorites.append(generated_password)
                with open(FAVORITES_FILE, 'w') as f:
                    json.dump(favorites, f)
                flash("Contraseña añadida a favoritos", "success")
            else:
                flash("La contraseña ya está en favoritos", "info")

    return render_template('generator.html', generated_password=generated_password, favorites=favorites)

@app.route('/download_favorites')
def download_favorites():
    with open(FAVORITES_FILE, 'r') as f:
        favorites = json.load(f)

    if not favorites:
        flash("No hay contraseñas favoritas para descargar", "error")
        return redirect(url_for('generator'))

    filename = 'favoritos.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for pw in favorites:
            f.write(pw + '\n')

    return send_file(filename, as_attachment=True)

@app.route('/clear_favorites')
def clear_favorites():
    with open(FAVORITES_FILE, 'w') as f:
        json.dump([], f)
    flash("Lista de favoritos vaciada", "success")
    return redirect(url_for('generator'))

if __name__ == '__main__':
    app.run(debug=True)
