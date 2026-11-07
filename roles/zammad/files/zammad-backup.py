#!/usr/bin/python3
"""Back up a quiesced Zammad installation and fail on any dump/archive error."""
import datetime
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import time


CONFIG_FILE = Path('/etc/zammad-backup.json')
LOCK_FILE = Path('/run/zammad-backup.lock')
BACKUP_PATHS = ('/opt/zammad/config', '/opt/zammad/storage', '/etc/zammad', str(CONFIG_FILE))


def main():
    os.umask(0o077)
    with open(LOCK_FILE, 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        config = json.loads(CONFIG_FILE.read_text())
        destination = Path(config['directory'])
        destination.mkdir(mode=0o700, parents=True, exist_ok=True)
        for name in BACKUP_PATHS[:2]:
            if Path(name).is_symlink():
                raise RuntimeError('Backup requires a real directory, not a symlink: ' + name)
        running = subprocess.run(
            ['systemctl', 'is-active', '--quiet', 'zammad'], check=False
        ).returncode == 0
        try:
            if running:
                subprocess.run(['systemctl', 'stop', 'zammad'], check=True)
            with tempfile.TemporaryDirectory(prefix='.zammad-', dir=destination) as work:
                work = Path(work)
                env = os.environ.copy()
                env.update(PGHOST=config['host'], PGPORT=str(config['port']),
                           PGDATABASE=config['database'], PGUSER=config['user'],
                           PGPASSWORD=config['password'])
                subprocess.run([config['pg_dump'], '--format=custom',
                                '--file', str(work / 'database.dump')], env=env, check=True)
                with tarfile.open(work / 'files.tar.gz', 'w:gz') as archive:
                    for name in BACKUP_PATHS:
                        if Path(name).exists():
                            archive.add(name, arcname=name.lstrip('/'))
                version = subprocess.check_output(
                    ['dpkg-query', '-W', '-f=${Version}', 'zammad'], text=True
                )
                (work / 'version.txt').write_text(version + '\n')
                stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                target = destination / ('zammad-' + stamp + '.tar')
                partial = work / 'backup.tar'
                with tarfile.open(partial, 'w') as archive:
                    for name in ('database.dump', 'files.tar.gz', 'version.txt'):
                        archive.add(work / name, arcname=name)
                shutil.move(str(partial), target)
                print('Created ' + str(target))
            cutoff = time.time() - int(config['hold_days']) * 86400
            for old in destination.glob('zammad-*.tar'):
                if old.is_file() and not old.is_symlink() and old.stat().st_mtime < cutoff:
                    old.unlink()
        finally:
            if running:
                subprocess.run(['systemctl', 'start', 'zammad'], check=True)


if __name__ == '__main__':
    main()
