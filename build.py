#!/usr/bin/env python3
# Génère le site Bivouak Endurance (statique). Usage: python3 build.py
import re, os, html, json
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
MAT = os.path.join(HERE, "..", "Material", "Bivouak")
SRC = os.path.expanduser("~/mnt/EnduroHub²/EnduroHub/UserGuide.swift")
IMG = os.path.join(HERE, "img"); os.makedirs(IMG, exist_ok=True)
CONTACT = "bivouakendurance@outlook.com"
BETA_HREF = "mailto:" + CONTACT + "?subject=Je%20veux%20%C3%AAtre%20b%C3%AAta-testeur%20de%20Bivouak%20Endurance&body=Bonjour%2C%0A%0AJe%20voudrais%20faire%20partie%20des%20b%C3%AAta-testeurs%20de%20Bivouak%20Endurance%20%28TestFlight%29.%0A%0AMon%20pr%C3%A9nom%20%3A%0AMon%20mod%C3%A8le%20d%27iPhone%20%3A%0AMon%20sport%20principal%20%3A%0AL%27adresse%20e-mail%20de%20mon%20identifiant%20Apple%20%28pour%20recevoir%20l%27invitation%29%20%3A%0A%0AJ%27ai%20lu%20et%20j%27accepte%20la%20charte%20du%20b%C3%AAta-testeur%20%28https%3A//samous92.github.io/bivouak-endurance/beta.html%29.%20En%20r%C3%A9sum%C3%A9%20%3A%0A-%20version%20de%20test%20fournie%20en%20l%27%C3%A9tat%2C%20avec%20des%20erreurs%20possibles%20%3B%0A-%20b%C3%A9n%C3%A9volat%20%3A%20aucune%20r%C3%A9mun%C3%A9ration%20ni%20droit%20sur%20l%27application%2C%20son%20code%20ou%20ses%20revenus%20%3B%0A-%20mes%20retours%20peuvent%20%C3%AAtre%20utilis%C3%A9s%20librement%20%3B%0A-%20je%20ne%20diffuse%20rien%20avant%20la%20sortie%20officielle%20%3B%0A-%20en%20%C3%A9change%2C%20j%27aurai%20acc%C3%A8s%20gratuitement%20%C3%A0%20la%20version%20d%C3%A9finitive%20%3B%0A-%20mon%20adresse%20ne%20sert%20qu%27%C3%A0%20l%27invitation%20TestFlight.%0A%0AMerci%20%21"

# ---------- images ----------
def save(src, dst, w, q=82, crop=None):
    im = Image.open(os.path.join(MAT, src)).convert("RGB")
    if crop: im = im.crop(crop)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(os.path.join(IMG, dst), quality=q, optimize=True, progressive=True)
save("IMG_8127.JPG", "hero.jpg", 1600, crop=(0,0,1376,612))
save("IMG_8129.JPG", "dusk.jpg", 1400)
save("IMG_8136.JPG", "sunrise.jpg", 1400)
save("IMG_8117.JPG", "phone-night.jpg", 560)
save("IMG_8122.JPG", "phone-day.jpg", 560)
save("IMG_8123.JPG", "phone-dusk.jpg", 560)
from PIL import ImageOps
def band(src,dst):
    im=Image.open(os.path.join(MAT,src)).convert("RGB");w,h=im.size;c=im.crop((0,0,int(w*0.36),h))
    o=Image.new("RGB",(c.width*2,h));o.paste(c,(0,0));o.paste(ImageOps.mirror(c),(c.width,0));o.save(os.path.join(IMG,dst),quality=80,optimize=True)
band("IMG_8127.JPG","band-night.jpg");band("IMG_8129.JPG","band-dusk.jpg");band("IMG_8136.JPG","band-sunrise.jpg")
ic = Image.open(os.path.join(MAT, "IMG_8124.JPG")).convert("RGB")
ic.resize((512, 512), Image.LANCZOS).save(os.path.join(IMG, "icon.png"), optimize=True)
ic.resize((64, 64), Image.LANCZOS).save(os.path.join(IMG, "favicon.png"), optimize=True)
ic.resize((180, 180), Image.LANCZOS).save(os.path.join(IMG, "apple-touch-icon.png"), optimize=True)

# ---------- captures d'écran (Material/Captures -> img/shot-*.jpg) ----------
CAP = os.path.join(HERE, "..", "Material", "Captures")
STATUSBAR = {"shot-%s.jpg" % n for n in ("biblio","budget","camp","creer","equipement","graphiques","nutrition","palmares","piscine","planchart","stats","synthese","tip","tourmalet","tracker","trainer","trainerlist","trajet")}
def shot(src, dst, crop=None, w=640):
    im = Image.open(os.path.join(CAP, src)).convert("RGB")
    if crop:
        W, H = im.size
        im = im.crop((int(crop[0]*W), int(crop[1]*H), int(crop[2]*W), int(crop[3]*H)))
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if dst in STATUSBAR:   # retire la barre d'état iPhone (heure, cloche, wifi, batterie)
        im = im.crop((0, round(66 * w / 640), im.width, im.height))
    im.save(os.path.join(IMG, dst), quality=84, optimize=True, progressive=True)
shot("IMG_8393.jpg", "shot-plan.jpg")
shot("IMG_8394.PNG", "shot-trainer.jpg")
shot("IMG_8397.jpg", "shot-materiel.jpg")
shot("PUB_palmares.png", "shot-palmares.jpg")
shot("IMG_8400.PNG", "shot-graphiques.jpg")
shot("IMG_8402.PNG", "shot-synthese.jpg")
shot("IMG_8404.PNG", "shot-sauvegarde.jpg", crop=(0, 0.05, 1, 0.50))
# nouvelles captures (versions nettoyées : adresse floutée, logo remplacé, photo de profil rognée)
for _n in ("trajet","tip","planchart","equipement","camp","stats","creer","biblio","budget","nutrition","tracker","piscine","tourmalet","trainerlist","forme","canyon","fiche","widgets","intervals","seuils","profil","exportbudget","coachimport","seance","exportplan"):
    shot("PUB_%s.png" % _n, "shot-%s.jpg" % _n)
shot("PUB_erg.png", "shot-erg.jpg", w=1000)
STATUSBAR |= {"shot-bibliotheque.jpg", "shot-videos.jpg", "shot-recordsnat.jpg", "shot-volumes.jpg"}
shot("PUB_bibliotheque.png", "shot-bibliotheque.jpg")
shot("PUB_videos.png", "shot-videos.jpg", crop=(0, 0, 1, 0.5))
shot("PUB_recordsnat.png", "shot-recordsnat.jpg")
shot("PUB_volumes.png", "shot-volumes.jpg")
shot("PUB_widgetcloche.jpg", "shot-widgetcloche.jpg", crop=(0.045, 0.085, 0.49, 0.925), w=420)
STATUSBAR |= {"shot-coachprepa.jpg", "shot-trackernat.jpg"}
shot("PUB_coachprepa.png", "shot-coachprepa.jpg")
shot("PUB_trackernat.png", "shot-trackernat.jpg")
shot("PUB_coachpaysage.png", "shot-coachpaysage.jpg", w=1000)
shot("PUB_coachportrait.png", "shot-coachportrait.jpg")
shot("PUB_carte.png", "shot-carte.jpg", w=760)
shot("PUB_pdfsemaine.png", "shot-pdfsemaine.jpg", w=1100)
shot("PUB_accueil.png", "shot-tableau.jpg")
shot("PUB_bvman.png", "shot-objectif.jpg", crop=(0, 0.112, 1, 0.99))

# ---------- guide ----------
def swift_str(s, i):
    # s[i] == '"' ; renvoie (texte, index après)
    assert s[i] == '"'; i += 1; out = []
    while s[i] != '"':
        if s[i] == "\\":
            n = s[i+1]
            out.append({"n": "\n", "t": " ", '"': '"', "\\": "\\"}.get(n, n)); i += 2
        else: out.append(s[i]); i += 1
    return "".join(out), i + 1
def parse_guide(path):
    s = open(path, encoding="utf-8").read()
    chaps = []
    for m in re.finditer(r'GuideChapter\(id: "([^"]+)", title: "((?:[^"\\]|\\.)*)"', s):
        chaps.append((m.start(), m.group(1), m.group(2).replace('\\"', '"')))
    out = []
    for k, (pos, cid, title) in enumerate(chaps):
        end = chaps[k+1][0] if k+1 < len(chaps) else len(s)
        blk = s[pos:end]
        tg = re.search(r'tagline: "((?:[^"\\]|\\.)*)"', blk)
        tagline = tg.group(1).replace('\\"', '"') if tg else ""
        sec_start = blk.find("sections:")
        secs = []; i = sec_start
        while True:
            m = re.compile(r'\(\s*"').search(blk, i)
            if not m: break
            j = m.end() - 1
            t, j = swift_str(blk, j)
            rest = re.compile(r'\s*,\s*"').match(blk, j)
            if not rest: i = j; continue
            b, j2 = swift_str(blk, rest.end() - 1)
            if re.compile(r'\s*\)').match(blk, j2): secs.append((t, b))
            i = j2
        out.append(dict(id=cid, title=title, tagline=tagline, sections=secs))
    return out
guide = parse_guide(SRC)

# ---------- gabarit ----------
NAV = [("index.html", "Accueil"), ("fonctionnalites.html", "Fonctionnalités"), ("tout-en-un.html", "Tout en un coup d’œil"), ("partager.html", "Partage & coach"), ("astuces.html", "Astuces"), ("connexions.html", "Connexions"), ("mode-emploi.html", "Mode d'emploi"), ("assistance.html", "Assistance")]
def page(fname, title, body, desc="", cls=""):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == fname else ""}>{t}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Bivouak Endurance</title>
<meta name="description" content="{html.escape(desc or 'Bivouak Endurance : l’application iPhone qui rassemble entraînement, forme, matériel et courses pour la course à pied, le trail, le vélo, la natation et le triathlon. Sans compte, sans cloud.')}">
<link rel="icon" type="image/png" href="img/favicon.png"><link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="stylesheet" href="style.css"></head>
<body class="{cls}">
<header class="top"><a class="brand" href="index.html"><img src="img/favicon.png" alt="" width="30" height="30"><span>Bivouak <em>Endurance</em></span></a>
<nav>{nav}</nav></header>
<main>{body}</main>
<footer><div class="wrap foot">
<div><strong>Bivouak Endurance</strong><br><span class="muted">Application iPhone d’entraînement en endurance.</span></div>
<div><a href="tout-en-un.html">Tout ce que Bivouak sait faire</a><a href="partager.html">Partage, exports et coach</a><a href="astuces.html">Les petits plus (astuces)</a><a href="connexions.html">Montres &amp; connexions</a><a href="confidentialite.html">Confidentialité</a><a href="conditions.html">Conditions &amp; mentions légales</a><a href="assistance.html">Assistance</a><a href="beta.html">Devenir bêta-testeur</a><a href="mailto:{CONTACT}">{CONTACT}</a></div>
</div><p class="wrap tiny muted">© 2026 Bivouak Endurance. Merci à <a href="https://intervals.icu" rel="noopener">Intervals.icu</a>, sur lequel s’appuient les connexions. Apple, iPhone, Apple Watch et App Store sont des marques d’Apple Inc. Garmin est une marque de Garmin Ltd. Intervals.icu, Strava, Coros, Polar, Suunto et Wahoo appartiennent à leurs propriétaires ; Bivouak Endurance est indépendante et n’a aucun partenariat avec eux.</p></footer>
</body></html>"""
def write(f, t): open(os.path.join(HERE, f), "w", encoding="utf-8").write(t)
APPSTORE = '<a class="store" href="#" aria-disabled="true" title="Bientôt sur l’App Store"><svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M16.4 12.6c0-2.3 1.9-3.4 2-3.5-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.15-2.8.85-3.5.85s-1.8-.8-3-.8c-1.5 0-3 .9-3.800 2.300-1.600 2.800-.4 7 1.200 9.300.8 1.100 1.700 2.400 2.900 2.300 1.200 0 1.600-.7 3-.7s1.800.7 3 .7 2-1.100 2.800-2.200c.9-1.300 1.200-2.500 1.300-2.600-.1 0-2.500-1-2.500-3.800zM14.100 5.800c.6-.8 1.100-1.900.9-3-.9.04-2.100.6-2.700 1.400-.6.700-1.100 1.800-1 2.900 1 .1 2.100-.5 2.800-1.300z"/></svg><span><small>Bientôt sur l’</small>App Store</span></a>'


# ---------- briques (accueil + fonctionnalités) ----------
BRICKS = json.loads(r'''[{"id": "plan", "ico": "📅", "name": "Plan", "title": "Un plan pour ton objectif", "intro": "Tu donnes ta course, ta date et le temps dont tu disposes. Bivouak construit un plan par phases à partir de règles écrites et prudentes, puis le suit semaine après semaine.", "items": [{"t": "Choisir ta course", "p": "Course à pied, vélo, trail, triathlon du S à l’Ironman, duathlon, swimrun, aquathlon. Tu choisis la discipline, puis le format ; une liste de 84 courses connues pré-remplit la fiche, et « Ma course n’est pas dans la liste » mène à une fiche vide.", "l": ["Le nom de la course est proposé automatiquement", "Les informations du catalogue sont à vérifier auprès de l’organisateur"]}, {"t": "Un plan par phases", "p": "Le plan est calculé à partir de règles écrites et prudentes, sans intelligence artificielle. Il suit tes repères (seuils, FTP, allures) et le temps que tu peux consacrer à l’entraînement.", "l": ["Des phases claires jusqu’au jour de la course", "Des zones adaptées à tes seuils"]}, {"t": "Échéance trop courte ou lointaine", "p": "Si ta date est trop proche, Bivouak te le dit. Si elle est très lointaine, il ajoute une phase de remise en forme avant le plan proprement dit.", "l": []}, {"t": "Un plan qui vit", "p": "Tu déplaces, allèges ou remplaces une séance, tu notes celles que tu as faites, et le plan reste lisible semaine après semaine.", "l": ["Export PDF d’une semaine, d’un mois ou du plan complet", "Export CSV pour Excel, et plan personnalisé importable depuis Excel"]}, {"t": "Records et seuils à jour", "p": "Quand une activité bat l’un de tes records ou montre une FC max plus haute, Bivouak te le propose : tu confirmes ou tu refuses. Chaque semaine, il réestime aussi ta FTP, ta VMA, ta VO2 max, ta CSS et ta FC max, puis te propose de changer la valeur ou de refaire un test. Ces valeurs restent des estimations : rien ne change sans ton accord.", "l": []}, {"t": "Sans montre, sans problème", "p": "Tu peux démarrer sans montre connectée : tu notes ta séance à la main. Garmin et Intervals.icu sont des bonus, pas une condition.", "l": []}]}, {"id": "seances", "ico": "⏱️", "name": "Séances", "title": "Ta séance du jour", "intro": "Le jour venu, tu suis ta séance dans l’app : sur home trainer connecté, ou dehors avec le tracker GPS.", "items": [{"t": "Home trainer Bluetooth", "p": "Mode ERG, cols, test FTP. L’écran affiche puissance, cœur, cadence, vitesse et distance, étape par étape.", "l": ["Testé avec le Decathlon D100", "L’iPhone peut passer en paysage pendant la séance"]}, {"t": "Tracker GPS", "p": "Vélo, course à pied, trail : tu enregistres ta sortie. Si l’app se ferme en route, tu peux reprendre la séance ensuite.", "l": []}, {"t": "Bibliothèque et atelier", "p": "Des séances prêtes à l’emploi, et un atelier pour créer les tiennes. Elles peuvent entrer dans ton plan et dans ton palmarès.", "l": []}, {"t": "Tes sorties importées", "p": "Tu as une montre ? Importe tes sorties via Intervals.icu ou Garmin Connect, et envoie tes séances à l’Apple Watch. Tu n’en as pas ? Tout fonctionne quand même.", "l": ["Connexions facultatives, que tu relies toi-même", "Seuls ces services reçoivent des données"]}]}, {"id": "jour-j", "ico": "🏁", "name": "Jour J", "title": "Ton jour J, rien oublié", "intro": "Une fiche par course rassemble la logistique, pour que le matin de la course ne dépende d’aucune mémoire.", "items": [{"t": "La fiche de course", "p": "Dossard, trajets, hébergement, nutrition de course, checklists, temps visés et guide de l’athlète au même endroit, avec un rappel si tu n’es pas encore inscrit.", "l": ["Fiche et journal de course exportables en PDF"]}, {"t": "Papiers et échéances", "p": "Licence, certificat médical, PPS : Bivouak te prévient avant qu’ils expirent, 30 jours à l’avance pour ceux qui demandent des démarches.", "l": []}, {"t": "Courses d’autres sports", "p": "Tu prépares aussi un duathlon, un swimrun ou un aquathlon ? La fiche s’adapte.", "l": []}]}, {"id": "materiel", "ico": "🎒", "name": "Matériel", "title": "Ton matériel, de la pièce au reçu", "intro": "Tout ce qui entoure l’entraînement, au même endroit, et seulement ce que tu choisis d’afficher.", "items": [{"t": "Vélos, chaussures, pièces", "p": "Chaque équipement a sa fiche : kilométrage, pièces montées, historique d’utilisation. Un rappel d’entretien apparaît selon les kilomètres ou la date.", "l": []}, {"t": "Garanties et documents", "p": "Factures, garanties, certificats : tu les classes avec l’équipement, et l’app te prévient avant l’expiration d’une garantie.", "l": ["La photo du QR Bicycode est enregistrée comme document d’identification"]}, {"t": "Budget", "p": "Ce que coûte ta saison, par objectif et par catégorie, avec export CSV pour Excel.", "l": []}, {"t": "Nutrition", "p": "Tes repères de nutrition et ce que tu prévois pour les courses.", "l": []}]}, {"id": "souvenirs", "ico": "🏆", "name": "Souvenirs", "title": "Ton palmarès et tes souvenirs", "intro": "Ce que tu as fait mérite de rester. Ton palmarès se remplit de tes objectifs et de tes courses déclarées.", "items": [{"t": "Palmarès", "p": "Tes résultats, classés de la course la plus récente à la plus ancienne, avec un filtre par année. Il se rouvre là où tu l’avais laissé.", "l": ["Courses déclarées à la main, même sans plan"]}, {"t": "Photos et vidéos", "p": "Tu rattaches photos et vidéos à tes activités. Les vidéos sont allégées à l’ajout et incluses dans la sauvegarde. La bibliothèque « Photos et vidéos » les regroupe dans un onglet à part, et dans la liste des activités, le filtre « Souvenirs » ne garde que celles qui ont une photo ou une vidéo.", "l": []}, {"t": "Images et diplômes à partager", "p": "Une image souvenir de ton activité, un diplôme personnel, une fiche de course : des documents que tu peux montrer, signés Bivouak Endurance.", "l": ["Le diplôme est établi à partir de tes informations, sans valeur officielle"]}]}, {"id": "quotidien", "ico": "📱", "name": "Au quotidien", "title": "Au quotidien", "intro": "De petites choses pour que l’app se glisse dans ta journée sans t’encombrer.", "items": [{"t": "Quatre widgets", "p": "Compte à rebours, semaine, prochaine séance, souvenirs. Un toucher ouvre la bonne fiche : l’activité, l’objectif ou la séance. Une petite cloche s’affiche sur « Prochaine séance » quand une alerte t’attend.", "l": []}, {"t": "La cloche « À faire bientôt »", "p": "Elle n’apparaît que si quelque chose approche : un entretien, un papier qui expire, une inscription, une sauvegarde. Rouge si c’est urgent, orange sinon. Tu peux repousser un rappel ou ne plus le recevoir.", "l": []}, {"t": "Recherche partout", "p": "Une loupe en haut des écrans principaux cherche dans tes contenus, puis dans l’aide.", "l": []}, {"t": "Thèmes et mascotte", "p": "Trois thèmes au choix. Bivi, la mascotte, t’accompagne si tu le veux, et se désactive d’un réglage.", "l": ["Tout est facultatif : masque ce qui ne te sert pas"]}]}, {"id": "donnees", "ico": "🔒", "name": "Tes données", "title": "Tes données restent chez toi", "intro": "Bivouak fonctionne sans compte et sans serveur Bivouak. Tout est sur ton iPhone.", "items": [{"t": "Sans compte, sans publicité", "p": "Aucun serveur Bivouak, aucune publicité, aucun suivi. Seuls les services que tu relies toi-même (Intervals.icu, Garmin, météo Apple) reçoivent des données.", "l": []}, {"t": "Sauvegarde et restauration", "p": "Une sauvegarde intégrée, avec chiffrement, couvre tes activités, tes tracés, tes vidéos et tes réglages. Elle sert aussi pour changer d’iPhone.", "l": ["Un compteur te dit quand une sauvegarde devient utile", "Quand une sauvegarde n’est pas chiffrée, l’app te le signale"]}, {"t": "Pourquoi c’est important", "p": "Sans compte, il n’y a rien à perdre côté serveur, mais la sauvegarde devient ta responsabilité. L’app te la rappelle au bon moment.", "l": []}]}, {"id": "limites", "ico": "ℹ️", "name": "Limites", "title": "Ce que Bivouak ne fait pas (encore)", "intro": "Mieux vaut le dire avant que tu le découvres.", "items": [{"t": "Pas encore", "p": "Pas de communauté ni de monde virtuel. Pas de lecture d’Apple Santé. L’app est en français uniquement pour l’instant ; l’anglais viendra plus tard.", "l": []}, {"t": "Pas un coach", "p": "Bivouak donne un plan indicatif, construit sur des règles prudentes. Il ne remplace ni un entraîneur, ni un médecin.", "l": []}]}]''')
MORE = {
 'plan': [['shot-planchart.jpg','La charge par semaine et les phases du plan'],['shot-camp.jpg','Camp de base : ta semaine vue par Bivouak'],['shot-stats.jpg','Statistiques : performances, activité, forme'],['shot-forme.jpg','Forme, fatigue, fraîcheur et leur courbe'],['shot-seuils.jpg','Tes seuils : FTP, FC max, VMA, VO2 max, CSS'],['shot-recordsnat.jpg','Tes records, natation comprise'],['shot-volumes.jpg','Tes volumes par semaine, calculés d’après tes activités'],['shot-exportplan.jpg','Exporter ta semaine, ton mois, ton plan complet']],
 'seances': [['shot-tracker.jpg','Le Tracker : séance du jour ou séance libre'],['shot-creer.jpg','Créer une séance, ou partir d’un modèle'],['shot-trainerlist.jpg','Les séances du home trainer en un coup d’œil'],['shot-tourmalet.jpg','Un col mythique, son profil et sa pente'],['shot-seance.jpg','Une séance : la faire, l’envoyer à ta montre, la nutrition conseillée'],['shot-coachimport.jpg','Les séances déposées par ton coach'],['shot-erg.jpg','Mode ERG en paysage',1],['shot-trackernat.jpg','Le Tracker, avec la tuile Natation'],['shot-coachprepa.jpg','Ardoise de piscine : longueur du bassin et séance à nager'],['shot-coachportrait.jpg','L’ardoise en portrait : exercice, distance et chrono en très gros, boutons Suivant et Pause'],['shot-coachpaysage.jpg','Ardoise de piscine en paysage : exercice, distance et chrono, lisibles depuis le bord du bassin',1]],
 'jour-j': [['shot-trajet.jpg','Coût du trajet : essence, péages, partage'],['shot-tip.jpg','Le « Le saviez-vous ? » qui explique chaque écran']],
 'materiel': [['shot-canyon.jpg','La fiche d’un vélo : composants et rappels'],['shot-equipement.jpg','Tes espaces de rangement'],['shot-budget.jpg','Combien te coûte ta passion ?'],['shot-nutrition.jpg','Ton frigo de nutrition']],
 'souvenirs': [['shot-piscine.jpg','Une activité avec sa photo et le message de Bivouak'],['shot-bibliotheque.jpg','La bibliothèque : photos d’activités, de matériel et de nutrition'],['shot-videos.jpg','L’onglet Vidéos de la bibliothèque']],
 'quotidien': [['shot-widgetcloche.jpg','Le widget « Prochaine séance » et sa cloche'],['shot-objectif.jpg','Compte à rebours et rappels au bon moment'],['shot-tableau.jpg','Ton tableau de bord'],['shot-profil.jpg','Le profil : sports, seuils, clubs, connexions']],
 'donnees': [['shot-biblio.jpg','Bibliothèque et coffre protégé']],
}
SHOTS = {'plan':('shot-plan.jpg','Le plan de la semaine, en grille'),'seances':('shot-trainer.jpg','Séance sur home trainer, étape par étape'),'jour-j':('shot-fiche.jpg','La fiche d’un objectif : budget, documents, jour J'),'materiel':('shot-materiel.jpg','La fiche d’un vélo et ses composants'),'souvenirs':('shot-palmares.jpg','Le palmarès'),'quotidien':('shot-widgets.jpg','Deux des quatre widgets de l’écran d’accueil'),'donnees':('shot-sauvegarde.jpg','Le compteur de sauvegarde')}
for _b in BRICKS:
    if _b['id'] in SHOTS: _b['shot'], _b['shotAlt'] = SHOTS[_b['id']]
    _b['more'] = MORE.get(_b['id'], [])
BRICK_META = json.loads(r'''[{"id": "plan", "ico": "📅", "title": "Un plan pour ton objectif", "teaser": "10 km, marathon, trail, triathlon : choisis ta course et ta date.", "wide": false}, {"id": "seances", "ico": "⏱️", "title": "Ta séance du jour", "teaser": "Home trainer, GPS, import de tes sorties.", "wide": false}, {"id": "jour-j", "ico": "🏁", "title": "Ton jour J, rien oublié", "teaser": "Dossard, trajets, hébergement, nutrition, checklists.", "wide": false}, {"id": "materiel", "ico": "🎒", "title": "Ton matériel, de la pièce au reçu", "teaser": "Vélos, chaussures, entretien, garanties, budget, nutrition.", "wide": false}, {"id": "souvenirs", "ico": "🏆", "title": "Ton palmarès et tes souvenirs", "teaser": "Courses, photos, vidéos, images à partager.", "wide": false}, {"id": "quotidien", "ico": "📱", "title": "Au quotidien", "teaser": "Widgets, cloche, recherche, thèmes, mascotte.", "wide": false}, {"id": "donnees", "ico": "🔒", "title": "Tes données restent chez toi", "teaser": "Pas de compte, pas de pub, sauvegarde chiffrée.", "wide": true}, {"id": "limites", "ico": "ℹ️", "title": "Ce que Bivouak ne fait pas (encore)", "teaser": "Communauté, Apple Santé, anglais.", "wide": true}]''')
brick_tiles = "".join(f'<a class="tile brick{" wide" if m.get("wide") else ""}" href="fonctionnalites.html#{m["id"]}"><div class="ico">{m["ico"]}</div><strong>{m["title"]}</strong><span>{m["teaser"]}</span></a>' for m in BRICK_META)

# ---------- accueil ----------
promises = [
 ("📅", "Prépare ton objectif", "Ta course, ta date, et un plan prudent par phases si tu en veux un.", "fonctionnalites.html#plan"),
 ("⏱️", "Fais ta séance", "Sur home trainer ou en GPS, avec ou sans montre.", "fonctionnalites.html#seances"),
 ("🏁", "Réussis ton jour J", "Dossard, trajets, nutrition, checklists : rien d’oublié.", "fonctionnalites.html#jour-j"),
 ("🎒", "Et tout autour", "Matériel, budget, nutrition, documents, palmarès : facultatif, tu masques ce qui ne te sert pas.", "fonctionnalites.html#materiel"),
]
feat_short = [
 ("📅", "Plan d’entraînement", "Un plan construit pour ton objectif, calendrier d’abord, qui s’adapte à ta forme et à tes indisponibilités."),
 ("🧱", "Enchaînements (bricks)", "Vélo + course le même jour ? Bivouak les regroupe et t’explique le pourquoi."),
 ("🚴", "Home trainer", "Pilotage Bluetooth, écran personnalisable, mode paysage, fantôme pour te comparer."),
 ("📍", "Tracker GPS", "Enregistre tes sorties sans montre : parcours, distance, allure."),
 ("🏊", "Ardoise de piscine", "Ton téléphone au bord du bassin t’annonce l’exercice, la distance et le chrono en gros ; tu valides à chaque aller-retour."),
 ("🎒", "Matériel & entretien", "Kilomètres, heures, durée : rappels d’entretien, historique des interventions, piles et charges."),
 ("💶", "Budget & carbone", "Suis le coût de ta saison, importe un CSV, estime l’empreinte de tes déplacements de course."),
 ("📂", "Bibliothèque", "Parcours GPX, photos, documents et véhicules, rangés dans l’ordre qui te plaît."),
 ("🏁", "Objectifs & souvenirs", "Compte à rebours, calendrier de courses, et le souvenir de ta course au détour d’un message du jour."),
 ("⌚", "Apple Watch & Intervals.icu", "Envoie tes séances à la montre, importe tes activités sans doublons."),
]
def promise_cards(items): return "".join(f'<a class="card plink" href="{h}"><div class="ico">{i}</div><h3>{t}</h3><p>{d}</p><span class="more">Découvrir →</span></a>' for i, t, d, h in items)
def cards(items): return "".join(f'<article class="card"><div class="ico">{i}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in items)
HERO_VIDEO = '<figure class="hero-video" id="hv" data-fmt="land">\n<div class="hv-frame"><video id="hvid" poster="img/poster-paysage.jpg" muted loop playsinline autoplay preload="metadata" aria-label="Présentation de Bivouak Endurance en vidéo : de ton objectif à ton jour J"><source src="video/bivouak-paysage.mp4" type="video/mp4"></video>\n<div class="hv-bar"><button type="button" id="hv-sound">🔊 Activer le son</button><button type="button" id="hv-play">⏸ Pause</button><button type="button" id="hv-full">⛶ Plein écran</button></div></div>\n<figcaption>La présentation en une minute : ton objectif, ton plan, tes activités, ton matériel.</figcaption></figure>\n<script>\n(function(){\nvar v=document.getElementById(\'hvid\'),f=document.getElementById(\'hv\');if(!v)return;\nvar cur=\'land\',bs=document.getElementById(\'hv-sound\'),bp=document.getElementById(\'hv-play\'),bf=document.getElementById(\'hv-full\');\nfunction want(){return(window.innerWidth<900||window.innerHeight>window.innerWidth*1.05)?\'port\':\'land\'}\nfunction apply(){var w=want();if(w===cur)return;var t=v.currentTime,was=!v.paused;cur=w;f.setAttribute(\'data-fmt\',w);\nv.poster=w===\'port\'?\'img/poster-portrait.jpg\':\'img/poster-paysage.jpg\';\nv.src=w===\'port\'?\'video/bivouak-portrait.mp4\':\'video/bivouak-paysage.mp4\';\nv.addEventListener(\'loadedmetadata\',function h(){v.removeEventListener(\'loadedmetadata\',h);try{v.currentTime=t}catch(e){}if(was)v.play().catch(function(){})});v.load()}\napply();window.addEventListener(\'resize\',apply);window.addEventListener(\'orientationchange\',apply);\nif(window.matchMedia&&matchMedia(\'(prefers-reduced-motion: reduce)\').matches){v.removeAttribute(\'autoplay\');v.pause();v.loop=false;v.controls=true}\nelse{var p=v.play();if(p&&p.catch)p.catch(function(){})}\nbs.onclick=function(){v.muted=!v.muted;bs.textContent=v.muted?\'🔊 Activer le son\':\'🔇 Couper le son\';if(!v.muted&&v.paused)v.play()};\nbp.onclick=function(){if(v.paused){v.play();bp.textContent=\'⏸ Pause\'}else{v.pause();bp.textContent=\'▶ Lecture\'}};\nbf.onclick=function(){v.muted=false;bs.textContent=\'🔇 Couper le son\';if(v.requestFullscreen)v.requestFullscreen();else if(v.webkitEnterFullscreen)v.webkitEnterFullscreen()};\n})();\n</script>\n'
index = f"""
<section class="hero"><div class="hero-in wrap hero-grid">
<div class="hero-head">
<ul class="sports" aria-label="Natation, vélo, course à pied"><li><svg viewBox="0 0 48 48" width="34" height="34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="33" cy="13" r="3.2"/><path d="M8 24l9-5 7 4 5-6"/><path d="M4 33c3 0 3-2.4 6-2.4s3 2.4 6 2.4 3-2.4 6-2.4 3 2.4 6 2.4 3-2.4 6-2.4 3 2.4 6 2.4"/><path d="M4 41c3 0 3-2.4 6-2.4s3 2.4 6 2.4 3-2.4 6-2.4 3 2.4 6 2.4 3-2.4 6-2.4 3 2.4 6 2.4"/></svg><span>Nager</span></li><li><svg viewBox="0 0 48 48" width="34" height="34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="31" r="7.5"/><circle cx="37" cy="31" r="7.5"/><path d="M11 31l8-14h11l7 14M19 17l7 14h-15M27 11h6"/></svg><span>Pédaler</span></li><li><svg viewBox="0 0 48 48" width="34" height="34" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="29" cy="9" r="3.2"/><path d="M26 15l-7 7 7 5-3 10M26 15l7 7 7 1M19 22l-8 2M26 27l8 5v8"/></svg><span>Courir</span></li></ul>
<p class="eyebrow big">Application iPhone pour les sports d’endurance</p>
<h1>Ton objectif, ta séance, ton jour J.</h1>
</div>
{HERO_VIDEO}<div class="hero-rest">
<p class="lead">Prépare ton objectif d’endurance : un plan, ta séance du jour et ta logistique de course, sans compte ni abonnement. Pour la course à pied, le trail, le vélo, la natation et le triathlon, du premier dossard jusqu’à l’Ironman.</p>
<ul class="chips"><li>Course à pied</li><li>Trail</li><li>Vélo</li><li>Natation</li><li>Triathlon</li></ul>
<div class="cta">{APPSTORE}<a class="ghost" href="fonctionnalites.html">Découvrir</a><a class="ghost beta" href="beta.html">Devenir bêta-testeur</a></div>
<p class="tiny betanote">Bivouak Endurance est en phase de test. Tu veux l’essayer en avant-première ? Lis d’abord la charte du bêta-testeur : tu pourras ensuite demander ton invitation TestFlight.</p>
</div>
</div></section>
<section class="wrap band"><h2>L’esprit du bivouak</h2>
<p class="sub">Le bivouak, c’est l’endroit où l’on pose son sac pour faire le point avant de repartir. Ici, tu poses ta pratique : où tu en es, où tu vas, et de quoi tu as besoin pour y arriver. Utile avec ou sans plan d’entraînement.</p>
<div class="grid4">{promise_cards(promises)}</div></section>
<section class="shots"><div class="wrap"><h2>L’app en images</h2><p class="sub">Quelques écrans, tels qu’ils s’affichent sur iPhone.</p>
<div class="phones">
<figure><div class="phone real"><img src="img/shot-tableau.jpg" alt="Tableau de bord : objectif, semaine et séance du jour" loading="lazy"></div><figcaption>Ton tableau de bord</figcaption></figure>
<figure class="mid"><div class="phone real"><img src="img/shot-plan.jpg" alt="Plan de la semaine en grille" loading="lazy"></div><figcaption>Ton plan, semaine par semaine</figcaption></figure>
<figure><div class="phone real"><img src="img/shot-trainer.jpg" alt="Séance sur home trainer" loading="lazy"></div><figcaption>Ta séance sur home trainer</figcaption></figure>
<figure class="mid"><div class="phone real"><img src="img/shot-synthese.jpg" alt="Bilan d’une séance avec le message de Bivouak" loading="lazy"></div><figcaption>Le bilan après la séance</figcaption></figure>
</div></div></section>
<section class="tr"><div class="wrap"><div><p class="eyebrow">Home trainer</p><h2>Un home trainer qui va à l’essentiel</h2>
<p>Ta séance d’abord : watts, cible, cœur, cadence. L’écran est pensé pour être fonctionnel et efficace, sans décor qui te dérange pendant l’effort.</p>
<p>Et si le petit bonhomme qui pédale te manque vraiment, on le retrouve en mode paysage, avec la route et les collines, dans un clin d’œil rétro années 80. Rien d’indispensable, juste pour le plaisir.</p></div>
<figure class="trfig"><div class="phone real"><img src="img/shot-erg.jpg" alt="Mode ERG en paysage : un petit cycliste pédale sur une route, avec la puissance, le cœur, la cadence et la vitesse" loading="lazy"></div><figcaption>Mode ERG en paysage : la touche rétro années 80.</figcaption></figure></div></section>
<section class="wrap band"><h2>Explore par brique</h2><p class="sub">Chaque brique ouvre ses fonctions, une par une.</p><div class="bricks">{brick_tiles}</div>
<p class="sub" style="margin-top:28px">Compatible Apple Watch et Garmin Connect, et, via Intervals.icu, avec Coros, Polar, Suunto, Wahoo ou Strava. <a href="connexions.html">Voir comment ça marche</a>.</p>
<p class="center"><a class="ghost dark" href="tout-en-un.html">Tout ce que Bivouak sait faire</a> <a class="ghost dark" href="partager.html">Partage, exports et coach</a> <a class="ghost dark" href="astuces.html">Les petits plus</a> <a class="ghost dark" href="fonctionnalites.html">Explorer avec captures</a> <a class="ghost dark" href="mode-emploi.html">Lire le mode d’emploi</a></p></section>
<section class="band-photo" style="--bg:url(img/band-dusk.jpg)"><div class="wrap">
<h2>Sans compte, sans cloud, sans pub</h2>
<p>Pas de compte, pas de serveur Bivouak, pas de publicité, aucun outil de mesure d’audience. Tes séances, tes photos et tes documents sont enregistrés sur ton iPhone. Les connexions facultatives (Intervals.icu, Garmin, météo Apple) ne servent que si tu les actives.</p>
<p><a class="ghost" href="confidentialite.html">Lire la politique de confidentialité</a></p></div></section>
<section class="wrap band thanks"><h2>Merci à Intervals.icu</h2>
<p class="sub">Bivouak s’appuie sur <a href="https://intervals.icu" rel="noopener" target="_blank">Intervals.icu</a> pour importer tes activités et envoyer tes séances vers ta montre. C’est un service indépendant que nous utilisons nous-mêmes, et nous lui sommes très reconnaissants : merci à son créateur et à sa communauté. Bivouak Endurance reste indépendante et n’a aucun partenariat avec lui. <a href="connexions.html">Voir les connexions</a>.</p></section>
<section class="wrap band center"><img class="appicon" src="img/icon.png" alt="Icône Bivouak Endurance" width="120" height="120">
<h2>Pose ton sac.</h2><p class="sub">Bivouak Endurance arrive sur l’App Store.</p><div class="cta c">{APPSTORE}</div></section>
"""
write("index.html", page("index.html", "Application d’entraînement en endurance", index, cls="home"))

# ---------- fonctionnalités ----------
fbody = """<section class="pagehead" style="--bg:url(img/band-sunrise.jpg)"><div class="wrap"><h1>Fonctionnalités</h1><p class="lead">Choisis une brique, puis une fonction. Le détail complet se trouve dans le mode d’emploi.</p></div></section>
<section class="wrap band"><div class="bricktabs" id="bt" role="tablist"></div>
<div class="explorer"><div class="flist" id="fl" role="tablist"></div><article class="fdetail" id="fd" aria-live="polite"></article></div>
<div class="gal" id="gal"></div>
<p class="center"><a class="ghost dark" href="mode-emploi.html">Lire le mode d’emploi</a></p></section>
<script>
const B=__BRICKS__;
const bt=document.getElementById('bt'),fl=document.getElementById('fl'),fd=document.getElementById('fd');
const esc=s=>s.replace(/&/g,'&amp;').replace(/</g,'&lt;');
bt.innerHTML=B.map(b=>`<a href="#${b.id}" data-id="${b.id}"><span>${b.ico}</span>${esc(b.name)}</a>`).join('');
function feature(b,k){const f=b.items[k];fd.innerHTML=`<div class="ftext"><h2>${esc(f.t)}</h2><p>${esc(f.p)}</p>`+(f.l.length?`<ul>${f.l.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:'')+`</div>`+(b.shot?`<figure class="fshot"><div class="phone real"><img src="img/${b.shot}" alt="${esc(b.shotAlt)}" loading="lazy"></div><figcaption>${esc(b.shotAlt)}</figcaption></figure>`:'');
 fl.querySelectorAll('button').forEach((e,i)=>e.setAttribute('aria-selected',i===k));}
function route(){const id=location.hash.slice(1);const b=B.find(x=>x.id===id)||B[0];
 bt.querySelectorAll('a').forEach(a=>a.toggleAttribute('aria-current',a.dataset.id===b.id));
 fl.innerHTML=`<p class="fintro"><strong>${esc(b.title)}</strong><br>${esc(b.intro)}</p>`+b.items.map((f,k)=>`<button role="tab" data-k="${k}">${esc(f.t)}</button>`).join('');
 fl.querySelectorAll('button').forEach(e=>e.addEventListener('click',()=>feature(b,+e.dataset.k)));feature(b,0);
 const gal=document.getElementById('gal');gal.innerHTML=(b.more&&b.more.length)?'<h3>Les écrans de cette brique</h3><div class="galrow">'+b.more.map(m=>`<figure${m[2]?' class="land"':''}><div class="phone real"><img src="img/${m[0]}" alt="${esc(m[1])}" loading="lazy"></div><figcaption>${esc(m[1])}</figcaption></figure>`).join('')+'</div>':'';}
addEventListener('hashchange',route);route();
</script>"""
fbody = fbody.replace("__BRICKS__", json.dumps(BRICKS, ensure_ascii=False))
write("fonctionnalites.html", page("fonctionnalites.html", "Fonctionnalités", fbody))

# ---------- mode d'emploi ----------
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower().replace("é","e").replace("è","e").replace("ê","e").replace("à","a").replace("ô","o").replace("î","i").replace("ç","c")).strip("-")
toc = '<a href="mode-emploi.html" onclick="history.pushState(null,\'\',\'mode-emploi.html\');show();return false">← Tous les chapitres</a>' + "".join(f'<a href="#{c["id"]}">{html.escape(c["title"])}</a>' for c in guide)
tiles = "".join(f'<a class="tile" href="#{c["id"]}"><strong>{html.escape(c["title"])}</strong><span>{html.escape(c["tagline"])}</span></a>' for c in guide)
chs = ""
for c in guide:
    secs = "".join(f'<section id="{c["id"]}-{slug(t)}" class="gs"><h3>{html.escape(t)}</h3><p>{html.escape(b).replace(chr(10), "<br>")}</p></section>' for t, b in c["sections"])
    chs += f'<article class="chap" id="{c["id"]}"><h2>{html.escape(c["title"])}</h2><p class="tag">{html.escape(c["tagline"])}</p>{secs}</article>'
mbody = f"""<section class="pagehead" style="--bg:url(img/band-night.jpg)"><div class="wrap"><h1>Mode d’emploi</h1><p class="lead">Le même guide que dans l’app, consultable ici. Tape un mot pour le retrouver.</p>
<input id="q" type="search" placeholder="Rechercher : budget, selle, sauvegarde…" autocomplete="off"></div></section>
<div class="wrap"><div class="tiles" id="tiles">{tiles}</div></div>
<div class="wrap docs"><aside><nav id="toc">{toc}</nav></aside><div id="content">{chs}<p id="none" hidden>Aucun résultat.</p></div></div>
<script>
const q=document.getElementById('q'),gs=[...document.querySelectorAll('.gs')],chaps=[...document.querySelectorAll('.chap')],none=document.getElementById('none'),tiles=document.getElementById('tiles'),docs=document.querySelector('.docs');
function show(){{const v=q.value.trim().toLowerCase(),id=location.hash.slice(1).split('-')[0];let n=0;
const one=!v&&chaps.some(c=>c.id===id);
tiles.hidden=!!v||one;docs.hidden=!v&&!one;
gs.forEach(g=>{{const ok=!v||g.textContent.toLowerCase().includes(v);g.hidden=!ok;if(ok)n++}});
chaps.forEach(c=>c.hidden=v?![...c.querySelectorAll('.gs')].some(g=>!g.hidden):c.id!==id);
none.hidden=n>0||!v;if(one)scrollTo(0,0)}}
q.addEventListener('input',show);addEventListener('hashchange',show);show();
</script>"""
write("mode-emploi.html", page("mode-emploi.html", "Mode d’emploi", mbody))

# ---------- confidentialité ----------
priv = f"""<section class="pagehead"><div class="wrap"><h1>Politique de confidentialité</h1><p class="lead">En une phrase : tes données restent sur ton iPhone.</p></div></section>
<div class="wrap legal">
<p class="muted">Dernière mise à jour : 26 novembre 2026. <strong>Version provisoire</strong> à relire avant la publication.</p>
<h2>1. Qui sommes-nous</h2><p>Bivouak Endurance est une application iPhone d’entraînement en endurance. Contact : <a href="mailto:{CONTACT}">{CONTACT}</a>. Application créée et éditée par Samuel Forlot, à titre personnel.</p>
<h2>2. Ce qui reste sur ton iPhone</h2><p>Bivouak Endurance n’a pas de compte utilisateur et n’envoie tes données à aucun serveur de l’éditeur : il n’y en a pas. Tout ce que tu saisis ou importes (profil, objectifs, plan, séances, activités et leurs tracés, matériel, budget, nutrition, documents, photos, vidéos, palmarès) est enregistré localement sur ton appareil. Nous n’avons aucun moyen d’y accéder, et nous n’utilisons ni publicité, ni outil de mesure d’audience, ni pistage.</p>
<p>L’achat de l’application passe uniquement par l’App Store : Apple traite le paiement selon sa propre politique, et nous ne recevons aucune donnée personnelle sur toi.</p>
<h2>3. Autorisations demandées</h2>
<ul><li><strong>Localisation (quand l’app est utilisée)</strong> : pour enregistrer le parcours, la distance et l’allure de tes séances, et, si tu actives la météo, pour afficher celle de ton lieu. Pendant une sortie du Tracker, l’app continue d’enregistrer si tu verrouilles l’écran.</li>
<li><strong>Bluetooth</strong> : pour piloter ton home trainer et lire tes capteurs (puissance, cadence, cœur). Le Bluetooth peut rester actif en arrière-plan pendant une séance.</li>
<li><strong>Appareil photo</strong> : pour ta photo de profil, celle d’un équipement ou d’un document, ou le QR Bicycode de ton vélo.</li>
<li><strong>Photothèque</strong> : l’app ne lit que les photos et vidéos que tu choisis toi-même d’associer à une activité ou à un équipement.</li>
<li><strong>Face ID / Touch ID</strong> : pour confirmer la suppression d’un objectif. La biométrie est traitée par iOS ; l’app n’y a pas accès.</li>
<li><strong>Notifications</strong> : rappels d’entretien, de documents qui expirent, de sauvegarde et de séance. Elles sont programmées sur ton appareil, et tu choisis lesquelles tu veux recevoir.</li>
<li><strong>Sons</strong> : l’app peut émettre des bips et des consignes pendant une séance, y compris écran verrouillé.</li>
<li><strong>Apple Watch</strong> : si tu le demandes, l’app envoie une séance planifiée vers l’app Entraînement de ta montre.</li></ul>
<h2>4. Services tiers que tu actives toi-même</h2>
<ul><li><strong>Météo d’Apple (WeatherKit)</strong> : si tu l’actives, ta position approximative est transmise à Apple pour obtenir les prévisions, selon la <a href="https://www.apple.com/legal/privacy/fr-ww/">politique d’Apple</a>.</li>
<li><strong>Cartes Apple (MapKit)</strong> : affichage des cartes et recherches de lieux.</li>
<li><strong>Intervals.icu</strong> : si tu saisis ta clé personnelle, l’app échange directement avec Intervals.icu pour importer tes activités et y envoyer tes séances. La clé est conservée dans le trousseau de ton iPhone.</li>
<li><strong>Garmin Connect</strong> : si tu saisis ta clé personnelle, l’app dialogue directement avec Garmin pour récupérer tes activités. Les règles de Garmin s’appliquent à ce compte. La clé est conservée dans le trousseau de ton iPhone.</li>
<li><strong>Pages web de produits</strong> : lorsque tu colles l’adresse d’un produit pour renseigner une fiche de matériel, l’app télécharge cette page et son image depuis le site concerné.</li>
<li><strong>Liens que tu ouvres</strong> : un site de course, un itinéraire dans Plans ou Google Maps, un lien de la bibliothèque. L’app ouvre alors ton navigateur ou l’autre application, dont les règles s’appliquent.</li></ul>
<p>Ces échanges partent de ton iPhone vers ces services, sans passer par un serveur de l’éditeur.</p>
<h2>5. Intelligence artificielle</h2><p>Le plan d’entraînement est calculé par des règles écrites, sans intelligence artificielle. Si ton iPhone le permet et que tu l’actives, Apple Intelligence peut reformuler certains messages ou lire le guide d’une course : le traitement se fait sur l’appareil et rien n’est envoyé à l’éditeur ni à un serveur.</p>
<h2>6. Widgets et extension de partage</h2><p>Les widgets de l’écran d’accueil et l’extension qui reçoit des liens depuis Safari lisent et écrivent dans un espace partagé avec l’app, situé sur ton iPhone. Rien n’en sort.</p>
<h2>7. Sauvegarde, exports et partage</h2><p>La sauvegarde est un fichier que tu crées et que tu ranges où tu veux (iCloud Drive, Fichiers, AirDrop). Elle contient tes données, y compris les tracés de tes séances et tes vidéos. Tu peux la chiffrer avec un mot de passe, ce que l’app recommande et te signale quand tu ne le fais pas : sans ce mot de passe, nous ne pouvons pas ouvrir une sauvegarde chiffrée à ta place. Une sauvegarde non chiffrée se lit par quiconque a le fichier : range-la en conséquence.</p>
<p>Les documents que tu exportes (PDF, images, fichiers CSV) sont créés sur ton iPhone et ne partent que si tu les envoies toi-même, par le menu de partage d’iOS. Ils peuvent contenir ton nom, ta photo de profil et les informations que tu as saisies ; ils portent la mention « Bivouak Endurance », et pour les PDF l’adresse du site en petit pied de page. L’envoi d’un retour par e-mail ne se fait que si tu appuies sur « Envoyer » dans ton application Mail.</p>
<h2>8. Durée de conservation et suppression</h2><p>Les données restent tant que tu ne les supprimes pas. Un élément supprimé (activité, objectif, plan) reste 30 jours dans la corbeille de l’app avant suppression définitive. Supprimer l’application supprime les données locales ; une sauvegarde que tu as exportée reste chez toi.</p>
<h2>9. Ce site</h2><p>Ce site est une vitrine. Il n’utilise ni cookie, ni outil de mesure d’audience, ni service de pistage. Comme tout site web, son hébergeur, GitHub Pages (GitHub, Inc., États-Unis), peut conserver les journaux techniques habituels (adresse IP, date de visite) pour assurer la sécurité du service.</p>
<h2>10. Enfants</h2><p>L’application ne s’adresse pas spécifiquement aux enfants et ne collecte aucune donnée à leur sujet.</p>
<h2>11. Tes droits</h2><p>Comme nous ne détenons aucune de tes données, il n’y a rien à demander : tu les consultes, exportes et supprimes toi-même dans l’app. Pour toute question : <a href="mailto:{CONTACT}">{CONTACT}</a>. Tu peux aussi saisir la CNIL (cnil.fr).</p>
<h2>12. Modifications</h2><p>Cette politique peut évoluer ; la date de mise à jour figure en haut de page.</p>
<p class="note">⚠️ Ce texte est un projet rédigé à partir du fonctionnement de l’application. Il ne constitue pas un avis juridique et doit être relu et complété (coordonnées, hébergeur) avant publication.</p></div>"""
write("confidentialite.html", page("confidentialite.html", "Confidentialité", priv))

# ---------- conditions ----------
cond = f"""<section class="pagehead"><div class="wrap"><h1>Conditions d’utilisation &amp; mentions légales</h1></div></section>
<div class="wrap legal"><p class="muted">Dernière mise à jour : 26 novembre 2026. <strong>Version provisoire.</strong></p>
<h2>Mentions légales</h2><p>Éditeur et créateur : Samuel Forlot, à titre personnel. [Adresse postale à compléter avant la mise en vente.] Contact : <a href="mailto:{CONTACT}">{CONTACT}</a>. Directeur de la publication : Samuel Forlot. Hébergeur du site : GitHub Pages (GitHub, Inc., États-Unis).</p>
<h2>Utilisation de l’application</h2><p>Bivouak Endurance est fournie telle quelle. Elle est distribuée par l’App Store, et ses conditions d’achat et de licence sont celles du contrat de licence standard d’Apple pour les applications. [Prix et modèle d’achat à compléter avant publication.]</p>
<h2>Pas un avis médical</h2><p>Les plans, conseils et messages produits par l’app viennent d’un moteur de règles écrites, pas d’un professionnel de santé. Bivouak Endurance n’est pas un dispositif médical. Ils ne remplacent ni un entraîneur, ni un médecin. Consulte un médecin avant de reprendre ou d’intensifier une pratique, et écoute ton corps. Un test d’effort chez un médecin du sport ou dans un centre spécialisé reste la meilleure façon de connaître tes vraies limites ; les valeurs que l’app estime pour toi sont volontairement prudentes et ne le remplacent pas. L’éditeur ne peut être tenu responsable d’une blessure ou d’un problème de santé.</p>
<h2>Estimations</h2><p>Les calculs (charge, zones, empreinte carbone, budget, usure du matériel) et les informations du catalogue de courses sont des estimations ou des repères indicatifs : vérifie les détails d’une course auprès de son organisateur. Vérifie l’état de ton matériel, notamment pour la sécurité.</p>
<h2>Ardoise de piscine et sécurité de ton téléphone</h2><p>L’ardoise de piscine est un tableau blanc d’entraînement : il affiche l’étape à nager et tu le valides à la main. Il n’est pas conçu pour être emporté dans l’eau. Il implique de poser ton téléphone au bord du bassin : ne le laisse jamais sans surveillance dans un lieu où aucune personne de confiance ne veille dessus (vestiaire, bord de bassin désert, lieu public), et protège-le des éclaboussures et des chutes. L’éditeur ne peut être tenu responsable de la perte, du vol ou de la détérioration de ton appareil. L’app te demande de confirmer cet avertissement avant la première séance.</p>
<h2>Sauvegarde</h2><p>Tes données sont locales : pense à exporter régulièrement une sauvegarde, de préférence chiffrée. Si tu perds ton iPhone, ta sauvegarde ou son mot de passe, l’éditeur ne peut pas récupérer tes données.</p>
<h2>Droit applicable</h2><p>Les présentes conditions sont régies par le droit français.</p>
<h2>Propriété intellectuelle</h2><p>L’application, son nom, son identité visuelle et ses textes sont protégés. Les marques citées appartiennent à leurs propriétaires et ne signifient aucun partenariat.</p>
<p class="note">⚠️ Texte provisoire, à faire relire avant publication.</p></div>"""
write("conditions.html", page("conditions.html", "Conditions & mentions légales", cond))


# ---------- montres et connexions ----------
conn = f"""<section class="pagehead" style="--bg:url(img/band-sunrise.jpg)"><div class="wrap"><h1>Montres &amp; connexions</h1><p class="lead">Bivouak fonctionne seul. Les connexions sont des coups de pouce facultatifs : voici ce qui marche aujourd’hui, sans surprise.</p></div></section>
<div class="wrap legal conn">
<h2>Le principe</h2>
<p>Bivouak Endurance a été pensé pour durer, sans dépendre de personne. Sans aucune connexion, tu peux déjà planifier, enregistrer tes sorties avec le Tracker GPS ou le home trainer, saisir tes activités à la main et tout suivre. Les connexions ci-dessous servent à t’éviter de la saisie : elles facilitent la vie, elles ne sont jamais indispensables.</p>
<div class="devs">
<article class="card"><div class="ico">⌚</div><h3>Apple Watch</h3><p><strong>Envoi des séances : oui, directement.</strong> Tes séances planifiées partent vers l’app Entraînement de la montre, avec leurs étapes et leurs cibles. Tout reste dans l’écosystème Apple, sans compte ni intermédiaire.</p><p class="small">Récupération des sorties : pas encore de lecture directe d’Apple Santé. En attendant, tu peux importer tes sorties depuis un fichier exporté, ou passer par Strava puis Intervals.icu.</p></article>
<article class="card"><div class="ico">🧭</div><h3>Garmin Connect</h3><p><strong>Récupération de tes activités : oui.</strong> Tu crées une clé personnelle dans ton compte Garmin et Bivouak récupère tes sorties, directement de ton iPhone vers Garmin.</p><p class="small">Cela repose sur les autorisations que Garmin accorde aujourd’hui aux particuliers. Elles peuvent évoluer : l’app s’adaptera, et tu pourras toujours continuer sans.</p></article>
<article class="card"><div class="ico">🔗</div><h3>Coros, Polar, Suunto, Wahoo, Zwift, Strava…</h3><p><strong>Via Intervals.icu.</strong> Ces marques n’ouvrent pas d’accès direct aux petites applications. Intervals.icu, une plateforme d’entraînement, propose gratuitement les passerelles : tu y relies ta marque, puis tu lui donnes ta clé personnelle dans Bivouak. Les séances partent vers ta montre, tes activités reviennent.</p><p class="small">Bivouak ne passe par aucun serveur à lui : l’échange se fait de ton iPhone vers Intervals.icu.</p></article>
</div>
<h2>Ce que ta montre ou ton GPS permet</h2>
<p>Selon ton matériel, tu n’as pas exactement les mêmes fonctions. Ce n’est pas un défaut de l’app : chaque marque décide de ce qu’elle ouvre aux applications extérieures. <strong>Historique avant l’app</strong> : retrouver les sorties faites avant d’installer Bivouak. <strong>Activités</strong> : récupérer tes sorties au fil de l’eau. <strong>Séances</strong> : envoyer tes séances planifiées vers l’appareil.</p>
<h3>Montres</h3><div class="tw"><table class="compat"><thead><tr><th>Matériel</th><th>Historique avant l’app</th><th>Activités</th><th>Séances</th></tr></thead><tbody>
<tr><th scope="row">Garmin<span class="rem">Historique via ta clé Garmin Connect. Séances envoyées via Intervals.icu : environ 7 jours à l&#x27;avance.</span></th><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Apple Watch<span class="rem">Séances envoyées directement vers l&#x27;app Entraînement. Pas encore de lecture directe d&#x27;Apple Santé : import de fichier, ou Strava puis Intervals.icu.</span></th><td class="c-n">❌ non</td><td class="c-n">❌ non</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Coros<span class="rem">Via Intervals.icu, à partir du moment où tu le connectes.</span></th><td class="c-n">❌ non</td><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Suunto<span class="rem">Via Intervals.icu, à partir du moment où tu le connectes.</span></th><td class="c-n">❌ non</td><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Polar<span class="rem">Via Intervals.icu, à partir du moment où tu le connectes.</span></th><td class="c-n">❌ non</td><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Huawei<span class="rem">Via Intervals.icu. Seules les courses planifiées partent vers la montre.</span></th><td class="c-n">❌ non</td><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Amazfit / Zepp<span class="rem">Connexion listée par Intervals.icu, détails non confirmés.</span></th><td class="c-n">❌ non</td><td class="c-q">❓ à confirmer</td><td class="c-q">❓ à confirmer</td></tr>
</tbody></table></div>
<h3>GPS vélo</h3><div class="tw"><table class="compat"><thead><tr><th>Matériel</th><th>Historique avant l’app</th><th>Activités</th><th>Séances</th></tr></thead><tbody>
<tr><th scope="row">Garmin Edge<span class="rem">Comme une montre Garmin : tout passe par Garmin Connect et Intervals.icu.</span></th><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td><td class="c-y">✅ oui</td></tr>
<tr><th scope="row">Wahoo ELEMNT<span class="rem">Activités via Intervals.icu (connexion directe conseillée). Envoi des séances : non confirmé.</span></th><td class="c-n">❌ non</td><td class="c-y">✅ oui</td><td class="c-q">❓ à confirmer</td></tr>
<tr><th scope="row">Hammerhead Karoo<span class="rem">Un guide existe pour Intervals.icu. Détails non confirmés.</span></th><td class="c-n">❌ non</td><td class="c-q">❓ à confirmer</td><td class="c-q">❓ à confirmer</td></tr>
<tr><th scope="row">iGPSPORT, Magene, SIGMA<span class="rem">Connexions listées par Intervals.icu, détails non confirmés.</span></th><td class="c-n">❌ non</td><td class="c-q">❓ à confirmer</td><td class="c-q">❓ à confirmer</td></tr>
</tbody></table></div>
<h3>Plateformes et applications</h3><div class="tw"><table class="compat"><thead><tr><th>Matériel</th><th>Historique avant l’app</th><th>Activités</th><th>Séances</th></tr></thead><tbody>
<tr><th scope="row">Strava<span class="rem">Les sorties arrivent via Intervals.icu. Pas d&#x27;envoi de séances.</span></th><td class="c-n">❌ non</td><td class="c-y">✅ oui</td><td class="c-n">❌ non</td></tr>
<tr><th scope="row">Zwift, MyWhoosh<span class="rem">Séances envoyées via Intervals.icu. Zwift n&#x27;accepte que les séances avec cibles de puissance.</span></th><td class="c-n">❌ non</td><td class="c-q">❓ à confirmer</td><td class="c-y">✅ oui</td></tr>
</tbody></table></div>
<p class="small">✅ oui · ❌ non · ❓ à confirmer : nous n’avons pas de source ou de test suffisant, donc nous préférons ne rien promettre. Sans connexion, Bivouak reste utilisable : tu saisis tes sorties à la main ou tu les enregistres avec le Tracker.</p>
<p class="small">Sources : <a href="https://www.intervals.icu/integrations/" rel="noopener">Intervals.icu, intégrations</a> · <a href="https://docs.intervalcoach.app/articles/9507601-syncing-workouts-to-your-devices-and-apps" rel="noopener">IntervalCoach, synchronisation des séances</a> · <a href="https://forum.intervals.icu/t/best-way-to-sync-data-collected-from-wahoo/113409" rel="noopener">forum Intervals.icu, Wahoo</a> · <a href="https://forum.intervals.icu/t/health-sync-now-supports-intervals-icu/92287" rel="noopener">forum Intervals.icu, Health Sync</a> · <a href="https://www.adaptcycling.com/guides/intervals-icu-karoo-workout-sync" rel="noopener">Adapt Cycling, Karoo</a>. Ces services peuvent changer sans préavis.</p>
<h2>Un grand merci à Intervals.icu</h2>
<p>Intervals.icu est une plateforme indépendante, construite et entretenue avec soin, qui met à disposition de tous ces fonctionnalités. Nous l’utilisons nous-mêmes, et nous lui sommes très reconnaissants : merci à son créateur et à sa communauté. Sans elle, relier autant de marques serait hors de portée d’une petite application sans serveur. Si tu t’en sers, n’hésite pas à la soutenir : <a href="https://intervals.icu" rel="noopener">intervals.icu</a>.</p>
<h2>Comment ça pourrait évoluer</h2>
<ul><li>D’autres connexions directes, quand les marques ouvrent leurs accès (par exemple une lecture directe d’Apple Santé, ou Polar).</li>
<li>Des changements chez Garmin ou chez Intervals.icu : si une règle change, Bivouak s’adapte, et ton travail reste sur ton iPhone.</li></ul>
<p class="note">Bivouak Endurance est indépendante : elle n’a aucun partenariat avec Garmin, Apple, Intervals.icu ni les autres marques citées. Ces fonctions dépendent des services de ces tiers, qui peuvent changer sans préavis.</p>
</div>"""
write("connexions.html", page("connexions.html", "Montres & connexions", conn, desc="Apple Watch, Garmin Connect et Intervals.icu : ce qui fonctionne aujourd’hui avec Bivouak Endurance, et comment ça peut évoluer."))

# ---------- pages complémentaires (contenu dans contenu_pages.py) ----------
exec(compile(open(os.path.join(HERE, 'contenu_pages.py'), encoding='utf-8').read(), 'contenu_pages.py', 'exec'))


# ---------- bêta-test : charte du bêta-testeur ----------
_BETA = """<section class="pagehead" style="--bg:url(img/band-dusk.jpg)"><div class="wrap"><h1>Charte du bêta-testeur</h1>
<p class="lead">Merci de vouloir essayer Bivouak Endurance avant tout le monde. Voici, simplement, ce que ça signifie.</p></div></section>
<div class="wrap legal">
<h2>Ce que c’est</h2><p>Une version de test, fournie en l’état. Elle peut contenir des erreurs, changer d’un jour à l’autre, et la bêta peut s’arrêter à tout moment.</p>
<h2>Ce que tu y gagnes</h2><p>En échange de ta collaboration, tu auras accès gratuitement à la version définitive quand elle sera disponible sur l’App Store. Les modalités pour l’obtenir te seront communiquées à ce moment-là.</p>
<h2>Ce que ça ne donne pas</h2><p>Être bêta-testeur est bénévole. Cela ne donne droit à aucune rémunération ni indemnité, et aucun droit sur l’application, son nom, son logo, son code, ses contenus ou ses revenus. Tes remarques et idées peuvent être utilisées librement, sans contrepartie ni mention. Cela ne crée aucun lien de travail, d’association ou de société.</p>
<h2>Ce qu’on te demande</h2><p>Utiliser l’app pour de vrai, et dire franchement ce qui te plaît, ce qui t’a gêné, ce qui manque. Quelques minutes suffisent. Merci de ne pas diffuser de captures, vidéos ou informations sur l’application avant sa sortie officielle, sans accord préalable.</p>
<h2>Donner ton avis</h2><p>Dans la version de test, un bouton « Donner mon avis sur la bêta » (dans À propos) ouvre un e-mail déjà préparé. Ce bouton existe seulement pour faciliter les retours pendant la bêta : il sera retiré de la version définitive, donc ne t’y arrête pas s’il te paraît mal placé ou peu soigné. Pour un bug ou un écran mal affiché, tu peux aussi utiliser l’app TestFlight, qui permet d’envoyer un retour avec capture d’écran.</p>
<h2>Tes données</h2><p>Bivouak enregistre tout sur ton iPhone. Une version de test peut avoir des défauts : une mise à jour ou un bug peut, dans de rares cas, abîmer ou effacer des données. Fais une sauvegarde avant chaque mise à jour, et garde-la hors de ton téléphone (iCloud Drive, ordinateur, NAS). L’éditeur ne peut pas récupérer des données perdues. Ton adresse e-mail ne sert qu’à t’envoyer l’invitation TestFlight et à échanger avec toi pendant la bêta. Elle n’est pas transmise à des tiers.</p>
<h2>Santé</h2><p>Bivouak est un outil d’organisation, pas un avis médical. Les plans et conseils sont indicatifs : tu restes responsable de tes choix et de ta santé.</p>
<h2>Arrêter</h2><p>Tu peux arrêter quand tu veux en le disant par e-mail. Nous pouvons aussi mettre fin à la bêta ou à ton accès.</p>
<h2>Acceptation</h2><p>En envoyant ta demande « Je veux être bêta-testeur », tu déclares avoir lu et accepté cette charte.</p>
<p class="center" style="margin-top:28px"><a class="ghost dark" href="{BETA_HREF}">Devenir bêta-testeur</a></p>
</div>"""
write("beta.html", page("beta.html", "Charte du bêta-testeur", _BETA.replace("{BETA_HREF}", BETA_HREF), desc="Charte du bêta-testeur de Bivouak Endurance : ce que c'est, ce que tu y gagnes et ce que ça ne donne pas."))

# ---------- assistance ----------
faq = [
 ("Comment sauvegarder mes données ?", "Dans le menu de ton profil, ouvre « Sauvegarde » : tu y crées un fichier à ranger dans Fichiers ou iCloud Drive, de préférence chiffré avec un mot de passe. Il contient aussi tes tracés et tes vidéos. Un compteur t’indique quand il devient utile d’en refaire une."),
 ("J’ai changé d’iPhone, comment tout retrouver ?", "Installe Bivouak, puis restaure ton fichier de sauvegarde depuis le même écran « Sauvegarde »."),
 ("Mes séances apparaissent en double", "Si deux activités ont lieu en même temps (le tracker du téléphone et ta montre, par exemple), la fiche de la sortie te propose de garder l’une ou l’autre : rien n’est choisi à ta place, et l’activité écartée reste 30 jours dans la corbeille. Si tu vois un autre doublon, écris-nous avec la date et la source."),
 ("Les notifications d’entretien n’arrivent pas", "Vérifie que les notifications sont autorisées pour Bivouak dans les Réglages d’iOS, puis ouvre une fiche de matériel : les rappels sont recalculés à ce moment-là."),
 ("Mon home trainer ne se connecte pas", "Active le Bluetooth, ferme les autres apps connectées au trainer (Zwift, etc.), réveille-le en pédalant, puis réessaie."),
 ("Où est mon mode d’emploi ?", "Dans l’app avec la loupe de recherche (elle cherche aussi dans l’aide), ou ici : <a href=\"mode-emploi.html\">mode d’emploi</a>."),
]
fq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq)
sup = f"""<section class="pagehead" style="--bg:url(img/band-dusk.jpg)"><div class="wrap"><h1>Assistance</h1><p class="lead">Une question, un bug, une idée ? On lit tout.</p></div></section>
<div class="wrap legal"><h2>Nous écrire</h2><p><a class="mail" href="mailto:{CONTACT}?subject=Bivouak%20Endurance">{CONTACT}</a></p>
<p>Pour qu’on t’aide vite : modèle d’iPhone, version d’iOS, version de Bivouak (écran « À propos ») et ce que tu faisais quand le problème est arrivé.</p>
<h2>Questions fréquentes</h2><div class="faq">{fq}</div></div>"""
write("assistance.html", page("assistance.html", "Assistance", sup))

# ---------- CSS ----------
css = r""":root{--navy:#0d1626;--navy2:#16233a;--ink:#e9edf4;--muted:#9aa7bb;--accent:#c8743a;--accent2:#e39a60;--cream:#f6f1e8;--paper:#fbf8f2;--text:#1c2433}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:17px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:var(--text);background:var(--paper)}
h1,h2,h3{font-family:"Iowan Old Style","Palatino Linotype",Georgia,serif;line-height:1.15;margin:0 0 .5em;font-weight:600}
a{color:var(--accent)}img{max-width:100%;display:block}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
.top{position:sticky;top:0;z-index:20;display:flex;gap:16px;align-items:center;justify-content:space-between;flex-wrap:wrap;padding:10px 20px;background:rgba(13,22,38,.92);backdrop-filter:blur(10px);color:#fff}
.brand{display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;font-weight:600}.brand img{border-radius:7px}.brand em{font-style:normal;color:var(--accent2)}
.top nav{display:flex;gap:18px;flex-wrap:wrap}.top nav a{color:#cdd6e4;text-decoration:none;font-size:15px}.top nav a:hover,.top nav a[aria-current]{color:#fff}
.pagehead,.band-photo{background:linear-gradient(rgba(13,22,38,.35),rgba(13,22,38,.85)),var(--bg,none) center/cover,var(--navy);color:#fff}
.hero-img{height:58vh;min-height:340px;background:var(--bg) center/cover,var(--navy)}
.cta .beta{border-color:var(--accent2);color:#fff}.betanote{max-width:34em;color:#aebbd0;margin-top:12px}
.sports{list-style:none;display:flex;gap:30px;margin:0 0 14px;padding:0;color:#7fd6d0}.sports li{display:flex;align-items:center;gap:9px}.sports span{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:#aebbd0}.eyebrow.big{font-size:clamp(17px,2.4vw,22px);font-weight:600;letter-spacing:.02em;text-transform:none;color:#fff}@media(max-width:520px){.sports{gap:16px}.sports span{display:none}}
.hero{color:#fff;background:var(--navy);padding:44px 0 64px}
.hero h1{font-size:clamp(36px,6vw,62px)}.lead{font-size:clamp(18px,2.2vw,22px);max-width:40em;color:#dbe3ef}
.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:13px;color:var(--accent2)}
.pagehead{padding:70px 0 50px}.pagehead h1{font-size:clamp(32px,5vw,50px)}
.pagehead input{margin-top:14px;width:100%;max-width:520px;padding:13px 16px;border-radius:12px;border:0;font:inherit}
.cta{display:flex;gap:14px;flex-wrap:wrap;align-items:center;margin-top:26px}.cta.c{justify-content:center}
.store{display:inline-flex;align-items:center;gap:10px;background:#000;color:#fff;text-decoration:none;padding:9px 20px;border-radius:12px;border:1px solid #444;font-weight:600;font-size:19px;line-height:1.1}
.store small{display:block;font-size:11px;font-weight:400;opacity:.8}.store[aria-disabled]{cursor:not-allowed}
.ghost{display:inline-block;padding:12px 22px;border-radius:12px;border:1.5px solid currentColor;color:#fff;text-decoration:none;font-weight:600}.ghost.dark{color:var(--navy);margin:4px}
.band{padding:70px 20px}.band h2{font-size:clamp(28px,4vw,40px);text-align:center}.sub{text-align:center;max-width:40em;margin:0 auto 36px;color:#566}
.center{text-align:center}
.grid4,.grid3{display:grid;gap:18px}.grid4{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.grid3{grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.card{background:#fff;border-radius:18px;padding:24px;box-shadow:0 1px 3px rgba(20,30,50,.08),0 8px 24px rgba(20,30,50,.05)}
a.plink{display:block;color:inherit;text-decoration:none}a.plink .more{display:inline-block;margin-top:12px;font-size:14px;font-weight:600;color:var(--accent2)}a.plink:hover .more{text-decoration:underline}.card h3{font-size:21px}.card p{margin:0;color:#4a5568;font-size:16px}.ico{font-size:30px;margin-bottom:8px}
.shots{background:var(--navy);color:#fff;padding:70px 0}.shots h2{text-align:center;font-size:clamp(28px,4vw,40px)}.shots .sub{color:var(--muted)}
.phones{display:flex;justify-content:center;gap:28px;flex-wrap:wrap;align-items:flex-start}
.phones figure{margin:0;text-align:center;width:min(250px,70vw)}.phones .mid{margin-top:26px}
.phone{border:9px solid #05080f;border-radius:38px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.5);background:#000}.phone img{width:100%;aspect-ratio:2/3;object-fit:cover}
figcaption{margin-top:12px;color:var(--muted);font-size:14px}
.band-photo{padding:90px 0;background:linear-gradient(rgba(13,22,38,.55),rgba(13,22,38,.8)),var(--bg) center/cover}.band-photo h2{font-size:clamp(28px,4vw,42px)}.band-photo p{max-width:40em}
.appicon{margin:0 auto 14px;border-radius:27px;box-shadow:0 10px 30px rgba(0,0,0,.3)}
.featgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px}
.feat{background:#fff;border-radius:18px;padding:26px;box-shadow:0 1px 3px rgba(20,30,50,.08)}.feat h3{font-size:22px;margin-bottom:4px}.tag{color:var(--accent);margin:0 0 10px;font-style:italic}.feat ul{padding-left:18px;font-size:15px;color:#4a5568}.feat li{margin-bottom:6px}.feat a{font-weight:600;text-decoration:none}
.docs{display:grid;grid-template-columns:240px 1fr;gap:40px;padding-top:30px;padding-bottom:60px}
#toc{position:sticky;top:76px;display:flex;flex-direction:column;gap:2px;max-height:calc(100vh - 100px);overflow:auto}#toc a{padding:7px 12px;border-radius:8px;text-decoration:none;color:var(--text);font-size:15px}#toc a:hover{background:#ece6d9}
.chap{margin-bottom:56px;scroll-margin-top:80px}.chap h2{font-size:32px;border-bottom:2px solid var(--accent);padding-bottom:6px}.gs h3{font-size:19px;margin:22px 0 4px;font-family:inherit}.gs p{margin:0;color:#3b4557}
.chips{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:20px 0 0}.chips li{border:1px solid var(--accent2);color:var(--accent2);border-radius:99px;padding:4px 14px;font-size:15px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;padding:36px 0 60px}.tile{background:#fff;border-radius:16px;padding:18px 20px;text-decoration:none;color:var(--text);box-shadow:0 1px 3px rgba(20,30,50,.08);display:flex;flex-direction:column;gap:6px;transition:transform .2s}.tile:hover{transform:translateY(-3px)}.tile strong{font-family:"Iowan Old Style",Georgia,serif;font-size:20px}.tile span{color:#566;font-size:15px}[hidden]{display:none!important}
.devs{display:grid;gap:18px;margin:26px 0}.devs .card p{margin:0 0 .6em}.small{font-size:14px!important;color:#6a7385!important}.conn{max-width:860px}
.legal{max-width:760px;padding-top:40px;padding-bottom:70px}.legal h2{font-size:25px;margin-top:1.8em}.muted{color:var(--muted)}.tiny{font-size:13px}.note{background:#fff3e3;border-left:4px solid var(--accent);padding:12px 16px;border-radius:8px}
.mail{font-size:22px;font-weight:600}.faq details{background:#fff;border-radius:12px;padding:14px 18px;margin-bottom:10px;box-shadow:0 1px 2px rgba(0,0,0,.06)}.faq summary{cursor:pointer;font-weight:600}.faq p{margin:.6em 0 0}
footer{background:var(--navy);color:var(--ink);padding:40px 0 20px}footer a{color:#cdd6e4;display:block;text-decoration:none;margin-bottom:6px}footer a:hover{color:#fff}.foot{display:flex;justify-content:space-between;gap:30px;flex-wrap:wrap}
@media(max-width:800px){.docs{grid-template-columns:1fr}#toc{position:static;flex-direction:row;flex-wrap:wrap;max-height:none;border-bottom:1px solid #ddd;padding-bottom:12px}.hero-img{height:50vh}}
@media(prefers-reduced-motion:no-preference){.card,.feat{transition:transform .2s}.card:hover,.feat:hover{transform:translateY(-3px)}}
/* Briques et explorateur de fonctionnalités (2026-11-26) */
.bricks{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.brick{min-height:150px}.brick .ico{font-size:28px;margin-bottom:0}.brick.wide{background:var(--navy);color:var(--ink)}.brick.wide strong{color:#fff}.brick.wide span{color:var(--muted)}
.bricktabs{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:28px}.bricktabs a{display:inline-flex;gap:8px;align-items:center;padding:9px 16px;border-radius:99px;border:1px solid #d9d1c1;background:#fff;text-decoration:none;color:var(--text);font-size:15px}.bricktabs a[aria-current]{background:var(--navy);color:#fff;border-color:var(--navy)}
.explorer{display:grid;grid-template-columns:minmax(0,330px) minmax(0,1fr);gap:22px;align-items:start;margin-bottom:34px}
.flist{display:flex;flex-direction:column;gap:8px}.flist .fintro{margin:0 0 8px;color:#566;font-size:15px}.flist button{font:inherit;text-align:left;cursor:pointer;background:#fff;border:1px solid #e4dccb;border-radius:12px;padding:12px 16px;color:var(--text)}.flist button[aria-selected=true]{background:var(--navy);color:#fff;border-color:var(--navy)}
.fdetail{background:#fff;border-radius:18px;padding:28px;box-shadow:0 1px 3px rgba(20,30,50,.08),0 8px 24px rgba(20,30,50,.05);min-height:220px}.fdetail h2{text-align:left;font-size:28px}.fdetail p{margin:0 0 12px;color:#3b4557}.fdetail ul{padding-left:18px;color:#4a5568}.fdetail li{margin-bottom:6px}
.phone.real img{aspect-ratio:auto;object-fit:initial}.phones figure{width:min(230px,70vw)}
.fdetail{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,210px);gap:26px;align-items:start}.fshot{margin:0;text-align:center}.fshot .phone{border-width:7px;border-radius:30px}.fshot figcaption{font-size:13px;color:#667}
.gal{margin-top:34px}.gal h3{font-size:18px;margin:0 0 12px}.galrow{display:flex;gap:18px;overflow-x:auto;padding:6px 4px 18px;scroll-snap-type:x proximity}.galrow figure{flex:0 0 200px;margin:0;text-align:center;scroll-snap-align:start}.galrow figure.land{flex-basis:420px}.galrow .phone{border-width:7px;border-radius:28px}.galrow figcaption{font-size:13px;color:#667;margin-top:8px}
.tiny a{display:inline;color:inherit;text-decoration:underline;margin:0}
.tr{background:var(--navy);color:#fff;padding:70px 0}.tr .wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.35fr);gap:38px;align-items:center}.tr h2{margin-top:0}.tr p{color:#cdd6e4}.trfig{margin:0;text-align:center}.trfig .phone{border-width:8px;border-radius:26px}.trfig figcaption{font-size:13px;color:#9fb0c8;margin-top:10px}
.xrow{display:grid;grid-template-columns:minmax(0,1fr);gap:26px;margin-top:20px}.xrow.withfig{grid-template-columns:minmax(0,1fr) 230px;align-items:start}.xrow.tips{grid-template-columns:minmax(0,1fr) 450px}
.xcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}.xcards .card{padding:20px}.xcards h3{margin:0 0 6px;font-size:18px}.xcards p{margin:0}
.xcards .fmt{margin-top:10px;font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;color:var(--accent2)}
.xwide{margin-top:24px;text-align:center}.paper{border-radius:12px;overflow:hidden;box-shadow:0 10px 36px rgba(20,30,50,.22);background:#fff}.paper img{display:block;width:100%;height:auto}.xwide .xfig{max-width:760px;margin:0 auto}.xfigs .xfig.paper{width:100%}
.xfigs{display:flex;flex-direction:column;gap:20px}.xfig{margin:0;text-align:center}.xfig .phone{border-width:7px;border-radius:30px}.xfig figcaption{font-size:13px;color:#667;margin-top:8px}
.cat-chips{display:flex;flex-wrap:wrap;gap:8px}.cat-chips a{background:#fff;border-radius:99px;padding:6px 14px;font-size:14px;text-decoration:none;color:var(--text);box-shadow:0 1px 3px rgba(20,30,50,.1)}.cat-chips a:hover{background:var(--navy);color:#fff}
.cat-sec{background:#fff;border-radius:18px;padding:22px 26px;margin:0 0 18px;box-shadow:0 1px 3px rgba(20,30,50,.08),0 8px 24px rgba(20,30,50,.05)}.cat-sec h2{margin:0 0 12px;font-size:23px}
ul.ticks{list-style:none;padding:0;margin:0;columns:2 340px;column-gap:34px}ul.ticks li{break-inside:avoid;padding:7px 0 7px 28px;position:relative;border-bottom:1px solid #e8ebf1}ul.ticks li:before{content:"✓";position:absolute;left:2px;color:var(--accent2);font-weight:700}
[hidden]{display:none!important}
@media(max-width:860px){.xrow.withfig,.xrow.tips{grid-template-columns:minmax(0,1fr)}.xfigs{flex-direction:row;overflow-x:auto}.xfig{flex:0 0 200px}.xrow.tips .xfigs{overflow:visible}.xrow.tips .xfig{flex:1 1 0;min-width:0}}
.thanks{text-align:center}.thanks .sub{max-width:720px;margin-left:auto;margin-right:auto}
@media(max-width:800px){.tr .wrap{grid-template-columns:1fr}}
@media(max-width:860px){.fdetail{grid-template-columns:minmax(0,1fr)}.fshot{max-width:230px;margin:0 auto}}
@media(max-width:860px){.bricks{grid-template-columns:repeat(2,minmax(0,1fr))}.explorer{grid-template-columns:minmax(0,1fr)}}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}.mail{overflow-wrap:anywhere}@media(max-width:520px){.top nav{gap:6px 14px}.top nav a{font-size:14px}.mail{font-size:clamp(16px,5.4vw,22px)}}
"""
write("style.css", css)
print("ok", len(guide), "chapitres;", sum(len(c["sections"]) for c in guide), "sections")
