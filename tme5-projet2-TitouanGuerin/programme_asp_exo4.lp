%%% MONDE DES BLOCS (DOMAIN) %%%

%%% Déclaration des prédicats (domain) %%%
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
