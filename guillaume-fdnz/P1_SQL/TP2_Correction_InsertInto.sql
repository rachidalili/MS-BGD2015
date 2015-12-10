-- Pour assouvir la contrainte d unicité, il faut dans ce cas différencier les dates
-- Insertions dans la table achat de tuples afin de tester la procédire vstat
insert into a values(12, 45, sysdate, 'Paris', 20);
insert into a values(12, 45, sysdate+1, 'Paris', 33);
insert into a values(12, 45, to_date('13/02/2003', 'dd/mm/yyyy'), 'Paris', 10);
insert into a values(12, 45, to_date('14/02/2003', 'dd/mm/yyyy'), 'Paris', 11);
insert into a values(12, 45, sysdate+1, 'Lille', 33);
insert into a values(12, 45, sysdate, 'Lille', 13);
insert into a values(12, 45, to_date('13/02/2001', 'dd/mm/yyyy'), 'Lille', 15);
insert into a values(12, 45, to_date('14/02/2001', 'dd/mm/yyyy'), 'Lille', 16);