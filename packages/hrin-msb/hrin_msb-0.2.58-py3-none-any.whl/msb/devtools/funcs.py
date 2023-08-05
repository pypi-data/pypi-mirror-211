from msb.env import NameConst, PathConst

from .dataclasses import DbVendorConfig


def log_to_console(msg, format=False, sep="\n"):
	if format:
		_sep = '#' * ((len(msg) if 30 <= len(msg) <= 100 else 100)+10)
		msg = f"\n{_sep}\n##  {msg.capitalize()}\n{_sep}\n"
	return print(msg)


def get_django_db_vendor_config(db_connection) -> DbVendorConfig:
	from .constants import DJANGO_MIGRATION_DB_VENDOR_CONFIG
	if db_connection and hasattr(db_connection, 'vendor'):
		return DJANGO_MIGRATION_DB_VENDOR_CONFIG.get(getattr(db_connection, 'vendor'))
	return None


def init_django_app(settings_dir: str = NameConst.APP_DIR_NAME, *sys_pathlist, **kwargs):
	import django, sys, os
	sys.path.extend([*PathConst.SYS_PATH_LIST, *sys_pathlist])
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"{settings_dir}.settings")
	os.environ.setdefault("PYTHONUNBUFFERED", "1")

	django.setup()


def require_django(_func):
	def inner_func(*args, **kwargs):
		init_django_app()
		return _func(*args, **kwargs)

	return inner_func
