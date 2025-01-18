# Usa la imagen oficial de WordPress como base
FROM wordpress:latest

# Limpia el directorio de WordPress
RUN rm -rf /var/www/html/*

# Copia el archivo wp-config.php personalizado
COPY wp-config.php /var/www/html/wp-config.php

# Habilita el log de errores en PHP
RUN echo "log_errors = On" >> /usr/local/etc/php/conf.d/logging.ini && \
    echo "error_log = /var/log/php-errors.log" >> /usr/local/etc/php/conf.d/logging.ini

# Crea el archivo de log y establece los permisos
RUN touch /var/log/php-errors.log && chmod 777 /var/log/php-errors.log

# Agrega la configuración para el nombre del servidor en Apache
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Exponer el puerto 80 para que Apache sirva el sitio
EXPOSE 80

# Comando por defecto para iniciar Apache
CMD ["apache2-foreground"]
