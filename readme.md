#### К настройке solr:

1. docker run --restart=always -d -v solr_volume:/opt/solr -p 8983:8983 --name solr-container solr:6.6.6-alpine
2. Create core 
```docker exec -it solr-container solr create -c weestepstore.pl -n basic_config``` or  
```docker exec -it solr-container solr create_core -c weestepstore.pl```
3. python manage.py build_solr_schema --configure-directory=/var/www/weestepuser/data/www/weestepstore.pl/project/solr_config
4. docker exec -it solr-container rm /opt/solr/server/solr/weestepstore.pl/conf/schema.xml -f
5. docker exec -it solr-container rm /opt/solr/server/solr/weestepstore.pl/conf/solrconfig.xml -f
6. Проверяем, что файлы schema.xml и solrconfig.xml удалены
```
docker exec -it solr-container ls -al /opt/solr/server/solr/weestepstore.pl/conf/
```
4. sudo docker cp ./solr_config/schema.xml solr-container:/opt/solr/server/solr/weestepstore.pl/conf/schema.xml
5. sudo docker cp ./solr_config/solrconfig.xml solr-container:/opt/solr/server/solr/weestepstore.pl/conf/solrconfig.xml
6. sudo docker exec -it solr-container ls -al /opt/solr/server/solr/weestepstore.pl/conf/
7. python manage.py build_solr_schema --reload-core weestepstore.pl
8. python manage.py rebuild_index --noinput
9. sudo docker cp ./solr_config/security.json solr-container:/opt/solr/server/solr/security.json
10. docker restart solr-container

##### On Windows
1. solr.cmd start
2. solr.cmd create -c weestepstore.pl -n basic_config
3. python manage.py build_solr_schema --configure-directory=C:\Users\buzov\PycharmProjects\solr-6.6.6\server\solr\weestepstore.pl\conf
4. python manage.py build_solr_schema --reload-core weestepstore.pl
5. python manage.py rebuild_index --noinput


##### Frontend for development
https://weestep-kids-sgo8-zkmns-projects.vercel.app/es
https://weestep-kids.vercel.app/