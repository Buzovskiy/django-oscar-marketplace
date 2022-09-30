#### К настройке solr:

1. docker run --restart=always -d -v solr_volume:/opt/solr -p 8983:8983 --name solr-container solr:6.6.6-alpine
2. docker exec -it solr-container solr create_core -c weestepstore.pl
3. python manage.py build_solr_schema --configure-directory=/var/www/weestepuser/data/www/solr_config
4. sudo docker cp ./solr_config/schema.xml solr-container:/opt/solr/server/solr/weestep.eu/conf
5. sudo docker cp ./solr_config/solrconfig.xml solr-container:/opt/solr/server/solr/weestep.eu/conf
6. sudo docker exec -it solr-container ls -al /opt/solr/server/solr/weestep.eu/conf
7. python manage.py build_solr_schema --reload-core weestep.eu
8. python manage.py rebuild_index --noinput
9. sudo docker cp ./solr_config/security.json solr-container:/opt/solr/server/solr/security.json
10. docker restart solr-container