import logging
from argparse import ArgumentParser

from msb.env import Config
from msb.env import NameConst, PathConst
from .constants import (REGEX_TO_SELECT_ENV_VARIABLE, REGEX_TO_REPLACE_ENV_VARIABLE)
from .django import (DjangoMigration, DjangoFixtures)
from .funcs import (require_django, log_to_console)


def build_prod_env_file_from(dev_env_file_path: str = None, prod_env_file_path: str = None):
	import os, re

	dev_env_file_path = dev_env_file_path or PathConst.DEV_ENV_FILE_PATH
	prod_env_file_path = prod_env_file_path or PathConst.PROD_ENV_FILE_PATH

	if os.path.isfile(dev_env_file_path) and os.path.isfile(prod_env_file_path):
		with open(dev_env_file_path, "r+") as dev_env_file:
			dev_env_file_content = dev_env_file.read()

		prod_env_file_content = re.sub(
			REGEX_TO_SELECT_ENV_VARIABLE, REGEX_TO_REPLACE_ENV_VARIABLE, dev_env_file_content
		)

		with open(prod_env_file_path, "w+") as prod_env_file:
			prod_env_file.write(prod_env_file_content)


@require_django
class MsbAppSetupTask:

	@property
	def is_local_env(self):
		from django.conf import settings
		return self.env.lower() == NameConst.LOCAL_ENV_NAME and settings.IS_LOCAL_ENVIRONMENT

	def _initialize_setup_environment(self):
		parser = ArgumentParser(description='Run Msb Setup Script For Django Application')
		parser.add_argument('-env', choices=NameConst.ENV_NAME_LIST, help='Environment Name', required=True)
		args = parser.parse_args()
		self.env = args.env

	def __load_django_db_fixtures(self):
		_fixture_dirs = [NameConst.DEFAULT_FIXTURE_DIR_NAME, *self.fixture_dirs]
		log_to_console(f"Loading Database Fixtures From {_fixture_dirs} Dirs.", format=True)
		database_fixtures = DjangoFixtures(env=self.env)
		database_fixtures.load(*_fixture_dirs)

	def __run_django_db_migrations(self, apps: list, dbs: list, load_fixtures: bool = False, **kwargs):
		try:
			migration = DjangoMigration(env=self.env, **kwargs)
			migration.set_apps_to_migrate(*apps)
			migration.set_dbs_to_migrate(*dbs)
			migration.run()
		except Exception as e:
			logging.exception(e)

	def __init__(self, **kwargs):
		self._initialize_setup_environment()

	def __ask(self, ques: str):
		return str(input(f"{ques}?. : ")).lower().strip(" ")

	def run_database_setup(self, apps: list, dbs: list, fixture_config: dict):

		self.fixture_dirs = fixture_config.get(self.env) or []
		log_to_console(f"Welcome to Database Setup Wizard", format=True)
		print(f"HINT : Reply/Input '1' for yes/agree, anything else to no/skip.\n{'*' * 100}")

		run_db_migrations, drop_tables, load_fixtures = (True, False, True)

		if self.is_local_env:
			if run_db_migrations := bool(self.__ask(f"Run Database Migrations for {apps}")):
				drop_tables = bool(self.__ask("Remove Database tables? This will also remove old migration files."))

			load_fixtures = bool(self.__ask(f"Load Database fixtures for {self.env} Env"))

		if run_db_migrations:
			self.__run_django_db_migrations(
				apps=apps, dbs=dbs, load_fixtures=load_fixtures,
				remove_migration_files=drop_tables,
				drop_tables_from_db=drop_tables,
				db_to_drop_tables_from=[NameConst.DEFAULT_DATABASE_NAME]
			)

		if load_fixtures:
			self.__load_django_db_fixtures()


class MsbAppPreCommitTask:
	pass


def load_database_fixtures(env=None, **kwargs):
	_fixture_dirs = [
		NameConst.DEFAULT_FIXTURE_DIR_NAME,
		NameConst.TEST_FIXTURE_DIR_NAME if Config.is_dev_or_test_env() else NameConst.PROD_FIXTURE_DIR_NAME
	]
	database_fixtures = DjangoFixtures().load(*_fixture_dirs)


def fresh_db_setup_task(**kwargs):
	if Config.env_name() not in NameConst.DEV_ENV_NAMES_LIST:
		raise ValueError(f"This Task can Only Be Run For {NameConst.DEV_ENV_NAMES_LIST} Environment")

	migration = DjangoMigration(env=Config.env_name(), **dict(
		remove_migration_files=False,
		drop_tables_from_db=True,
		db_to_drop_tables_from=[NameConst.DEFAULT_DATABASE_NAME]
	))
	migration.set_apps_to_migrate(*kwargs.get('apps', []))
	migration.set_dbs_to_migrate(*kwargs.get('dbs', []))
	migration.run()

	if kwargs.get("load_fixtures", True):
		load_database_fixtures()


@require_django
class MsbSetupTask:
	TASK_FUNCTION_MAPPING = {
		"load_fixtures": {
			"func": load_database_fixtures, "desc": "Loads Database Fixtures", "args": None,
		},
		"fresh_db_setup": {
			"func": fresh_db_setup_task, "args": None,
			"desc": "Initializes cleam Database, by removing all tables and then runs all migrations"
		},
	}

	@property
	def __task_names(self):
		return list(self.TASK_FUNCTION_MAPPING.keys())

	@property
	def __usage_text(self):
		_task_list_template = "[ -t  {} {} ] : {}\n"
		_task_list = []
		for task_name, td in self.TASK_FUNCTION_MAPPING.items():
			_task_list.append(_task_list_template.format(
				task_name, ('*' + td.get('args')) if td.get('args', None) else '', td.get('desc', '')
			))

		_usage_heading = f"python setup.py -t <task_name> -a <task_args>. Refer Below Usage for more details.\n"
		_usage_example = f"HINT : python setup.py -t {self.__task_names[0]} -a arg1=value1  arg2=value2 if any.\n"
		return f"{_usage_heading}{''.join(_task_list)}{_usage_example}\n\n\n"

	def __run_setup_task(self, *args, **kwargs):
		if not callable((task_name := self.TASK_FUNCTION_MAPPING.get(self.task_name, {}).get('func', None))):
			raise ValueError(f"Invalid Task Name {task_name}")

		return task_name(*args, **self.kwargs)

	def __get_user_inputs(self):
		parser = ArgumentParser(prog='Msb Application Setup Task', usage=self.__usage_text)
		parser.add_argument('-t', choices=self.__task_names, help='Task Name', required=True)
		return parser.parse_known_args()

	def __init__(self, **kwargs):
		self.env = Config.env_name()
		kwargs.update({"env": self.env})
		self.kwargs = kwargs

	def run(self):
		try:
			input_args, task_args = self.__get_user_inputs()
			self.task_name = input_args.t
			self.kwargs.update({i.split("=")[0]: i.split("=")[1] for i in task_args if "=" in i})

			return self.__run_setup_task()
		except Exception as e:
			logging.exception(e)
