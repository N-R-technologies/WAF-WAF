from network_scanner.scan_functions import ScanFunctions


class EngineError(Exception):
    """
    This class will handle errors if one of the engines
    cant work properly with the given password
    """
    def __init__(self, engine_num):
        self._engine_num = engine_num

    def __str__(self):
        return "Engine number: " + str(self._engine_num) + " cant work properly with your password"


class InvalidChar(Exception):
    """
    This class will handle errors if the password
    contains non ascii characters
    """
    def __init__(self, invalid_char):
        self._invalid_char = invalid_char

    def __str__(self):
        return "Your password contains an invalid character: " + self._invalid_char + " so unfortunately we cant analyze it"


class PasswordEngines:
    KEYS_PER_SECOND = 17042497

    def _convert_to_suitable_format(self, estimated_time):
        """
        This function will convert the estimated time
        from seconds to a more suitable format
        :param estimated_time: the estimated time in seconds
        :type estimated_time: int
        :return type: the new type
        :return estimated_time: the new estimated time (no longer in seconds)
        :rtype type: string
        :rtype estimated_time: int
        """
        time_type = ""
        if estimated_time < 60:
            time_type = "seconds"
        elif (estimated_time > 60) and (estimated_time < 60 * 60):
            time_type = "minutes"
            estimated_time = estimated_time / 60
        elif (estimated_time > 60 * 60) and (estimated_time < 60 * 60 * 24):
            time_type = "hours"
            estimated_time = estimated_time / (60 * 60)
        elif (estimated_time > 60 * 60 * 24) and (estimated_time < 60 * 60 * 24 * 30):
            time_type = "days"
            estimated_time = estimated_time / (60 * 60 * 24)
        else:
            time_type = "months"
        return time_type, int(estimated_time)

    def _estimated_crack_time_format(self, estimated_time, time_type, engine_num):
        """
        This function will print the estimated time
        it would take to crack your password
        :param estimated_time: the estimated time ot would take to crack your password
        :param time_type: the type of the time (like hours or minutes)
        :param engine_num: the number of the engine which calculated this time
        :type estimated_time: int
        :type time_type: string
        :type engine_num: int
        :return: the estimated crack time
        :rtype: string
        """
        time_to_crack = ""
        if time_type != "months":
            time_to_crack = str(estimated_time) + ' ' + time_type
        else:
            time_to_crack = "more than a month"
        return(f"Engine number {str(engine_num)} calculated that it would take about "
               f"{time_to_crack} to crack your password.")

    def _analyze_password(self, password):
        """
        This function will analyze the password and will check its content
        :param password: the password
        :type password: string
        :return attributes_lst: list of all attributes of password
        :rtype: list
        """
        have_upper_case = False
        have_lower_case = False
        have_numbers = False
        have_symbol = False
        list_symbols = ['@', '_', '!', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', "\\", '|', '}',
                        '{', '~', ':', ']', '+', '=', '.', '`', ';', "'", '-', '"']
        for char in password[:-1]:
            if char.isnumeric():
                have_numbers = True
            elif char.islower():
                have_lower_case = True
            elif char.isupper():
                have_upper_case = True
            elif char in list_symbols:
                have_symbol = True
            else:
                raise InvalidChar(char)
        return [have_lower_case, have_upper_case, have_numbers, have_symbol]

    def _first_engine(self, password):
        """
        This function will calculate with a mathematical formula how long
        it would take to crack the password with brute force attack
        :param password: the password
        :type password: string
        :return: the time in seconds it would take to crack your password
        :rtype: int
        """
        have_lower, have_upper, have_numbers, have_symbols = self._analyze_password(password)
        password_type = 0
        if have_lower:
            password_type += 26
        if have_upper:
            password_type += 26
        if have_numbers:
            password_type += 10
        if have_symbols:
            password_type += 30
        combinations = password_type ** len(password)  # ** - means pow
        crack_time_seconds = combinations / self.KEYS_PER_SECOND
        if crack_time_seconds < 1:
            return 0
        return crack_time_seconds

    def _second_engine(self, password):
        """
        This function will calculate with static table how long
        it would take to crack the password with brute force attack
        :param password: the password
        :type password: string
        :return: the time in seconds it would take to crack your password
        :rtype: int
        """
        have_lower, have_upper, have_numbers, have_symbols = self._analyze_password(password)
        password_length = len(password)
        time_crack_table = [[0, 0, 3, 10], [0, 8, 180, 780],
                            [0, 300, 10800, 61200], [4, 345600, -1, -1],
                            [40, -1, -1, -1], [360, -1, -1, -1],
                            [3600, -1, -1, -1], [39600, -1, -1, -1], [345600, -1, -1, -1]]
        time_in_seconds = 0
        if password_length > 14:
            time_in_seconds = 1000000
        elif password_length < 5:
            time_in_seconds = 0
        else:
            if have_numbers and have_upper and have_lower and have_symbols:
                password_strength = 3
            elif have_numbers and have_upper and have_lower:
                password_strength = 2
            elif have_upper and have_lower and not have_symbols:
                password_strength = 1
            elif have_numbers and not (have_upper or have_lower or have_symbols):
                password_strength = 0
            else:
                raise EngineError(2)
            time_in_seconds = time_crack_table[password_length - 5][password_strength]
            if time_in_seconds == -1:
                time_in_seconds = 1000000
        return time_in_seconds

    def password_engines(self, password):
        """
        This function will print the estimated time it would take
        to crack the password according to two separate engines
        :param password: the password
        :type password: string
        :return: the estimated crack time the engines calculated
        :rtype: list
        """
        engines = [self._first_engine, self._second_engine]
        est_times = []
        common_password = [-1, -1]
        if ScanFunctions.find_in_file(password, "network_scanner/network_scanner_data/passwords.txt"):
            return common_password
        else:
            for engine in engines:
                try:
                    time_type, est_time = self._convert_to_suitable_format(engine(password))
                except Exception as e:
                    print(e.__str__())
                    est_times.append('!')
                else:
                    est_times.append(self._estimated_crack_time_format(est_time, time_type, engines.index(engine) + 1))
        return est_times
