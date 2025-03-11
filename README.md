First of all download a version of you full website :
  
Run this command but replace it by the url of the snapshot of your website on wayback machine :
  
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://web.archive.org/web/202/https://YOUR-URL.com/    
  
  
Then run this software and write as an argument the path to the downloaded website like this :   

python  waybackrem.py  "/home/yourname/Téléchargements/kite/web.archive.org/web/20250121032/https:/ki.xx"

It will remove all traces of wayback machine on your file. You may have to recode the links to make the website run.

Developer :  

Hamdy Abou El Anein
hamdy.aea@protonmail.com 
