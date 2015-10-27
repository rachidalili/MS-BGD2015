CREATE OR REPLACE PROCEDURE vstat(idVin INTEGER) AS
--DECLARE
--Selection des regions de production du vin demande (idVin) et le nombre de producteurs/region
  cursor V_REGIONSPROD is Select distinct P.region,count(P.np) as nombreProducteurs from Producteurs P, Recoltes, Vins
                          where P.NP=RECOLTES.NP and VINS.NV=RECOLTES.NV and VINS.NV=idVin
                          group by P.REGION ;
  cursor V_VILLESCLASSEMENTTOTAL is Select distinct lieu,sum(qte) as totalParVille from Achats
                                    where nb=idVin group by lieu order by sum(qte) desc;

  cursor V_VILLESCLASSEMENTANNEE is Select distinct lieu,sum(qte) as totalParVille,extract(year from dates) as annee from Achats
                                    where nb=idVin group by lieu,extract(year from dates) order by sum(qte) desc;

BEGIN
  dbms_output.new_line;
  dbms_output.put_line('Regions de production du vin numero ' || idVin);
   for V_REGION in V_REGIONSPROD loop
      dbms_output.new_line; --retour à la ligne <=> \n
      dbms_output.put_line(chr(9) || V_REGION.region || ' ( ' || V_REGION.nombreProducteurs || ' producteurs)');
   end loop;
  dbms_output.new_line; --retour à la ligne <=> \n
  dbms_output.put_line('Vente du vin numero ' || idVin);
   for V_VILLETOTAL in V_VILLESCLASSEMENTTOTAL loop
      dbms_output.new_line; --retour à la ligne <=> \n
      dbms_output.put_line(chr(9) || V_VILLETOTAL.lieu || ' ( ' || V_VILLETOTAL.totalParVille || ' bouteilles)');
      for V_VILLETOTALPARANNEE in V_VILLESCLASSEMENTANNEE loop
          IF V_VILLETOTALPARANNEE.lieu = V_VILLETOTAL.lieu THEN
              dbms_output.new_line; --retour à la ligne <=> \n
              dbms_output.put_line( chr(9) || chr(9) || V_VILLETOTALPARANNEE.annee || '  : ' || V_VILLETOTALPARANNEE.totalParVille);
          end IF;
      end loop;
   end loop;
END;
/
-- Pour exécuter: 
-- execute vstat(12);