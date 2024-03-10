% domaines
maison(1..5). 
couleur(rouge;verte;blanche;jaune;bleue).
nationalites(britannique;suedois;danois;norvegien;allemand).
animaux(chien;chats;chevaux;poissons;oiseaux).
boissons(cafe;the;lait;biere;eau).
cigarettes(pallmall;dunhill;blend;bluemaster;princess).

% Génération
% Note : il y a une équivalence dans les contraintes.
% Couleur de la maison.
1 { couleur(Maison, Couleur) : couleur(Couleur) } 1 :- maison(Maison).
1 { couleur(Maison, Couleur) : maison(Maison) } 1 :- couleur(Couleur).
% Nationalité du propriétaire.
1 { nationalite(Maison, Nationalite) : nationalites(Nationalite) } 1 :- maison(Maison).
1 { nationalite(Maison, Nationalite) : maison(Maison) } 1 :- nationalites(Nationalite).
% Animal possédé par le propriétaire.
1 { animal(Maison, Animal) : animaux(Animal) } 1 :- maison(Maison).
1 { animal(Maison, Animal) : maison(Maison) } 1 :- animaux(Animal).
% Boisson préférée du propriétaire.
1 { boisson(Maison, Boisson) : boissons(Boisson) } 1 :- maison(Maison).
1 { boisson(Maison, Boisson) : maison(Maison) } 1 :- boissons(Boisson).
% Cigarettes préférées du propriétaire.
1 { fume(Maison, Cigarette) : cigarettes(Cigarette) } 1 :- maison(Maison).
1 { fume(Maison, Cigarette) : maison(Maison) } 1 :- cigarettes(Cigarette).

% contrainte pour les voisins
a_cote(P1, P2) :- maison(P1), maison(P2), |P1-P2| == 1.

% 1. 
:- couleur(P1, rouge), nationalite(P2, britannique), P1 != P2.

% 2. 
:- nationalite(P1, suedois), animal(P2, chien), P1 != P2.

% 3. 
:- nationalite(P1, danois), boisson(P2, the), P1 != P2.

% 4. 
:- couleur(P1, verte), couleur(P2, blanche), P1 + 1 != P2.

% 5. 
:- couleur(P1, verte), boisson(P2, cafe), P1 != P2.

% 6. 
:- fume(P1, pallmall), animal(P2, oiseaux), P1 != P2.

% 7. 
:- fume(P1, dunhill), couleur(P2, jaune), P1 != P2.

% 8. 
:- not boisson(3, lait).

% 9.
:- not nationalite(1, norvegien).

% 10.
:- fume(P1, blend), animal(P2, chats), not a_cote(P1, P2).

% 11. 
:- fume(P1, dunhill), animal(P2, chevaux), not a_cote(P1, P2).

% 12.
:- fume(P1, bluemaster), boisson(P2, biere), P1 != P2.

% 13.
:- nationalite(P1, allemand), fume(P2, princess), P1 != P2.

% 14. 
:- nationalite(P1, norvegien), couleur(P2, bleue), not a_cote(P1, P2).

% 15. 
:- fume(P1, blend), boisson(P2, eau), not a_cote(P1, P2).

a_poissons(Nationalite) :- 
    nationalite(Maison, Nationalite), 
    animal(Maison, poissons). 

#show a_poissons/1.

% celui qui possede des poissons est:
% Reading from cassetete.lp
% Solving...
% Answer: 1
% a_poissons(allemand)
% SATISFIABLE
% donc c'est l'Allemand!