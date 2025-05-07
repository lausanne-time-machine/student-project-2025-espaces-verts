import geopandas as gpd
import pandas as pd

# Selection du fichier et de la clé csv
chemin_fichier = "C:/Users/maxim/Documents/1888_Renove_Sauvegarde_ZE.gpkg"
chemin_csv = "mapping_macro_all.csv"

# --- Chargements des données ---
gdf = gpd.read_file(chemin_fichier)

# --- Première partie : Regroupement en macro-catégories ---"""
colone_filtre = "class"
colonne = "1888_Registre_use"
non_built = gdf[gdf[colone_filtre] == "non-built"]
valeurs_uniques = non_built[colonne].unique()
liste_valeurs = list(valeurs_uniques)

cat = pd.read_csv("mapping_macro_all.csv")

macro = {
    "foret": cat["Forêt"].unique(),
    "bosquet" : cat["Bosquet"].unique(),
    "pre": cat["Pré"].unique(),
    "champ" : cat["Champ"].unique(),
    "vigne": cat["Verger"].unique(),
    "jardin" : cat["Jardin"].unique(),
    "none ": cat["None"].unique(),
}

for key, value in macro.items():
    macro[key] = value[~pd.isna(value)]

# --- Ajouter la colonne macro_ev à partir du dictionnaire macro ---
def assign_macro(value):
    for key, values in macro.items():
        if value in values:
            return key
    return "inconnu"

# Appliquer uniquement aux parcelles non bâties
gdf["macro_ev"] = gdf.apply(
    lambda row: assign_macro(row[colonne]) if row[colone_filtre] == "non-built" else "bâti",
    axis=1
)

print("Assignation des macro-catégories : Done")

# --- Deuxième partie : Calcul des aires ---"""

# Vérifier la projection de la couche
gdf = gdf.to_crs(epsg=2056)
gdf["area_m2"] = gdf.geometry.area
print("Assigner aire en m2 : Done")

# --- 3. Export en GeoJSON avec couleur par catégorie de macro_ev --- #

gdf["macro_ev"] = gdf["macro_ev"].str.strip()
espaces_verts = gdf[~gdf["macro_ev"].isin(["bâti", "none", "inconnu"])].copy()


# Définir une couleur pour chaque macro catégorie
couleurs = {
    "foret": "#006400",
    "bosquet": "#228B22",
    "pre": "#7CFC00",
    "champ": "#DAA520",
    "vigne": "#8B0000",
    "jardin": "#32CD32",
}

# Ajouter une colonne "color" pour la carto
espaces_verts["color"] = espaces_verts["macro_ev"].map(couleurs).fillna("#999999")

# Exporter en GeoJSON
espaces_verts = espaces_verts.to_crs(epsg=4326)
espaces_verts.to_file("espaces_verts_macro.geojson", driver="GeoJSON", encoding="utf-8")


print("Export GeoJSON : Done")
print("Pipeline terminé avec succès.")