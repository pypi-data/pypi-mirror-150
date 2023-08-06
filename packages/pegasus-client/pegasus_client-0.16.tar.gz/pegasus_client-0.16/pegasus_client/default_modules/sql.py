import pymysql
import sqlparse
import yaml
import pyodbc
from rich.console import Console
from rich.table import Table
from rich import print
from pegasus_client.default_modules.generic.clipboard import Clipboard
from tabulate import tabulate
from pegasus_client.default_modules.format import module as format
import base64
import time
import datetime
import traceback


class module:
    """Run a predetermined SQL command. Use 'sql help' for available commands."""

    def __init__(self):
        """Checks all contents exist in the yaml file"""

        config = sql_config().load_config(include_additional=True)

        config_requirements = ['connections',
                               'commands',
                               'queries',
                               'credentials',
                               'settings']

        # check correct sections exist in config
        for section in config_requirements:
            try:
                setattr(self, section, config[section])
            except KeyError:
                raise Exception(f"\nmissing '{section}' from sql.yaml file\n")

    def __run__(self, params=None):

        if self.settings['auto_format_queries']:
            sql_config().reformat_yaml()

        # check a sql command has been passed
        try:
            sql_command = params[0]
        except IndexError:
            raise Exception(
                "SQL command missing, type 'sql help' for available commands")

        sql_param = ' '.join(params[1:])

        # module commands
        command_dispatch = {
            'copy': self.copy_query,
            'view': self.view_queries,
            'help': self.help,
            'encrypt': self.encrypt}

        if sql_command in command_dispatch:
            return command_dispatch[sql_command](sql_param)

        # runs either command or individual query
        if sql_command in self.commands or sql_command in self.queries:
            return self.run_command(sql_command, sql_param)
        else:
            raise ValueError(f'Command not recognised: {sql_command}')

    def run_command(self, command, param):
        """Takes a given command/param and runs it"""

        if command in self.commands:
            try:
                queries = self.commands[command]['queries']
            except KeyError:
                return [f"'query_order' missing from sql.yaml config for command '{command}'."]

        elif command in self.queries:
            queries = [command]

        all_results = []

        border_started = False

        all_results.append(f"%start_row%")
        for index, query in enumerate(queries):

            query_details = self.queries[query]
            try:
                connection_details = self.connections[query_details['connection']]
            except KeyError:
                missing_connection = query_details['connection']
                all_results.append(
                    f"Connection '{missing_connection}' does not exist.")
                continue

            begin = time.time()

            if connection_details['credential'] != 'windows':
                try:
                    credential = sql_config().load_config(
                    )['credentials'][connection_details['credential']]
                except KeyError:
                    raise Exception(
                        f"Credential {connection_details['credential']} is missing, please create a new one.")
            else:
                credential = {
                    'username': 'windows',
                    'password': base64.b64encode('windows'.encode("utf-8"))
                }
            query_results = SQL_Conn().run_query(connection_details,
                                                 query_details['query'], param, credential)
            time_taken = round(time.time()-begin, 2)

            prev_conn = self.queries[queries[index-1]]['connection']
            curr_conn = query_details['connection']

            if curr_conn != prev_conn:
                if border_started == True:
                    all_results.append(f"%end_border%")
                all_results.append(f"%start_border%")
                conn_str = query_details['connection']
                all_results.append(f"%header%{conn_str}")
                border_started = True
            elif index == 0:
                all_results.append(f"%start_border%")
                conn_str = query_details['connection']
                all_results.append(f"%header%{conn_str}")
                border_started = True

            if self.settings['two_columns']:
                all_results.append(f"%start_column%")

            num_rows = len(query_results['results'])
            plural = 's'
            if num_rows == 1:
                plural = ''

            now = datetime.datetime.now().strftime("%H:%M:%S")

            all_results.append(
                f'{ query } | {num_rows} row{plural} | {time_taken}s | {now}')

            all_results.append(query_results)

            if self.settings['two_columns']:
                all_results.append(f"%end_column%")

        if border_started == True:
            all_results.append(f"%end_border%")
        all_results.append(f"%end_row%")

        return all_results

    def subcommands(self):

        # pass back sub-commands (can be called directly without initial command), excludes module commands
        commands_keys = list(self.commands.keys())
        queries = list(self.queries.keys())

        sub_commands = commands_keys + queries

        return sub_commands

    def format_sql(self, query):

        return sqlparse.format(
            query, reindent=True, keyword_case='upper')

    def view_queries(self, command):

        queries = []

        if command not in self.commands and command not in self.queries:
            raise Exception(
                f"Command '{command}' not recognised.")

        if command in self.commands:
            for query in self.commands[command]['queries']:
                queries.append(self.format_sql(query.replace('&p', "''")))

        if command in self.queries:
            sub_commands = [
                query for query in self.queries[command]['query']]
            for comm in sub_commands:
                queries.append(comm)
                for comm in self.commands[comm]['queries']:
                    queries.append(self.format_sql(comm.replace('&p', "''")))

        return queries

    def copy_query(self, command):

        queries = self.commands[command]['queries']
        query_needed = 0
        if len(queries) != 1:
            self.view_queries(command)
            query_needed = int(input('\nquery to copy (number): '))-1

        query = self.format_sql(queries[query_needed])

        query = query.replace('&p', "''")
        Clipboard.add_to_clipboard(query)

        print('\ncopied to clipboard')

    def help(self, command):

        commands = [command for command in self.commands]

        queries = [query for query in self.queries]

        return ['commands', commands, 'queries', queries]

    def encrypt(self, value):

        encrypted = base64.b64encode(value.encode("utf-8"))

        return str(encrypted)


class SQL_Conn:

    def get_connection(self, conn, credentials):

        self.type = conn['type']

        server = conn['server']
        database = conn['database']
        username = credentials['username']
        password = base64.b64decode(credentials['password']).decode("utf-8")
        if self.type == 'mysql':
            self.get_tables = 'SHOW TABLES;'
            self.connection = pymysql.connect(host=server,
                                              user=username,
                                              password=password,
                                              database=database,
                                              cursorclass=pymysql.cursors.DictCursor)

        elif self.type == 'sqlserver':
            self.get_tables = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
            self.connection = pyodbc.connect(
                f'DRIVER=SQL Server; SERVER={server}; DATABASE={database};Trusted_Connection=yes;')

        elif self.type == 'azure':
            self.get_tables = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
            driver = '{ODBC Driver 17 for SQL Server}'
            connection = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={{' + \
                password + '};Authentication=ActiveDirectoryPassword;Encrypt=yes;TrustServerCertificate=YES'
            self.connection = pyodbc.connect(connection)
            self.connection.add_output_converter(-155, str)

        else:
            raise Exception(f"type {self.type} not recognised")

    def run_query(self, conn, query, param=None, credentials=None):

        results = {}
        params = []
        try:
            self.get_connection(conn, credentials)
        except Exception as e:

            return {
                'results': [[traceback.format_exc()]],
                'columns': []
            }

        with self.connection:
            with self.connection.cursor() as cursor:
                if '&p' in query:
                    if not param:
                        # raise ValueError('Missing query parameter')
                        return {
                            'results': [['Error: Missing query parameter']],
                            'columns': []
                        }

                    marker_lookup = {
                        'sqlserver': '?',
                        'mysql': '%s',
                        'azure': '?'
                    }
                    params = [param for i in range(0, query.count('&p'))]
                    query = query.replace('&p', marker_lookup[self.type])
                try:
                    cursor.execute(query, params)
                except Exception as e:
                    return {
                        'results': [[traceback.format_exc()]],
                        'columns': []
                    }

                content = cursor.fetchall()
                if self.type == 'mysql':

                    string_dict = []

                    for row in content:
                        keys_values = row.items()
                        string_dict.append({str(key): str(value)
                                            for key, value in keys_values})

                    results['results'] = [list(i.values())
                                          for i in string_dict]

                else:
                    new_content = []
                    for res in content:
                        new_row = [str(i) for i in res]
                        new_content.append(new_row)

                    results['results'] = new_content

                results['columns'] = [i[0] for i in cursor.description]

                # tables = cursor.execute(self.get_tables).fetchall()
                # results['tables'] = [table[2] for table in tables if table[1]=='dbo']

            self.connection.commit()

        return results


class sql_config:

    def __init__(self):
        pass

    def load_config(self, location='sql.yaml', include_additional=None, only_additional=None):
        try:
            with open(location, 'r') as stream:
                config = yaml.safe_load(stream)
        except FileNotFoundError:
            open("sql.yaml", "x")
            new_config = {
                'commands': {},
                'connections': {},
                'queries': {},
                'credentials': {},
                'settings': {
                    'additional_config': '',
                    'auto_format_queries': False,
                    'better_tables': False,
                    'settings': False,
                    'two_columns': False,
                }
            }
            with open('sql.yaml', 'w') as f:
                yaml.dump(new_config, f, width=2000)

        if include_additional:
            try:
                with open(config['settings']['additional_config'], 'r') as stream:
                    network_config = yaml.safe_load(stream)

                config['queries'] = {
                    **config['queries'],
                    **network_config['queries']}
                config['commands'] = {
                    **config['commands'],
                    **network_config['commands']}
            except FileNotFoundError:
                pass
        elif only_additional:
            with open(config['settings']['additional_config'], 'r') as stream:
                config = yaml.safe_load(stream)

        return config

    def update_config(self, new_config):

        with open('sql.yaml', 'w') as f:
            yaml.dump(new_config, f, width=2000)

    def reformat_yaml(self):
        """Converts any multi-line sql commands into a single line to make the config more readable"""

        doc = self.load_config()

        queries = doc['queries']
        for query in queries:

            formatted_query = queries[query]['query'].replace('\n', '')

            doc['queries'][query]['query'] = formatted_query

        self.update_config(doc)

    def new_query(self, query_command, connection, query):

        config = self.load_config()

        config['queries'][query_command] = {
            'query': query,
            'connection': connection
        }

        self.update_config(config)

    def delete_query(self, query):

        config = self.load_config()

        del config['queries'][query]

        for command in config['commands']:
            if query in config['commands'][command]['queries']:
                config['commands'][command]['queries'].remove(query)

        self.update_config(config)

    def update_settings(self, enabled_settings, additional_config):

        config = self.load_config()

        skip = ['queries', 'commands', 'connections',
                'credentials', 'additional_config']

        config['settings']['additional_config'] = additional_config

        for item in config['settings']:
            if item not in skip:
                if item in enabled_settings:
                    config['settings'][item] = True
                else:
                    config['settings'][item] = False

        self.update_config(config)

    def delete_conn(self, conn):

        config = self.load_config()

        for query in config['queries']:
            if config['queries'][query]['connection'] == conn:
                raise Exception(
                    '(ERROR) Connection is still in use by one or more queries.')

        del config['connections'][conn]

        self.update_config(config)

    def update_conn(self, connection_name, connection_details):

        config = self.load_config()

        config['connections'][connection_name] = connection_details

        self.update_config(config)

    def update_command(self, command_name, queries, query_order):

        config = self.load_config()

        query_order = query_order.split(",")

        query_order = [query.strip()
                       for query in query_order if query.strip() in queries]

        for query in queries:
            if query not in query_order:
                query_order.append(query)

        config['commands'][command_name] = {'queries': query_order}

        self.update_config(config)

    def delete_command(self, command_name):

        config = self.load_config()

        del config['commands'][command_name]

        self.update_config(config)

    def delete_cred(self, cred_name):

        config = self.load_config()

        del config['credentials'][cred_name]

        self.update_config(config)

    def update_cred(self, cred_name, username, password):

        config = self.load_config()

        config['credentials'][cred_name] = {
            'username': username, 'password': base64.b64encode(password.encode("utf-8"))}

        self.update_config(config)
