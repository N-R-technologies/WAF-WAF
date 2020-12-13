import re
"""this is the main function which will called from the proxy,
here we will call to all the sub function"""
NO_RISK = 0
UNIMPORTANT_RISK = 1
VERY_LITTLE_RISK = 2
LITTLE_RISK = 3
VERY_LOW_RISK = 4
LOW_RISK = 5
MEDIUM_RISK = 6
LARGE_RISK = 7
HIGH_RISK = 8
VERY_DANGEROUS = 9

BETWEEN_LEN = 7
AND_LEN = 3

def find_sql_injection(request):
    # need to call al the check function and calculate the risk level
    pass


"""check if the user try to run from the input common MySQL function “find_in_set”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def find_in_set(request):
    return MEDIUM_RISK if re.search(r"\bfind_in_set\b.*?\(.+?,.+?\)", request) else NO_RISK


"""check if the user try to run from the input SQLite information disclosure “sqlite_master”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def find_master_access(request):
    return LARGE_RISK if re.search(r"\bsqlite_master\b", request) else NO_RISK


"""check if the user try to run from the input MySQL information disclosure “mysql.user”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_user_disclosure(request):
    return LITTLE_RISK if re.search(r"\bmysql.*?\..*?user\b", request) else NO_RISK


"""check if the user try to run from the input Common SQL command “union select”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_union_select(request):
    return LITTLE_RISK if re.search(r"\bunion\b.+?\bselect\b", request) else NO_RISK


"""check if the user try to run from the input Common SQL command “update”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_update_command(request):
    return LITTLE_RISK if re.search(r"\bupdate\b.+?\bset\b", request) else NO_RISK


"""check if the user try to run from the input Common SQL command “drop”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_drop_command(request):
    return LITTLE_RISK if re.search(r"\bdrop\b.+?\b(database|table)\b", request) else NO_RISK


"""check if the user try to run from the input Common SQL command “delete”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_delete_command(request):
    return LITTLE_RISK if re.search(r"\bdelete\b.+?\bfrom\b", request) else NO_RISK


"""check if the user try to run from the input Common SQL comment syntax
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_comment_syntax(request):
    return VERY_LITTLE_RISK if re.search(r"--.+?", request) else NO_RISK


"""check if the user try to run from the input Common mongoDB commands
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_mongo_db_command(request):
    return MEDIUM_RISK if re.search(r"\[\$(ne|eq|lte?|gte?|n?in|mod|all|size|exists|type|slice|or)\]", request) else NO_RISK


"""check if the user try to run from the input Common C-style comment
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_cstyle_comment(request):
    return LITTLE_RISK if re.search(r" \/\*.*?\*\/", request) else NO_RISK


"""check if the user try to run from the input blind sql benchmark
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_blind_benchmark(request):
    return MEDIUM_RISK if re.search(r"bbenchmark\b.*?\(.+?,.+?\)", request) else NO_RISK


"""check if the user try to run from the input blind sql sleep
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_blind_sql_sleep(request):
    return VERY_LITTLE_RISK if re.search(r"\bsleep\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from the input blind mysql disclosure "load_file"
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_load_file_disclosure(request):
    return LARGE_RISK if re.search(r"\bload_file\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from the input blind mysql disclosure "load_data"
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_load_data_disclosure(request):
    return LARGE_RISK if re.search(r"\bload\b.*?\bdata\b.*?\binfile\b.*?\binto\b.*?\btable\b", request) else NO_RISK


"""check if the user try to run from the input MySQL file write "into outfile"
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_write_into_outfile(request):
    return HIGH_RISK if re.search(r"\bselect\b.*?\binto\b.*?\b(out|dump)file\b", request) else NO_RISK


"""check if the user try to run from the input the command concat
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_concat_command(request):
    return LITTLE_RISK if re.search(r"\b(group_)?concat(_ws)?\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from the input mysql information disclosure
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_information_disclosure(request):
    return LARGE_RISK if re.search(r"\binformation_schema\b", request) else NO_RISK


"""check if the user try to run from input the pgsql sleep command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_sleep_pg_command(request):
    return MEDIUM_RISK if re.search(request, r"\bpg_sleep\b.*?\(.+?\)") else NO_RISK


"""check if the user try to run from input the blind tsql "waitfor"
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_blind_tsql(request):
    return VERY_LOW_RISK if re.search(r"\bwaitfor\b.*?\b(delay|time(out)?)\b", request) else NO_RISK


"""check if the user try to run from input the mysql length command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_length_command(request):
    return VERY_LITTLE_RISK if re.search(request, r"\b(char_|bit_)?length\b.*?\(.+?\)") else NO_RISK


"""check if the user try to run from input the mysql hex/unhex command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_hex_command(request):
    return VERY_LITTLE_RISK if re.search(r"\b(un)?hex\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the mysql to base 64/ from base 64 command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_base64_command(request):
    return VERY_LOW_RISK if re.search(r"\b(from|to)_base64\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL substr command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_substr_command(request):
    return LITTLE_RISK if re.search(r"\bsubstr(ing(_index)?)?\b.*?\(.+?,.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL user command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_user_command(request):
    return VERY_LITTLE_RISK if re.search(r"\b(current_)?user\b.*?\(.*?\)", request) else NO_RISK


"""check if the user try to run from input the SQL version command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_version_command(request):
    return VERY_LITTLE_RISK if re.search(r" \bversion\b.*?\(.*?\)", request) else NO_RISK


"""check if the user try to run from input the SQL system variable command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_system_variable(request):
    return UNIMPORTANT_RISK if re.search(r"@@.+?", request) else NO_RISK


"""check if the user try to run from input the SQL oct command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_oct_command(request):
    return VERY_LITTLE_RISK if re.search(r"\boct\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL ord command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_ord_command(request):
    return VERY_LITTLE_RISK if re.search(r"\bord\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL ascii command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_ascii_command(request):
    return VERY_LITTLE_RISK if re.search(r" \bascii\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL bin command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_bin_command(request):
    return VERY_LITTLE_RISK if re.search(r"\bbin\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL char command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_char_command(request):
    return VERY_LITTLE_RISK if re.search(r"\bcha?r\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL where command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_where_command(request):
    return VERY_LITTLE_RISK if re.search(r"\bwhere\b.+?(\b(not_)?(like|regexp)\b|[=<>])", request) else NO_RISK


"""check if the user try to run from input the SQL if command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_if_command(request):
    return VERY_LITTLE_RISK if re.search(r"\bif\b.*?\(.+?,.+?,.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL ifnull command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_ifnull_command(request):
    return LITTLE_RISK if re.search(request, r"\b(ifnull|nullif)\b.*?\(.+?,.+?\)") else NO_RISK


"""check if the user try to run from input the SQL where command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_where_condition_command(request):
    return LITTLE_RISK if re.search(r"\bwhere\b.+?(\b(n?and|x?or|not)\b|(\&\&|\|\|))", request) else NO_RISK


"""check if the user try to run from input the SQL case command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_case_command(request):
    return VERY_LOW_RISK if re.search(r"\bcase\b.+?\bwhen\b.+?\bend\b", request) else NO_RISK


"""check if the user try to run from input the MSSQL exec command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_exec_command(request):
    return VERY_DANGEROUS if re.search(r"\bexec\b.+?\bxp_cmdshell\b", request) else NO_RISK


"""check if the user try to run from input the SQL create command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_create_command(request):
    return VERY_LOW_RISK if re.search(r"\bcreate\b.+?\b(procedure|function)\b.*?\(.*?\)", request) else NO_RISK


"""check if the user try to run from input the SQL insert command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_insert_command(request):
    return LOW_RISK if re.search(r"\binsert\b.+?\binto\b.*?\bvalues\b.*?\(.+?\)", request) else NO_RISK


"""check if the user try to run from input the SQL insert command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_select_command(request):
    return LITTLE_RISK if re.search(r"\bselect\b.+?\bfrom\b", request) else NO_RISK


"""check if the user try to run from input the PgSQL information disclosure “pg_user”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_user_info_disclosure(request):
    return LARGE_RISK if re.search(r"\bpg_user\b", request) else NO_RISK


"""check if the user try to run from input the PgSQL information disclosure “pg_database”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_db_info_disclosure(request):
    return LARGE_RISK if re.search(r"\bpg_database\b", request) else NO_RISK


"""check if the user try to run from input the PgSQL information disclosure “pg_shadow”
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_shadow_info_disclosure(request):
    return LARGE_RISK if re.search(r"\bpg_shadow\b", request) else NO_RISK


"""check if the user try to run from input the DATABASE command
:param request: the request packet
:type request: integer
:return: the risk level if found, zero if not
:rtype integer"""


def check_db_command(request):
    return VERY_LITTLE_RISK if re.search(r"\b(current_)?database\b.*?\(.*?\)", request) else NO_RISK


def check_common_sql_commands(request):
    dangerous_level = 0
    statements_list = []
    match_list = re.findall(r""";\s*(?:#|--)""", request)
    dangerous_level += len([match for match in match_list if match != ''])
    if ';' in request:
        statements_list = request.split(';')
    else:
        statements_list.append(request)
    if statements_list[-1] == '':
        statements_list = statements_list[:-1]
    for sub_statement in statements_list:
        sub_statement = sub_statement.strip()
        for or_statement in sub_statement.split("or")[1:]: # check for every statement if its an 'or' statement
        logic_statement = re.search(r"""(?P<statement>(?:not\s+)*\s*(?P<operators>.+?<[^=>]+|[^=!<>]+=[^=]+|[^<]+?>[^=]+|.+?(?:==|<=|>=|!=|<>).+?)\s*|(?:not\s+)*.+?\s+(?:(?P<like>like\s+.+)|(?P<betweenand>between\s+.+?and\s+.+)|(?P<in>in\s*\(.+\))))""", or_statement)
            if logic_statement:
                statement = logic_statement.group("statement")
                not_count = statement.count("not")
                statement = statement.replace("not", "")
                is_positive = False
                if not_count % 2 == 0:
                    is_positive = True

                if logic_statement.group("operators"):
                    if '=' in statement:
                        statement = statement.replace('=', "==")
                    elif "<>" in statement:
                        statement = statement.replace("<>", "!=")
                elif logic_statement.group("like"):
                    statement = statement.replace("like", "==")
                elif logic_statement.group("betweenand"):
                    middle_value = statement[:statement.find("between")]
                    lower_value = statement[statement.find("between") + BETWEEN_LEN: statement.find("and")]
                    higher_value = statement[statement.find("and") + AND_LEN:]
                    statement = lower_value " <= " middle_value + " <= " higher_value
                
                try:
                    result = eval(statement)
                    if not is_positive: # eval's result should be the opposite (True -> False | False -> True)
                        result = not result
                    if result # check if the or statement returns true
                        dangerous_level += LARGE_RISK
                    else:
                        dangerous_level += LOW_RISK
                except:  # means that the or statement is incorrect
                    dangerous_level += VERY_LOW_RISK
        #  check the alter table command if exists in the sql statement
        elif re.search(r"""alter\s+table\s+.+?\s+(?:add|drop\s+column)\s+.+""", sub_statement):
            dangerous_level += MEDIUM_RISK
        elif re.search(r"""delete\s+.+?\s+from\s+.+""", sub_statement):
            dangerous_level += HIGH_RISK
        elif re.search(r"""create\s+(?P<createinfo>database|table|index|(?:or\s+replace\s+)?view)\s+.+""", sub_statement):
            dangerous_level += MEDIUM_RISK
        elif re.search(r"""drop\s+(?P<deleteinfo>database|index|table|view)\s+.+""", sub_statement):
            dangerous_level += VERY_DANGEROUS
        elif re.search(r"""where\s+exists\s+.+""", sub_statement):
            dangerous_level += VERY_LOW_RISK
        elif re.search(r"""update\s+.+?\s+set\s+.+""", sub_statement):
            dangerous_level += VERY_LOW_RISK
        elif re.search(r"""truncate\s+table\s+.+""", sub_statement):
            dangerous_level += MEDIUM_RISK
        elif re.search(r"""\binsert\s+into\b""", sub_statement):
            dangerous_level += VERY_LOW_RISK
        elif re.search(r"""select\s+.+?\s+from\s+.+?\s+union(?:\s+all)?\s+select\s+.+?\s+from\s+.+""", sub_statement):
            dangerous_level += MEDIUM_RISK
        elif re.search(r"""select\s+.+?\s+into\s+.+?\s+from\s+.+""", sub_statement): # select into?
            dangerous_level += MEDIUM_RISK
        elif re.search(r"""select.+?from\s+.+""", sub_statement):
            dangerous_level += VERY_LOW_RISK
        grant_revoke_statement = re.search(r"""(?:grant|revoke)(?P<permissions>.+?)on\s+.+?\s+(?:to|from)\s+.+?""", sub_statement)
        if grant_revoke_statement:
            permissions_statement = grant_revoke_statement.group("permissions")
            permission_lst = re.findall(r"""(?:select|delete|insert|update|references|alter|all){1,7}""", permissions_statement)
            if len(permission_lst) > 0:
                if "all" in permission_lst:
                    dangerous_level += VERY_DANGEROUS
                else:
                    if "select" in permission_lst:
                        dangerous_level += MEDIUM_RISK
                    if "delete" in permission_lst:
                        dangerous_level += MEDIUM_RISK
                    if "insert" in permission_lst:
                        dangerous_level += MEDIUM_RISK
                    if "update" in permission_lst:
                        dangerous_level += MEDIUM_RISK
                    if "references" in permission_lst:
                        dangerous_level += LOW_RISK
                    if "alter" in permission_lst:
                        dangerous_level += HIGH_RISK


check_common_sql_commands('')