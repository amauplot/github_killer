# github_killer

29/09/2026
Données : 
-	(Mortalité par région/département
https://www.insee.fr/fr/statistiques/2012741#tableau-TCRD_048_tab1_departements)
-	Données géolocalisée des hôpitaux
https://www.data.gouv.fr/datasets/localisation-des-hopitaux-dans-openstreetmap 
	Réussir à transformer données en mode latitude, longitude en quartier (pour marseille, paris, lyon), en ville et département
-(	éventuelle données sur médecin (voir comment récupérer)
https://tableau.ordre.medecin.fr/recherche-avancee?specialite=3&discipline=&titre=&nom=&prenom=&civilite=i&region=11&departement=75&ville=Paris&rue= )
-	Données médecins :
https://www.data.gouv.fr/datasets/annuaire-sante-extractions-des-donnees-en-libre-acces-des-professionnels-intervenant-dans-le-systeme-de-sante-rpps
	A agréger pour en faire un indicateur relativement unique (par échelle d’analyse)
-	Info sur rev localisées
https://www.insee.fr/fr/statistiques/8984752?sommaire=8984758
-	APL 
https://data.drees.solidarites-sante.gouv.fr/explore/?sort=modified&exclude.keyword=Datavisualisations&q=APL&refine.keyword=Professionnel+de+sant%C3%A9 

Objectif : 
Lien implantation hôpitaux et info démographique + revenu/prix du foncier. 
	L’implantation des hôpitaux est-elle liée au niveau de vie de la population locale, et ce à plusieurs échelles (quartier-ville-département) ? Une distinction publique privée pourra être considérée.
Défis : 
Quartier (que Lyon/Paris/Marseille : usage des arrondissements)
Récupérer l’info publique/privée 
Données des médecins : créer une variable médecin/km2 qui pourra enrichir la réflexion (pour quartiers, villes, département)
Prix du foncier de manière précise
Pour la localisation des hôpitaux : transformer les latitude/longitude en => ensuite faire nombre d’hôpital par tête aux différentes échelles
Variables éco : PIB par tête/foncier
Variable démographique : pas oublier la population
