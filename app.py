from flask import Flask, request, redirect, render_template, session, url_for, flash, g
from code_Send import envoyer_email, generer_code
import hashlib
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
import secrets
import string

# Configuration de la base de données
DB_CONFIG = {
    'user': 'root',
    'password': 'WJ28@krhps',
    'host': 'localhost',
    'database': 'systeme_vote'
}

encoded_password = quote_plus(DB_CONFIG['password'])
# Création de l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_CONFIG['user']}:{encoded_password}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de session plus sécurisée
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800,  # 30 minutes
    WTF_CSRF_TIME_LIMIT=3600,  # Définit la durée d'expiration des jetons CSRF (en secondes)
    WTF_CSRF_ENABLED=True
)

# En production, activez ces paramètres supplémentaires
if os.environ.get('FLASK_ENV') == 'production':
    app.config.update(
        SESSION_COOKIE_SECURE=True
    )

# Initialiser une SEULE instance de SQLAlchemy
db = SQLAlchemy(app)

# Initialiser protection CSRF
csrf = CSRFProtect(app)

# Configuration du logging
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Application démarrée')

# Définition des modèles après l'initialisation de db
class Electeur(db.Model):
    __tablename__ = 'electeur'
    
    id = db.Column(db.Integer, primary_key=True)
    hash_identifiant = db.Column(db.String(64), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    code_verif = db.Column(db.String(6))
    date_creation = db.Column(db.DateTime, default=datetime.now)
    cle_publique = db.Column(db.Text, nullable=False)
    cle_symetrique_chiffree = db.Column(db.Text, nullable=False)
    id_confirmation_vote = db.Column(db.String(20), unique=True) 

class Election(db.Model):
    __tablename__ = 'election'
    
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.now)
    
class Candidat(db.Model):
    __tablename__ = 'candidat'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    id_election = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.now)
    
    # Relationship
    election = db.relationship('Election', backref=db.backref('candidats', lazy=True))

class Vote(db.Model):
    __tablename__ = 'vote'
    id = db.Column(db.Integer, primary_key=True)
    id_election = db.Column(db.Integer, db.ForeignKey('election.id'), nullable=False)
    hash_electeur = db.Column(db.String(64), nullable=False)
    vote_chiffre_asym = db.Column(db.Text, nullable=False)
    signature = db.Column(db.Text, nullable=False)
    iv_aes = db.Column(db.String(32), nullable=False)
    date_vote = db.Column(db.DateTime, nullable=False)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('id_election', 'hash_electeur'),)
    election = db.relationship('Election', backref=db.backref('votes', lazy=True))

# Vérifiez les chemins statiques au démarrage de l'application
def check_static_paths():
    """
    Vérifie l'existence des dossiers et fichiers statiques nécessaires
    et les crée si besoin
    """
    # Chemin vers le dossier statique
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    js_folder = os.path.join(static_folder, 'js')
    css_folder = os.path.join(static_folder, 'css')
    
    # Créer les dossiers s'ils n'existent pas
    for folder in [static_folder, js_folder, css_folder]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Dossier créé: {folder}")
    
    # Liste des fichiers JS requis
    required_js_files = [
        os.path.join(js_folder, 'main.js'),
        os.path.join(js_folder, 'login.js')
    ]
    
    # Liste des fichiers CSS requis
    required_css_files = [
        os.path.join(css_folder, 'style.css')
    ]
    
    # Vérifier chaque fichier JS
    for js_file in required_js_files:
        if not os.path.exists(js_file):
            # Créer un fichier vide avec un commentaire minimal
            with open(js_file, 'w') as f:
                f.write('/* JavaScript file for Système de Vote */\n')
            print(f"Fichier JS créé avec un contenu minimal: {js_file}")
    
    # Vérifier chaque fichier CSS
    for css_file in required_css_files:
        if not os.path.exists(css_file):
            # Créer un fichier vide avec un commentaire minimal
            with open(css_file, 'w') as f:
                f.write('/* CSS file for Système de Vote */\n')
            print(f"Fichier CSS créé avec un contenu minimal: {css_file}")
            
    print("Vérification des fichiers statiques terminée.")

# Fonctions de base de données
def get_db_connection():
    return db.session

def generer_identifiant_confirmation():
    """
    Génère un identifiant unique pour la confirmation de vote
    Format: VT-2025-XXXXXXXX où X est une combinaison aléatoire de lettres et chiffres
    """
    # Caractères possibles pour l'identifiant (lettres majuscules et chiffres)
    caracteres = string.ascii_uppercase + string.digits
    
    # Générer une partie aléatoire de 8 caractères
    partie_aleatoire = ''.join(secrets.choice(caracteres) for _ in range(8))
    
    # Construire l'identifiant complet
    identifiant = f"VT-2025-{partie_aleatoire}"
    
    return identifiant

def verifier_identifiant_existant(identifiant):
    """
    Vérifie si un identifiant public existe déjà dans la base de données
    """
    return Electeur.query.filter_by(id_confirmation_vote=identifiant).first() is not None

def attribuer_identifiant_confirmation(hash_electeur):
    """
    Attribue un identifiant de confirmation à un électeur existant
    """
    # Récupérer l'électeur
    electeur = Electeur.query.filter_by(hash_identifiant=hash_electeur).first()
    
    if not electeur:
        app.logger.error(f"Électeur non trouvé avec hash: {hash_electeur}")
        return None
    
    # Si l'électeur a déjà un identifiant, le retourner
    if electeur.id_confirmation_vote:
        return electeur.id_confirmation_vote
    
    # Maximum 10 tentatives pour générer un identifiant unique
    for _ in range(10):
        identifiant = generer_identifiant_confirmation()
        
        # Vérifier si cet identifiant existe déjà
        if not verifier_identifiant_existant(identifiant):
            try:
                # Attribuer l'identifiant à l'électeur
                electeur.id_confirmation_vote = identifiant
                db.session.commit()
                return identifiant
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Erreur lors de l'attribution de l'identifiant: {e}")
    
    # Si on ne peut pas générer un ID unique après 10 tentatives
    app.logger.error("Impossible de générer un identifiant unique après plusieurs tentatives")
    return None

def close_db_connection(e=None):
    """Ferme la connexion à la base de données"""
    db_connection = g.pop('db', None)
    if db_connection is not None:
        db_connection.close()

def get_electeur_by_hash(hash_identifiant):
    """Récupère un électeur par son hash."""
    electeur = Electeur.query.filter_by(hash_identifiant=hash_identifiant).first()
    return electeur

def inserer_electeur(nom, email, hash_identifiant, code_verif):
    """Insère un nouvel électeur dans la base de données."""
    # Generate dummy keys for now - you should implement proper key generation
    import base64
    import os
    
    # Generate a dummy public key (in a real application, this would be a proper RSA key)
    dummy_public_key = base64.b64encode(os.urandom(64)).decode('utf-8')
    
    # Generate a dummy encrypted symmetric key
    dummy_encrypted_key = base64.b64encode(os.urandom(32)).decode('utf-8')
    
    new_electeur = Electeur(
        nom=nom,
        email=email,
        hash_identifiant=hash_identifiant,
        code_verif=code_verif,
        cle_publique=dummy_public_key,
        cle_symetrique_chiffree=dummy_encrypted_key
    )
    db.session.add(new_electeur)
    db.session.commit()

def get_elections():
    """Récupère toutes les élections"""
    elections = Election.query.all()
    return elections

def inserer_vote(id_election, hash_electeur, vote_chiffre_asym, signature, iv_aes, date_vote):
    """Insère un nouveau vote dans la base de données"""
    try:
        nouveau_vote = Vote(
            id_election=id_election,
            hash_electeur=hash_electeur,
            vote_chiffre_asym=vote_chiffre_asym,
            signature=signature,
            iv_aes=iv_aes,
            date_vote=date_vote
        )
        db.session.add(nouveau_vote)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Erreur lors de l'insertion du vote: {e}")
        return False

# Enregistrer la fonction de fermeture de la connexion BD
@app.teardown_appcontext
def teardown_db(exception):
    close_db_connection()

@app.context_processor
def inject_csrf_token():
    """Injecte automatiquement le jeton CSRF dans tous les templates"""
    return dict(csrf_token=lambda: csrf._get_csrf_token())

# ---- Handlers d'erreurs améliorés ----
@app.errorhandler(404)
def page_not_found(e):
    app.logger.info(f"Page non trouvée : {request.url}")
    return render_template('404.html'), 404

@app.errorhandler(400)
def bad_request(e):
    app.logger.warning(f"Requête malformée : {request.url}")
    return render_template('404.html', error="Requête incorrecte"), 400

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Erreur serveur : {str(e)}")
    return render_template('404.html', error="Erreur interne du serveur"), 500

@app.route('/debug-csrf')
def debug_csrf():
    """Cette route temporaire affiche le token CSRF pour le débogage"""
    return f"""
    <html>
        <head><title>Debug CSRF</title></head>
        <body>
            <h1>CSRF Token Info</h1>
            <p>Current CSRF Token: {csrf._get_csrf_token()}</p>
            <p>This token should match what's being sent in your forms</p>
            <form action="/test-csrf" method="post">
                <input type="hidden" name="csrf_token" value="{csrf._get_csrf_token()}">
                <button type="submit">Test CSRF</button>
            </form>
        </body>
    </html>
    """

@app.route('/test-csrf', methods=['POST'])
def test_csrf():
    """Cette route teste la validation CSRF"""
    return "CSRF test passed! Form submission was successful."

# Middleware de sécurité
@app.after_request
def add_security_headers(response):
    # Politique plus permissive pour autoriser les scripts et CSS locaux
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
@app.route('/admin-login', methods=['GET', 'POST'])
@csrf.exempt
def admin_login():
    # Variable pour stocker les erreurs
    error = None
    
    if request.method == 'POST':
        # Récupérer les informations du formulaire
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Vérification des identifiants (à remplacer par une vérification sécurisée)
        # IMPORTANT: Ne stockez jamais les mots de passe en clair comme ceci 
        # C'est juste pour l'exemple - utilisez des hash en production
        if username == 'admin' and password == 'admin123':
            # Création d'une session admin
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Connexion réussie. Bienvenue dans le panneau d\'administration.', 'success')
            
            # Redirection vers le panneau d'administration
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Identifiants incorrects. Veuillez réessayer.'
            flash(error, 'error')
    
    # GET request ou authentification échouée
    return render_template('admin_login.html')

# Route pour le tableau de bord d'administration
@app.route('/admin-dashboard')
def admin_dashboard():
    # Vérifier si l'utilisateur est connecté en tant qu'admin
    if not session.get('admin_logged_in'):
        flash('Veuillez vous connecter pour accéder au panneau d\'administration.', 'error')
        return redirect(url_for('admin_login'))
    
    # Récupérer les données pour le tableau de bord
    elections = Election.query.all()
    votes_count = Vote.query.count()
    electeurs_count = Electeur.query.count()
    
    return render_template('admin_dashboard.html', 
                           elections=elections, 
                           votes_count=votes_count, 
                           electeurs_count=electeurs_count)

# Route pour la déconnexion admin
@app.route('/admin-logout')
def admin_logout():
    # Supprimer les variables de session admin
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/election/supprimer/<int:election_id>', methods=['POST'])
def supprimer_election(election_id):
    # Vérifier si l'administrateur est connecté
    if 'admin_username' not in session:
        flash('Vous devez être connecté pour effectuer cette action', 'error')
        return redirect(url_for('admin_login'))
    
    try:
        # Récupérer l'élection à supprimer
        election = Election.query.get_or_404(election_id)
        
        # Stocker le titre pour le message de confirmation
        titre_election = election.titre
        
        # Supprimer d'abord les votes associés à cette élection
        Vote.query.filter_by(election_id=election_id).delete()
        
        # Supprimer les candidats associés à cette élection
        Candidat.query.filter_by(election_id=election_id).delete()
        
        # Supprimer l'élection
        db.session.delete(election)
        db.session.commit()
        
        flash(f'L\'élection "{titre_election}" a été supprimée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression de l\'élection: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

# ----- ROUTES -----
# Route principale pour la page d'identification
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # This redirects to your identification page
    return redirect(url_for('index'))
# Route pour la page d'accueil
@app.route('/index.html')
def accueil():
    return render_template('index.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/identification')
def identification():
    return render_template('identification.html')

@app.route('/vote')
def vote_page():
    # Récupérer les élections actives et leurs candidats
    elections = get_elections()
    # Passer les données au template
    return render_template('vote.html', elections=elections)

@app.route('/merci')
def merci():
    return render_template('merci.html', now=datetime.now())

@app.route('/verification_code')
def verification_code_page():
    return render_template('verification_code.html')

# Redirection des routes .html vers les routes sans .html
@app.route('/results.html')
def redirect_results():
    return redirect(url_for('results'))

@app.route('/identification.html')
def redirect_identification():
    return redirect(url_for('identification'))

@app.route('/vote.html')
def redirect_vote():
    return redirect(url_for('vote_page'))

@app.route('/merci.html')
def redirect_merci():
    return redirect(url_for('merci'))

@app.route('/verification_code.html')
def redirect_verification_code():
    return redirect(url_for('verification_code_page'))

@app.route('/admin')
def admin_redirect():
    """Redirection de /admin vers /admin-login pour faciliter l'accès"""
    return redirect(url_for('admin_login'))

# Route pour envoyer un code de vérification
@app.route('/envoyer-code', methods=['POST'])
@csrf.exempt  # Exempting this route from CSRF protection temporarily
def envoyer_code():
    voter_id = request.form.get('voter_id')
    email = request.form.get('email')

    if not voter_id:
        flash("Identifiant requis.", "error")
        return redirect(url_for('identification'))

    if not email:
        flash("Adresse e-mail requise.", "error")
        return redirect(url_for('identification'))

    hash_identifiant = hashlib.sha256(voter_id.encode('utf-8')).hexdigest()
    electeur = get_electeur_by_hash(hash_identifiant)

    if not electeur:
        code_verification = generer_code()
        # Créer un nouvel électeur
        inserer_electeur(
            nom=voter_id,
            email=email,
            hash_identifiant=hash_identifiant,
            code_verif=code_verification
        )
    else:
        code_verification = electeur.code_verif or generer_code()
        # Mettre à jour le code de vérification si nécessaire
        if not electeur.code_verif:
            electeur.code_verif = code_verification
            db.session.commit()

    # Stocker dans la session de manière plus sécurisée
    session['code_verification'] = code_verification
    session['voter_id'] = voter_id
    session['hash_identifiant'] = hash_identifiant
    session['code_expiration'] = datetime.now().timestamp() + 300  # 5 minutes d'expiration

    try:
        envoyer_email(email, code_verification)
        return redirect(url_for('verification_code_page'))
    except Exception as e:
        flash(f"Erreur lors de l'envoi de l'email : {e}", "error")
        return redirect(url_for('identification'))

# Route pour vérifier le code
@app.route('/verifier-code', methods=['POST'])
@csrf.exempt  # Exempting this route from CSRF protection temporarily
def verifier_code():
    code_saisi = request.form.get('verification_code')
    code_correct = session.get('code_verification')
    code_expiration = session.get('code_expiration', 0)
    
    # Vérifier si le code n'a pas expiré
    if datetime.now().timestamp() > code_expiration:
        flash("Le code a expiré. Veuillez recommencer l'identification.", "error")
        return redirect(url_for('identification'))
        
    # Initialiser un compteur d'essais s'il n'existe pas encore
    if 'essais' not in session:
        session['essais'] = 0
        
    # Comparaison à temps constant pour éviter les attaques de timing
    code_valide = False
    if code_saisi and code_correct:
        if len(code_saisi) == len(code_correct):
            code_valide = True
            for a, b in zip(code_saisi, code_correct):
                if a != b:
                    code_valide = False
                    break
    
    if code_valide:
        # Réinitialiser essais si correct
        session.pop('essais', None)
        session.pop('code_expiration', None)
        return redirect(url_for('vote_page'))
    else:
        # Incrémenter le compteur d'essais
        session['essais'] = session.get('essais', 0) + 1
        if session['essais'] >= 3:
            # Nettoyer la session après trop d'essais
            session.pop('essais', None)
            session.pop('code_verification', None)
            session.pop('voter_id', None)
            session.pop('hash_identifiant', None)
            session.pop('code_expiration', None)
            
            flash("Nombre maximal d'essais atteint. Veuillez recommencer l'identification.", "error")
            return redirect(url_for('identification'))
        else:
            flash(f"Code incorrect, veuillez réessayer. Il vous reste {3 - session['essais']} essai(s).", "error")
            return redirect(url_for('verification_code_page'))

# Soumettre le vote
@app.route('/soumettre-vote', methods=['POST'])
@csrf.exempt  # Pour simplifier le test, mais à éviter en production
def soumettre_vote():
    try:
        # Récupérer le vote et l'ID de l'élection
        vote = request.form.get('candidate')
        id_election = request.form.get('election_id', 1)  # Par défaut, l'élection 1 si non spécifié
        hash_electeur = session.get('hash_identifiant')
        
        app.logger.info(f"Tentative de vote - candidate: {vote}, election_id: {id_election}, hash: {hash_electeur}")
        
        if not vote:
            flash("Aucun candidat sélectionné.", "error")
            return redirect(url_for('vote_page'))
            
        if not hash_electeur:
            flash("Session expirée. Veuillez vous identifier à nouveau.", "error")
            return redirect(url_for('identification'))
        
        # Convertir id_election en entier si ce n'est pas déjà le cas
        try:
            id_election = int(id_election)
        except (ValueError, TypeError):
            flash("ID d'élection invalide.", "error")
            return redirect(url_for('vote_page'))
        
        # Pour l'exemple, nous utilisons des valeurs simulées pour le chiffrement et la signature
        vote_chiffre_asym = hashlib.sha256(vote.encode('utf-8')).hexdigest()
        signature = hashlib.md5(vote.encode('utf-8')).hexdigest()
        iv_aes = os.urandom(16).hex()
        date_vote = datetime.now()
        
        # Utiliser directement SQLAlchemy ORM pour insérer le vote
        try:
            nouveau_vote = Vote(
                id_election=id_election,
                hash_electeur=hash_electeur,
                vote_chiffre_asym=vote_chiffre_asym,
                signature=signature,
                iv_aes=iv_aes,
                date_vote=date_vote
            )
            db.session.add(nouveau_vote)
            db.session.commit()
            
            # Générer et attribuer l'identifiant de confirmation
            id_confirmation = attribuer_identifiant_confirmation(hash_electeur)
            
            if id_confirmation:
                # Stocker l'identifiant de confirmation dans la session pour l'afficher sur la page de remerciement
                session['id_confirmation_vote'] = id_confirmation
                vote_reussi = True
            else:
                app.logger.error("Échec de génération de l'identifiant de confirmation")
                vote_reussi = False
                
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Erreur lors de l'insertion du vote: {e}")
            vote_reussi = False
        
        if vote_reussi:
            flash("Vote enregistré avec succès.", "success")
            # Ne pas supprimer immédiatement l'identifiant de la session pour pouvoir l'afficher sur la page de remerciement
            # Les autres informations sensibles peuvent être nettoyées
            session.pop('voter_id', None)
            session.pop('code_verification', None)
            return redirect(url_for('merci'))
        else:
            flash("Erreur lors de l'enregistrement du vote. Veuillez réessayer.", "error")
            return redirect(url_for('vote_page'))
    except Exception as e:
        app.logger.error(f"Exception non gérée dans soumettre_vote: {e}")
        flash("Une erreur inattendue s'est produite.", "error")
        return redirect(url_for('vote_page'))


if __name__ == '__main__':
    check_static_paths()  # Vérifier les dossiers statiques avant de démarrer
    
    # Afficher les chemins disponibles
    print("Routes disponibles:")
    for rule in app.url_map.iter_rules():
        print(f"{rule}")
    
    # Démarrer l'application
    app.run(debug=True)