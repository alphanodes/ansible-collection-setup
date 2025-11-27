<?php

if (!extension_loaded('Zend OPcache')) {
	die('You do not have the Zend OPcache extension loaded');
}

$status = opcache_get_status();

if (is_array($status)) {

  if (array_key_exists('scripts', $status)) {
    unset($status['scripts']);
  }

  foreach ($status as $key => $value) {
    if (is_array($value)) {
      foreach ($value as $inner_key => $inner_value) {
        if (!is_array($inner_value)) {
          add_value($inner_key, $inner_value);
        }
        else {
          add_value($inner_key, 'unknown array');
        }
      }
    }
    else {
      add_value($key, $value);
    }
  }
}

function add_value($key, $value) {
  echo $key . ":\t" . $value . "\n";
}
