manuel = """
**En utilisant ce tutoriel, vous certifiez avoir lu et accepté les conditions d’utilisation.**  
**Veuillez suivre attentivement les étapes suivantes. Si vous commettez des erreurs, cela ne sera pas de notre responsabilité.**
---
# 1 - ADMIN PC SANS BITLOCKER

## ⚙️ Préparation de l’installation

### 1️⃣ Branchement et téléchargement

- Branchez votre PC tout au long de l'opération.
- Téléchargez la version de Windows de votre choix via ce lien : [Windows ISO](https://pcpdl.live/liens-utiles/).
- Formatez votre clé USB au format **NTFS** (clic droit sur la clé, puis "Formater").
- Ouvrez le fichier ISO en double-cliquant dessus.
- Sélectionnez tous les fichiers, copiez-les, puis collez-les sur votre clé USB.
- Ajoutez également ce fichier : [wifi](https://pcpdl.live/liens-utiles/) sur la clé USB (sauf si vous avez un câble ethernet).

## 🔄 Démarrage et installation

### 2️⃣ Accéder au menu de dépannage

- Branchez votre clé USB sur le PC.
- Redémarrez votre PC en maintenant la touche `Shift` (majuscule) pour accéder au menu de dépannage.
- Allez dans :  
  Options avancées → Voir plus d'options de récupération → Récupération de l'image système.

### 3️⃣ Lancer l’installation

- Lorsque le PC demande la clé BitLocker, cliquez sur `Ignorer`.
- Si un mot de passe administrateur est demandé, consultez : https://discord.com/channels/1072925050409324644/1153721969762631730/1218272962478735430
- Une fenêtre d'installation de Windows s'ouvrira, fermez-la.
- Cliquez sur :
  1. `Suivant`
  2. `Avancé`
  3. `Installer un pilote`
  4. `OK`
- Un explorateur de fichiers s’ouvrira.
- Accédez à votre clé USB, faites un clic droit sur le fichier `setup`, puis choisissez **Exécuter**.

  ⚠️ *Si le fichier setup n'apparaît pas :*  
  Écrivez `*.*` dans la barre "Nom du fichier", puis validez.

## 🖥️ Installation de Windows

### 4️⃣ Choisir et installer Windows

- Vérifiez la langue, puis cliquez sur `Suivant`.
- Cliquez sur `Installer maintenant`.
- Sélectionnez la version de Windows souhaitée.
- Cliquez sur `Je n'ai pas de clé de produit` (*choisissez la version **Professionnelle** recommandée*).
- Cliquez sur :  
  `Suivant` → `Personnalisé : Installer uniquement Windows`
- Supprimez toutes les partitions, sauf la partition de récupération et votre clé USB !  
  *(À partir d'ici, ne plus éteindre votre PC !)*
- Cliquez sur `Nouveau` → `OK` → `Suivant`.

### 5️⃣ Finalisation de l’installation

- L'installation commencera et le PC redémarrera.
- À la fin de l’installation, utilisez la touche `Shift` pour naviguer dans les options.

## 🔑 Création d’un compte administrateur

### 6️⃣ Activer le compte administrateur

- Sur l'écran de connexion Internet, maintenez `Shift` et appuyez sur `F10` pour ouvrir une fenêtre de commande.
- Tapez la commande suivante et appuyez sur `Entrée` :

```cmd
net user administrateur /active:yes
```

- Ajoutez un nouvel utilisateur :

```cmd
net user /add username password
```
Remplacez `username` par le nom d'utilisateur de votre choix (**sans espace**).  
Remplacez `password` par le mot de passe souhaité (**sans espace**).  
Pour afficher un nom complet, ajoutez `/fullname:"Prénom Nom"` après `password`.

- Ajoutez l'utilisateur aux administrateurs :

```cmd
net localgroup administrateurs username /add
```
*(Si Windows est en anglais, remplacez `administrateur` par `administrator` et `administrateurs` par `administrators`.)*

### 📶 Installer le pilote Wi-Fi (sauf si vous avez un câble ethernet)

1. Tapez :
   ```cmd
   explorer.exe
   ```
   Une fenêtre d'explorateur Windows s'ouvrira.
2. Allez dans la clé USB et ouvrez `sp150721.exe`, installez-le et attendez quelques instants.
3. Revenez sur l’invite de commandes et tapez :
   ```cmd
   cd oobe
   ```
   puis :
   ```cmd
   msoobe.exe
   ```
   Attendez **30 secondes**, même si le message "Veuillez patienter..." persiste.
4. *Forcer l'arrêt de l'ordinateur* : Maintenez le bouton d'alimentation enfoncé.
5. Redémarrez votre PC et connectez-vous avec le compte créé.

### ❌ Retirer le compte administrateur de la connexion

Ouvrez une invite de commande en tant qu'administrateur et tapez :

```cmd
net user administrateur /active:no
```

Connectez-vous à un réseau Wi-Fi et effectuez les mises à jour Windows !

---

# 2 - ADMIN PC PREMIER DÉMARRAGE

## 🛠️ Étapes à suivre

1️⃣ Sur la page de demande de l'e-mail, maintenez la touche **Majuscule/Shift** et appuyez sur **F10** pour ouvrir une fenêtre de commande.

2️⃣ Tapez :
```cmd
net user administrateur /active:yes
```

3️⃣ Tapez ensuite :
```cmd
net user /add username password
```
Remplacez `username` par le nom d'utilisateur de votre choix (**sans espace**).  
Remplacez `password` par le mot de passe souhaité (**sans espace**).  
Optionnel : ajoutez `/fullname:"Prénom Nom"` après le mot de passe.

4️⃣ Ajoutez l'utilisateur au groupe Administrateurs :
```cmd
net localgroup administrateurs username /add
```
*(Si votre installation est en anglais, remplacez `administrateur` par `administrator` et `administrateurs` par `administrators`.)*

5️⃣ Tapez :
```cmd
cd oobe
```

6️⃣ Exécutez la commande suivante :
```cmd
msoobe.exe
```

7️⃣ Votre ordinateur affichera "Veuillez patienter...".  
Attendez 30 secondes.

8️⃣ Même si le message "Veuillez patienter..." est toujours affiché, forcez l'arrêt de votre ordinateur en maintenant le bouton d’allumage enfoncé.

9️⃣ Une fois votre ordinateur éteint, rallumez-le.

🔟 Votre ordinateur est maintenant déverrouillé.  
Vous pouvez vous connecter en utilisant le compte que vous avez créé.

### ❌ Retirer le compte administrateur de la connexion

Ouvrez une invite de commande en tant qu'administrateur et tapez :

```cmd
net user administrateur /active:no
```

## 🎁 Bonus

En débridant votre ordinateur, vous avez maintenant les permissions administrateur sur votre compte.

**Note importante :**  
Les créateurs de ce tutoriel ne sont pas affiliés à la région Pays de la Loire, Windows, HP ou Microsoft.  
Ils ne peuvent être tenus responsables en cas de dommages causés par une mauvaise utilisation de ce tutoriel.  
Vidéo explicative : [ici](https://youtu.be/xctHB2zrns4?si=-QzJUdmTmiEvvzNy) (à partir de 2 minutes).

---

# 3 - REVENIR SOUS LA RÉGION

Si jamais vous rencontrez des problèmes, vous pouvez à tout moment revenir sur le système de la région.

- Si votre PC n'est pas modifié : suivez le tutoriel <#1072932101034356757>, et lors du choix du réseau, sélectionnez votre réseau, cliquez sur Suivant et patientez.  
  Si vous voyez un texte comme « Bienvenue chez Conseil Régional des Pays de la Loire – Direction des Lycées ! » ou un logo de la région, saisissez votre adresse email de la région (prenom.nom@[RNE DE VOTRE LYCEE].paysdelaloire.education) puis votre mot de passe.

- Si votre PC est modifié (et que vous avez bien tout configuré sur les permissions **Administrateur**) : faites `Win + R`, tapez « sysprep » et validez.  
  Sur "l'action de nettoyage du système", choisissez « Entrer en mode OOBE (Out-Of-Box Experience) » et « Redémarrer », puis cliquez sur « OK ».  
  Patientez et suivez les instructions à l'écran.  
  Si `sysprep` ne fonctionne pas, suivez la procédure du PC non modifié.

> Votre fenêtre doit être configurée comme sur la photo dans le salon <#1140219251379146873>.

---

# 4 - ACTIVATION DES SERVICES MICROSOFT

## Activation d'Office sans email scolaire

⚠️ **Avertissement :** Pour commencer ce tutoriel, veuillez avoir installé la dernière version d'Office (Office 2021).

### Étape 1

Appuyez sur `Win + R` sur votre clavier.  
Dans la boîte de dialogue **Exécuter**, tapez `PowerShell` puis faites `Ctrl + Shift + Entrée`.

### Étape 2

Dans PowerShell, tapez la commande suivante puis appuyez sur Entrée :
```powershell
irm https://get.activated.win | iex
```

### Étape 3

Une deuxième fenêtre s'ouvre, entrez d'abord le numéro 2, puis le numéro 1.

### Fin du tutoriel

Patientez jusqu'à la fin du chargement, puis fermez la page.

---
# 5 - RETIRER LE LOGO DE DÉMARRAGE

Se référer au contenu du salon <#1278024746113437707> qui est très explicite.
"""