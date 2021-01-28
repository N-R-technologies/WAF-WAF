import os
from datetime import datetime
from .data.vulnerabilities_info import info
from colors import Colors


class Reporter:
    LOG_FILE_PATH = "network_scanner/data/logs/scan_log_"
    EVIL_TWIN = 0
    BROADCAST = 1
    COMMON_SSID = 2
    COMMON_USERNAME = 3
    COMMON_PASSWORD = 4
    ENGINES = 5
    FIRST_ENGINE = 0
    SECOND_ENGINE = 1

    _conclusions = {Colors.GREEN: "*****************************Scan Conclusions*****************************"}

    def _filter_conclusions(self, results):
        """
        This function will filter the conclusions of
        the last network scan from all the results
        :param results: the results of the scan
        :type results: list
        """
        if results[self.EVIL_TWIN]:
            self._conclusions[Colors.WHITE] = (info["evil twin"])
        if results[self.BROADCAST]:
            self._conclusions[Colors.BEIGE] = (info["open ssid"])
        if results[self.COMMON_SSID]:
            self._conclusions[Colors.BEIGE] = (info["common ssid"])
        if results[self.COMMON_USERNAME] not in ("No-Username", ""):
            self._conclusions[Colors.PURPLE] = (info["common router username"])
        if results[self.COMMON_PASSWORD] not in ("No-Password", ""):
            self._conclusions[Colors.CYAN] = (info["common router password"])
        self._conclusions[Colors.ORANGE] = ""
        if results[self.ENGINES][self.FIRST_ENGINE] == -1:
            self._conclusions[Colors.ORANGE] += ("\nYour network's password is in the common passwords database,"
                                                 " which means it will be\ncracked instantly. "
                                                 "Please make it to stronger and more complex.")
        else:
            if results[self.ENGINES][self.FIRST_ENGINE] != '!':
                self._conclusions[Colors.ORANGE] += '\n' + (results[self.ENGINES][self.FIRST_ENGINE])
            if results[self.ENGINES][self.SECOND_ENGINE] != '!':
                self._conclusions[Colors.ORANGE] += '\n' + (results[self.ENGINES][self.SECOND_ENGINE])
            self._conclusions[Colors.ORANGE] += ("\nRemember, good and strong passwords must contain at least"
                                                 " 8 characters, including\nnumbers, both upper "
                                                 "and lower letters, and special symbols like @, $ and &.")

    def report_conclusions(self, results):
        """
        This function will print the conclusions of the last network scan
        :param results: the results of the scan
        :type results: list
        """
        self._filter_conclusions(results)
        print('\n')
        for color, conclusion in self._conclusions.items():
            print(color + conclusion)
        print(Colors.BLUE)

    def report_log(self):
        """
        This function will write the conclusions of
        the last network scan into a log
        """
        scan_file_path = self.LOG_FILE_PATH + datetime.now().strftime("%d_%m_%Y__%H_%M_%S") + ".txt"
        with open(scan_file_path, 'w') as scan_log:
            for conclusion in self._conclusions.values():
                scan_log.write(conclusion + '\n')
            scan_log.close()
        print(f"\nThe report has also been saved at:\n{os.path.abspath(scan_file_path)}")

    def reset_conclusions(self):
        """
        This function will reset the conclusions of the last network scan
        """
        self._conclusions = {Colors.GREEN: "*****************************Scan Conclusions*****************************"}
