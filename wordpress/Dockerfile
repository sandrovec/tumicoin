# Limpia el directorio de WordPress
RUN rm -rf /var/www/html/*

# Copia el archivo de configuración personalizado
COPY wp-config.php /var/www/html/wp-config.php

# Usa la imagen oficial de WordPress
FROM wordpress:latest


# Configuración de PHP para habilitar logs
RUN echo "log_errors = On" >> /usr/local/etc/php/conf.d/logging.ini && \
    echo "error_log = /var/log/php-errors.log" >> /usr/local/etc/php/conf.d/logging.ini

# Crear archivo de log y dar permisos
RUN touch /var/log/php-errors.log && chmod 777 /var/log/php-errors.log

# Copiar wp-config.php personalizado al contenedor
COPY wp-config.php /var/www/html/wp-config.php

# Exponer el puerto 80 para WordPress
EXPOSE 80

# Comando de inicio
CMD ["apache2-foreground"]

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

RUN chmod -R 755 /var/www/html && chown -R www-data:www-data /var/www/html

