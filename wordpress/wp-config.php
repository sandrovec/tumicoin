<?php
// Información básica de la base de datos
define('DB_NAME', getenv('WORDPRESS_DB_NAME') ?: 'default_db_name');
define('DB_USER', getenv('WORDPRESS_DB_USER') ?: 'default_db_user');
define('DB_PASSWORD', getenv('WORDPRESS_DB_PASSWORD') ?: 'default_db_password');
define('DB_HOST', getenv('WORDPRESS_DB_HOST') ?: 'localhost'); // Cambia localhost por el host de tu base de datos si es necesario
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

// Habilitar el modo de depuración
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
@ini_set('display_errors', 0);

// Claves de autenticación (genera en: https://api.wordpress.org/secret-key/1.1/salt/)
define('AUTH_KEY',         '_o?O>X?+%7Q*cw3ANEW>A9|hWo<zaPo*P+.>kF4ZGk5YF|Wy+3]WNnF&cH^;i!A$');
define('SECURE_AUTH_KEY',  'jRhEWgp>b]?I-`WM>%|Dl,:H6/|-dRZTRI;(@+ ~TV$hz8L-$9_bv.!oEK?QrlQJ');
define('LOGGED_IN_KEY',    ']4T]l-/+WlK?Y`fHzD`KJ-[p,&aeesH%/K1`JmQ?4jxqofI-JnO3fqx5=AtZ2Y1v');
define('NONCE_KEY',        '+E+{s8j}U[QcB2Q[-$s;o,xkF;qBP<5#%r7Z;{9q/$XxU~smQXqFSd(N?w--t6>f');
define('AUTH_SALT',        '<of7sZHCyLKJr7rF:YU$%pS:s}~mvuz40oi4Btb6Kdsz@LBIl%07k)l)cFu4Iq-]');
define('SECURE_AUTH_SALT', 'Krm[?WU*Z/kYXPKYeUAA+*7R=@XP57F]C8|z6`]cRofj/N+e!X&Vsro#[!*YE}dH');
define('LOGGED_IN_SALT',   'h8$U^*aAZ-0~6~RU7j[r/:!I0S!D_!imL2b@t.?-(lUmjHPt+:4HiW<KPP ^R#+e');
define('NONCE_SALT',       ']-W,W<X-31|)QsiXI|sW+$p2aGP_+zyk0vE*7qvvO|W~.F-ASb;:GZR+3c!JM(k(');

// Prefijo de tablas
$table_prefix = 'wp_';

// Configuración de URLs
if ( !defined('ABSPATH') )
    define('ABSPATH', dirname(__FILE__) . '/');

// Incluye los archivos de WordPress
require_once(ABSPATH . 'wp-settings.php');
