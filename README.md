# github_killer


  Nous nous intéressons dans ce projet à l'accès aux soins médicaux en France au regard d'une analyse économique et spatiale. En effet, ce sujet est un objet de débat public alors que les inégalités d'accès aux soins s'aggravent (https://www.vie-publique.fr/en-bref/294142-acces-aux-soins-les-inegalites-territoriales-saggravent) et que les fermetures de lits, de services hospitaliers, voire d'établissements de santé (parfois au profit d'hospitalisation à domicile) tendent à s'accentuer (https://www.leparisien.fr/societe/sante/hopitaux-2-300-lits-fermes-en-2024-en-france-la-baisse-continue-de-saccentuer-09-07-2026-HBEVGFNXHBBFHA7QNAO7OGIZSY.php). Nous nous proposons de nous pencher sur divers indicateurs permettant de réfléchir à l'accès aux soins en France, en partant de l'APL (Accessibilité Potentielle localisée), développé par la DREES pour "mesurer l’adéquation spatiale entre l’offre et la demande de soins de premier recours à un échelon géographique fin" (https://data.drees.solidarites-sante.gouv.fr/explore/assets/530_l-accessibilite-potentielle-localisee-apl/), puis en réfléchissant à d'autres données qui peuvent nous permettre de visualiser ces disparités géographiques.

Ainsi, l'accès aux soins médicaux en France est-il lié au niveau de vie de la population locale, et, ce, à plusieurs échelles ? 

I . L'Accessibilité Potentielle localisée : un premier indicateur d'inégalité
  Dans cette partie (notebook I.A et I.B) nous chercherons à proposer une première analyse des inégalités d'accès aux soins médicaux en France, à l'aide de cet indicateur robuste et riche. On pourra alors s'intéresser aux manifestations différenciées de celles-ci selon l'échelle d'analyse (région, département) et pour différentes populations (âge).

Cette première partie nous pousse à chercher d'autres données pour observer les inégalités d'accès aux soins en France. Nous avons choisi d'utiliser, en complément de l'APL, une base de données recensant tous les hôpitaux en France métropolitaine tout en continuant à explorer aussi des données économiques localisées.

II. Saisir l'accès aux soins à plusieurs échelles et en utilisant de nouvelles données

Cette partie correspond au notebook II.A et II. B et propose d'une part une analyse à l'échelle locale et une analyse à l'échelle départementale des inégalités d'accès, en mobilisant de nouvelles données. Elle vise à enrichir les intuitions obtenues en partie I et à réfléchir à quelles données permettent de répondre à notre question.

En conclusion, nous voulions revenir sur plusieurs limites de notre méthode. Tout d'abord, la distinction public/privé, que nous aurions aimé effectuer pour les hôpitaux n'a pas pu être mise en place à l'échelle de ce projet. De plus, les DROM ne sont pas inclus dans la base sur les hôpitaux en France métropolitaine alors même que l'accès au soin au sein es DROM est une question riche en elle-même. 


Ordre d'exécution du code :   
1.
2.
3.
4.
I.A
I.B
II.A
II.B

Données : 
-	Données géolocalisée des hôpitaux
https://www.data.gouv.fr/datasets/localisation-des-hopitaux-dans-openstreetmap 
-	Informations socio-économiques localisées
https://www.insee.fr/fr/statistiques/8984752?sommaire=8984758
-	APL 
https://data.drees.solidarites-sante.gouv.fr/explore/?sort=modified&exclude.keyword=Datavisualisations&q=APL&refine.keyword=Professionnel+de+sant%C3%A9 
