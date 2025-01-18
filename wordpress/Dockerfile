# Usa la imagen oficial de WordPress como base
FROM wordpress:latest

# Actualiza los repositorios e instala Apache, PHP y la extensión MySQL para PHP 8.2
RUN apt-get update && apt-get install -y apache2 php8.2 libapache2-mod-php php8.2-mysql

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
