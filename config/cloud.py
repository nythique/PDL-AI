data = """# Guide d'installation, de configuration et de personnalisation des PC Région Pays de la Loire

## Préambule

Avant de commencer toute manipulation, il est impératif de lire et d’accepter les conditions d’utilisation mentionnées dans les tutoriels. Il est recommandé d’utiliser une souris pour plus de confort. Pensez à brancher votre PC tout au long des opérations pour éviter toute interruption due à une panne de batterie.

---

## Installation de Windows

Pour installer Windows, commencez par télécharger l’ISO de Windows via le lien officiel (https://pcpdl.live/liens-utiles/). Formatez votre clé USB en NTFS, puis ouvrez l’ISO et copiez tous les fichiers sur la clé USB. Ajoutez également le fichier wifi si vous n’avez pas de câble ethernet.

Branchez la clé USB sur le PC, redémarrez en maintenant la touche Shift, puis accédez au menu de dépannage (Options avancées > Voir plus d’options de récupération > Récupération de l’image système). Si le PC demande la clé BitLocker, cliquez sur Ignorer. Si un mot de passe administrateur est demandé, consultez le lien Discord du tutoriel.

Pour lancer l’installation, fermez la fenêtre d’installation qui s’ouvre, cliquez sur Suivant, puis Avancé, Installer un pilote, OK. Dans l’explorateur, accédez à la clé USB, faites clic droit sur setup et choisissez Ouvrir. Si le fichier setup n’apparaît pas, tapez `*.*` dans la barre Nom du fichier.

Après avoir lancé le setup, vérifiez la langue, cliquez sur Installer maintenant, sélectionnez la version de Windows souhaitée, puis cliquez sur Je n’ai pas de clé de produit (version Professionnelle recommandée). Supprimez toutes les partitions sauf la partition de récupération et la clé USB, puis cliquez sur Nouveau, OK, Suivant. N’éteignez plus le PC à partir de cette étape.

L’installation démarre et le PC redémarre. À la fin, utilisez la touche Shift pour naviguer dans les options.

---

## Comptes et droits administrateur

Sur l’écran de connexion Internet, ouvrez une invite de commande (Shift + F10). Pour activer le compte administrateur, tapez `net user administrateur /active:yes`. Pour créer un nouvel utilisateur, tapez `net user /add username password` (remplacez username et password par vos choix, sans espace). Pour afficher un nom complet, ajoutez `/fullname:"Prénom Nom"`. Ajoutez l’utilisateur au groupe administrateurs avec `net localgroup administrateurs username /add`. Si Windows est en anglais, utilisez administrator et administrators.

Pour installer le pilote Wi-Fi, ouvrez l’explorateur avec `explorer.exe`, allez sur la clé USB, ouvrez sp150721.exe et attendez. Pour finaliser la configuration, tapez `cd oobe` puis `msoobe.exe`. Attendez 30 secondes même si le message "Veuillez patienter..." reste affiché, puis forcez l’arrêt du PC en maintenant le bouton d’alimentation. Redémarrez et connectez-vous avec le compte créé.

Après installation, connectez-vous à un réseau Wi-Fi et effectuez les mises à jour Windows. Pour désactiver le compte administrateur, ouvrez une invite de commande en tant qu’administrateur et tapez `net user administrateur /active:no`.

---

## Déblocage et récupération

Si vous avez accès à votre clé BitLocker, rendez-vous directement à l’étape 4 du tutoriel. Sinon, vérifiez que BitLocker est désactivé avec `manage-bde -status`. Si besoin, désactivez-le avec `manage-bde -off C:`.

Pour créer un compte administrateur temporaire, tapez `net user 123 abc /add` puis `net localgroup administrateurs 123 /add`. Redémarrez en mode avancé avec `Shutdown /r /o /t 0`. Après redémarrage, accédez à l’invite de commandes via Dépannage > Options avancées > Invite de commandes. Utilisez le compte 123/abc si demandé.

Pour obtenir une fenêtre administrateur à tout moment, remplacez utilman.exe et narrator.exe par cmd.exe. Sur Windows 11, faites aussi la manipulation pour narrator.exe. Pour supprimer le compte temporaire, tapez `net user 123 /del`.

Pour créer un compte administrateur définitif, tapez `net user PDLadm PDLadm /add` puis `net localgroup administrateurs PDLadm /add`. Pour vérifier les droits, ouvrez une invite de commande en tant qu’administrateur et connectez-vous avec `.\\PDLadm / PDLadm.` Pour que le mot de passe n’expire jamais, ouvrez 'Gestion de l’ordinateur', allez dans "Utilisateurs locaux et groupes", double-cliquez sur PDLadm et cochez "le mot de passe n’expire jamais".

---

## Restauration du système de la région

En cas de problème, il est possible de revenir sur le système de la région. Si le PC n’est pas modifié, suivez le tutoriel du canal Discord dédié, choisissez votre réseau, puis connectez-vous avec votre adresse email académique et votre mot de passe. Si le PC est modifié, lancez `sysprep` (Win + R), choisissez "Entrer en mode OOBE" et "Redémarrer", puis suivez les instructions à l’écran. Si sysprep ne fonctionne pas, suivez la procédure pour PC non modifié.

---

## Activation d’Office sans email scolaire

Installez Office 2021. Ouvrez PowerShell en administrateur (Win + R, tapez PowerShell, puis Ctrl + Shift + Entrée). Exécutez la commande `irm https://get.activated.win | iex`. Dans la fenêtre qui s’ouvre, entrez d’abord le numéro 2, puis le numéro 1. Patientez jusqu’à la fin du chargement, puis fermez la page. Office est maintenant activé. Lien d’installation Office Professionnel Plus 2021 : https://tinyurl.com/OfficePaysDeLaLoire

---

## Installation de logiciels et applications

Pour installer une application du Microsoft Store, rendez-vous sur https://apps.microsoft.com/home?hl=fr-fr&gl=FR, recherchez l’application, cliquez sur "Télécharger" si disponible, puis ouvrez et installez le fichier. Si le bouton n’est pas disponible, copiez le lien de la page, allez sur https://store.rg-adguard.net/, collez le lien, cliquez sur ✅, puis téléchargez le fichier .appx, .appxbundle ou .msixbundle correspondant. Autorisez le téléchargement si une alerte de sécurité apparaît.

Pour certains logiciels, téléchargez le fichier d’installation, puis la pièce jointe du salon Discord <#1350199494792183879>. Glissez le fichier d’installation sur cette pièce jointe pour lancer l’installation. Si cela ne fonctionne pas, créez un dossier dans vos téléchargements, déplacez-y le fichier, faites clic droit > 7zip > extraire ici, puis ouvrez le dossier et lancez le fichier du logiciel. Ne supprimez jamais ce dossier, car le logiciel fonctionne à partir de celui-ci.

---

## BIOS et personnalisation

Les mots de passe BIOS sont :  
- G8 (2021-2022) : ci5Z7mKU97  
- G9 1ère génération (2022-2023) : 1pvFXs2i5l (souvent changé)  
- G9 2ème génération (2023-2024) et G10 (2024-2025) : en cours de recherche

Pour saisir les chiffres dans le mot de passe BIOS, utilisez la touche Shift (flèche du haut) et non Verr. Maj.  
Pour reconnaître un PC HP G9 1ère génération, cherchez une étiquette HP Wolf Security à côté de l’étiquette Pentium.

Attention : si vous vous connectez à votre compte de la région après avoir déverrouillé le BIOS, il se rebloquera automatiquement avec un mot de passe différent.

---

## Retirer ou personnaliser le logo Pays de la Loire au démarrage

Prérequis : avoir déverrouillé le BIOS et être administrateur.  
Téléchargez « hp-cmsl-1.7.1.exe », installez-le dans le path PowerShell, ouvrez PowerShell en administrateur, tapez `Set-ExecutionPolicy RemoteSigned` puis validez avec « T ». Tapez ensuite `Clear-HPFirmwareBootLogo` pour retirer le logo.

Pour mettre un logo personnalisé, utilisez : `Set-HPFirmwareBootLogo -file votrefichierperso.jpg`  
Le fichier doit être JPEG/JPG, résolution maximale 1024x768, taille inférieure à 32751 octets.

Si un mot de passe BIOS est encore actif, ajoutez un espace puis le mot de passe à la fin de la commande. Il est recommandé de supprimer le mot de passe BIOS dès que possible.  
Des photos explicatives sont disponibles dans le salon Discord <#1278024746113437707>.

---"""