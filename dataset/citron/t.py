import os

# 1. On se place dans le dossier de travail (le script doit être lancé ici)
folder = os.getcwd()

# 2. Lister et trier les fichiers .jpg
files = sorted(f for f in os.listdir(folder) if f.lower().endswith(".jpg"))

# 3. (Optionnel) Étape de pré‐renommage pour éviter les conflits :
#    on ajoute un préfixe temporaire à tous les fichiers existants
for f in files:
    os.rename(os.path.join(folder, f), os.path.join(folder, "tmp_" + f))

# 4. Renommer définitivement en 1.jpg, 2.jpg, …
files = sorted(f for f in os.listdir(folder) if f.lower().startswith("tmp_") and f.lower().endswith(".jpg"))
for i, tmp_name in enumerate(files, start=1):
    src = os.path.join(folder, tmp_name)
    dst = os.path.join(folder, f"{i}.jpg")
    os.rename(src, dst)

print(f"{len(files)} fichiers renommés de tmp_*.jpg → 1.jpg … {len(files)}.jpg")
