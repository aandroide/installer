# installer
repo installer

<b>lo-scienziato-pazzo-Installer</b><br>
Un installer dello Scienziato-Pazzo, una volta installato si auto-avvia e scarica lo zip da github, mentre ti mostra la schermata di configurazione iniziale<br>

<b>newVer</b><br>
Tool interno (scritto per python 3) per pubblicare una nuova major release velocemente, procedura
  1) clona il repo e assicurati di essere su master
  2) modifica addon.xml cambiando la versione e inserendo le novità
  3) python newVer.py cartellaGit
  4) recati in cartellaGit e controlla, poi fai il push
