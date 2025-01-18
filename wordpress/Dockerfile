# Usa la imagen oficial de WordPress como base
FROM wordpress:latest

# Agrega el repositorio de PHP
RUN apt-get update && apt-get install -y \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    curl && \
    curl -sSL https://packages.sury.org/php/README.txt | bash - && \
    apt-get update

# Instala Apache, PHP, y la extensión MySQL para PHP 8.2
RUN apt-get install -y apache2 php8.2 php8.2-mysql libapache2-mod-php

# Copia los archivos de configuración de Apache y PHP si es necesario
COPY ./config/apache2.conf /etc/apache2/apache2.conf
COPY ./config/php.ini /etc/php/8.2/apache2/php.ini

# Configura los permisos para los archivos y directorios de WordPress
RUN chown -R www-data:www-data /var/www/html
RUN find /var/www/html -type d -exec chmod 755 {} \;
RUN find /var/www/html -type f -exec chmod 644 {} \;

# Exponer el puerto 80 para que Apache sirva el sitio
EXPOSE 80

# Comando por defecto para iniciar Apache
CMD ["apache2-foreground"]
