%%% MONDE DES BLOCS (DOMAIN) %%%

%%% D�claration des pr�dicats (domain) %%%
pred(on(X,Y)) :- block(X),block(Y).
pred(ontable(X)) :- block(X).
pred(clear(X)) :- block(X).
pred(handempty).
pred(holding(X)) :- block(X).

action(pickup(X)) :- block(X).
pre(pickup(X), clear(X)) :- action(pickup(X)).
pre(pickup(X), ontable(X)) :- action(pickup(X)).
pre(pickup, handempty) :- action(pickup(X)).
del(pickup(X), ontable(X)) :- action(pickup(X)).
del(pickup(X), clear(X)) :- action(pickup(X)).
del(pickup(X), handempty()) :- action(pickup(X)).
add(pickup(X), holding(X)) :- action(pickup(X)).



action(putdown(X)) :- block(X).
pre(putdown(X), holding(X)) :- action(putdown(X)).
del(putdown(X), holding(X)) :- action(putdown(X)).
add(putdown(X), ontable(X)) :- action(putdown(X)).
add(putdown(X), clear(X)) :- action(putdown(X)).
add(putdown(X), handempty()) :- action(putdown(X)).



action(stack(X, Y)) :- block(X), block(Y).
pre(stack(X, Y), holding(X)) :- action(stack(X, Y)).
pre(stack(X, Y), clear(Y)) :- action(stack(X, Y)).
del(stack(X, Y), holding(X)) :- action(stack(X, Y)).
del(stack(X, Y), clear(Y)) :- action(stack(X, Y)).
add(stack(X, Y), handempty()) :- action(stack(X, Y)).
add(stack(X, Y), on(X, Y)) :- action(stack(X, Y)).



action(unstack(X, Y)) :- block(X), block(Y).
pre(unstack(X, Y), on(X, Y)) :- action(unstack(X, Y)).
pre(unstack(X, Y), clear(X)) :- action(unstack(X, Y)).
pre(unstack, handempty) :- action(unstack(X, Y)).
add(unstack(X, Y), holding(X)) :- action(unstack(X, Y)).
add(unstack(X, Y), clear(Y)) :- action(unstack(X, Y)).
del(unstack(X, Y), on(X, Y)) :- action(unstack(X, Y)).
del(unstack(X, Y), handempty()) :- action(unstack(X, Y)).



%%% PROBLEME %%%
%%% Domaine: blockWorld %%%

%%% Declaration of objects (problem)%%%
block(a).
block(b).
block(c).
block(d).

%%% Etat initial %%%
init(clear(c)).
init(on(c,d)).
init(ontable(d)).
init(clear(b)).
init(on(b,a)).
init(ontable(a)).
init(handempty).

%%% But %%%
but(on(a,b)).
but(on(b,c)).
but(on(c,d)).
but(ontable(d)).
but(handempty).

% tout ce qui est d�fini par init(P) est �tabli comme vrai au temps 0
holds(P,0) :- init(P).

% La r�gle force l'ex�cution d'une et une seule action parmi toutes les actions possibles � chaque instant 'T', sauf au dernier instant 'n'
1 { perform(A,T) : action(A) } 1 :- time(T), T != n.

% une action 'A' ne peut avoir lieu � l'instant 'T' que si toutes ses pr�conditions 'P' sont satisfaites � cet instant
:- perform(A,T), not holds(P,T), pre(A,P), action(A), pred(P), time(T).

% si une action 'A' est ex�cut�e � l'instant 'T', tous les effets positifs de cette action sont vrais au temps T+1
holds(P,T+1) :- perform(A,T), add(A,P), action(A), pred(P), time(T).

% un pr�dicat 'P' qui est vrai � l'instant 'T' reste vrai � T+1 sauf si une action effectu�e � 'T' l'annule
holds(P,T+1) :- holds(P,T), not del(A,P), perform(A,T), action(A), pred(P), time(T).

% La r�gle garantit qu'aucune paire d'actions diff�rentes ne peut �tre ex�cut�e au m�me moment
:- perform(A1,T), perform(A2,T), action(A1), action(A2), A1 != A2, time(T).

% tous les pr�dicats d�finissant le but doivent �tre vrais � l'instant final 'n'
:- not holds(P,n), but(P), pred(P).

% D�claration des objets (problem)
#const n=10.
time(0..n).

#show perform/2.
