FROM mysql:5.7
RUN yum install -y php-cli && yum clean all
COPY setup.php /tmp/
COPY setup.sh /docker-entrypoint-initdb.d/
