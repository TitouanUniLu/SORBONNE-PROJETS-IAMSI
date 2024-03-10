% Le nombre de couleurs disponibles (à ajuster selon le problème).
#const n = 4.

% Déclaration des nœuds du graphe.
node(1). node(2). node(3). node(4). node(5). node(6). node(7). 

% Déclaration des arêtes du graphe.
edge()


% Les couleurs disponibles, représentées par des entiers de 1 à n.
color(1..n).

% Assigner une couleur à chaque nœud.
1 { colored(N, C) : color(C) } 1 :- node(N).

% S'assurer que deux nœuds adjacents n'ont pas la même couleur.
:- edge(N1, N2), colored(N1, C), colored(N2, C).


