# github_killer


## Présentation du projet

Nous nous intéressons dans ce projet à **l'accès aux soins médicaux en France**, au regard d'une analyse économique et spatiale.

En effet, ce sujet est un objet de débat public, alors que les inégalités d'accès aux soins s'aggravent ([Vie publique – Les inégalités territoriales d'accès aux soins](https://www.vie-publique.fr/en-bref/294142-acces-aux-soins-les-inegalites-territoriales-saggravent)) et que les fermetures de lits, de services hospitaliers, voire d'établissements de santé (parfois au profit de l'hospitalisation à domicile), tendent à s'accentuer ([Le Parisien – 2 300 lits fermés en 2024](https://www.leparisien.fr/societe/sante/hopitaux-2-300-lits-fermes-en-2024-en-france-la-baisse-continue-de-saccentuer-09-07-2026-HBEVGFNXHBBFHA7QNAO7OGIZSY.php)).

Nous nous proposons d'étudier divers indicateurs permettant de réfléchir à l'accès aux soins en France. Nous partirons notamment de l'**APL (Accessibilité Potentielle Localisée)**, développé par la DREES pour « mesurer l’adéquation spatiale entre l’offre et la demande de soins de premier recours à un échelon géographique fin » ([DREES – L'accessibilité potentielle localisée](https://data.drees.solidarites-sante.gouv.fr/explore/assets/530_l-accessibilite-potentielle-localisee-apl/)). Nous réfléchirons ensuite à d'autres données susceptibles de nous permettre de visualiser ces disparités géographiques.




### Problématique

**L'accès aux soins médicaux en France est-il lié au niveau de vie de la population locale, et ce, à plusieurs échelles ?**

---

## I. L'Accessibilité Potentielle Localisée : un premier indicateur d'inégalité

Cette première partie, correspondant aux notebooks **I.A et I.B**, vise à proposer une première analyse des inégalités d'accès aux soins médicaux en France, à l'aide de cet indicateur robuste et riche.

On pourra alors s'intéresser aux manifestations différenciées de celles-ci :
- selon l'échelle d'analyse (région, département).
- entre différentes catégories de population, notamment selon l'âge.

Cette première analyse nous pousse à rechercher d'autres données pour observer les inégalités d'accès aux soins en France.

Nous avons ainsi choisi d'utiliser, en complément de l'APL, une base de données recensant les hôpitaux en France métropolitaine, tout en continuant à explorer des données économiques localisées.

## II. Saisir l'accès aux soins à plusieurs échelles et à partir de nouvelles données

Cette deuxième partie, correspondant aux notebooks **II.A et II.B**, propose :
- Une analyse des inégalités d'accès aux soins à l'échelle communale.
- Une analyse des inégalités à l'échelle départementale.
- La mobilisation de nouvelles données pour enrichir les analyses précédentes.

Elle vise à enrichir les intuitions obtenues en première partie et à réfléchir aux types de données les plus pertinents pour répondre à notre problématique.

---

## Conclusion et limites

En conclusion, nous souhaitons revenir sur plusieurs limites de notre méthode. Tout d'abord, la distinction entre **secteur public et secteur privé**, que nous aurions aimé effectuer pour les hôpitaux, n'a pas pu être mise en place à l'échelle de ce projet. De plus, les **DROM ne sont pas inclus dans la base de données sur les hôpitaux en France métropolitaine**, alors même que l'accès aux soins dans ces territoires constitue une question particulièrement riche en elle-même. Enfin, du fait de l'approche purement descriptive et visuelle du problème, les corrélations trouvées ne traduisent a priori des relations causales. 



---

## Ordre d'exécution du code

Les notebooks doivent être exécutés dans l'ordre suivant :

1. `2.`
2. `3.`
3. `4.`
4. `I.A`
5. `I.B`
6. `II.A`
7. `II.B`

---

## Sources et données

Les différentes analyses s'appuient sur les bases de données suivantes :

- **Localisation géographique des hôpitaux**
  - [data.gouv.fr – Localisation des hôpitaux dans OpenStreetMap](https://www.data.gouv.fr/datasets/localisation-des-hopitaux-dans-openstreetmap)

- **Informations socio-économiques localisées**
  - [INSEE – Données socio-économiques](https://www.insee.fr/fr/statistiques/8984752?sommaire=8984758)

- **Accessibilité Potentielle Localisée (APL)**
  - [DREES – Données relatives à l'APL](https://data.drees.solidarites-sante.gouv.fr/explore/?sort=modified&exclude.keyword=Datavisualisations&q=APL&refine.keyword=Professionnel+de+sant%C3%A9)


