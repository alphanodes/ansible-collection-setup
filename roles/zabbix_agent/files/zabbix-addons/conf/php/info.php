<?php
declare(strict_types=1);

/**
 * Exposes the full PHP runtime configuration in JSON, matching the FPM context.
 * Ideal for monitoring tools that should not rely on phpinfo() HTML parsing.
 */

if (!headers_sent()) {
    header('Content-Type: application/json; charset=UTF-8');
    header('Cache-Control: no-cache, no-store, must-revalidate');
}

/**
 * Safe wrapper around ini_get_all() in case the function is disabled.
 *
 * @param bool $details true => include local/global/access, false => current values only
 */
function collectIniSettings(bool $details = false): array
{
    try {
        $settings = ini_get_all(null, $details);
    } catch (Throwable $exception) {
        return [
            '_error' => sprintf(
                'ini_get_all failed (%s): %s',
                get_class($exception),
                $exception->getMessage()
            ),
        ];
    }

    if ($settings === false) {
        return [
            '_error' => 'ini_get_all unavailable (possibly disabled in php.ini)',
        ];
    }

    ksort($settings);

    if ($details) {
        foreach ($settings as $name => $info) {
            if (!is_array($info)) {
                $settings[$name] = ['value' => $info];
                continue;
            }

            ksort($info);
            $settings[$name] = array_filter(
                [
                    'local_value' => $info['local_value'] ?? null,
                    'global_value' => $info['global_value'] ?? null,
                    'access' => $info['access'] ?? null,
                ],
                static fn ($value): bool => $value !== null
            );
        }
    }

    return $settings;
}

/**
 * Collect information about loaded PHP and Zend extensions.
 */
function collectExtensions(): array
{
    $phpExtensions = get_loaded_extensions(false);
    $zendExtensions = get_loaded_extensions(true);

    sort($phpExtensions);
    sort($zendExtensions);

    $phpExtensionInfo = [];
    foreach ($phpExtensions as $extension) {
        $phpExtensionInfo[$extension] = phpversion($extension) ?: null;
    }

    return [
        'php' => $phpExtensionInfo,
        'zend' => $zendExtensions,
    ];
}

$iniScanned = php_ini_scanned_files();
$iniScannedFiles = $iniScanned !== false && $iniScanned !== ''
    ? array_map('trim', explode(',', $iniScanned))
    : [];
$iniScannedFiles = array_values(array_filter($iniScannedFiles, static fn (string $file): bool => $file !== ''));

$payload = [
    'timestamp' => gmdate('c'),
    'sapi' => PHP_SAPI,
    'php_version' => PHP_VERSION,
    'php_version_id' => defined('PHP_VERSION_ID') ? PHP_VERSION_ID : null,
    'zend_version' => zend_version(),
    'os' => [
        'php_os' => PHP_OS,
        'php_os_family' => defined('PHP_OS_FAMILY') ? PHP_OS_FAMILY : null,
        'uname' => php_uname(),
    ],
    'paths' => [
        'php_ini_loaded_file' => php_ini_loaded_file(),
        'php_ini_scanned_files' => $iniScannedFiles,
        'extension_dir' => ini_get('extension_dir') ?: null,
        'include_path' => ini_get('include_path') ?: null,
    ],
    'extensions' => collectExtensions(),
    'ini' => [
        'values' => collectIniSettings(false),
        'metadata' => collectIniSettings(true),
    ],
    'server' => [
        'request_uri' => $_SERVER['REQUEST_URI'] ?? null,
        'document_root' => $_SERVER['DOCUMENT_ROOT'] ?? null,
        'script_filename' => $_SERVER['SCRIPT_FILENAME'] ?? null,
        'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? null,
        'server_name' => $_SERVER['SERVER_NAME'] ?? ($_SERVER['HTTP_HOST'] ?? null),
        'hostname' => gethostname() ?: null,
    ],
];

try {
    echo json_encode(
        $payload,
        JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR
    );
} catch (JsonException $exception) {
    if (!headers_sent()) {
        header('Content-Type: text/plain; charset=UTF-8', true, 500);
    }
    echo 'JSON encode failed: ' . $exception->getMessage();
    exit(1);
}
