""" Main redactor class implementation """

import mimetypes
import os
import sys
import re
import math

from pyredactkit.identifiers import Identifier

id_object = Identifier()
""" Main redactor library """


class Redactor:
    """Redactor class
    Class containing all methods to support redaction
    of sensitive data

    Static variables:
        block (unicode string): To redact sensitive data
    """

    block = "\u2588" * 15

    def __init__(self):
        """
        Class Initialization
        Args:
            None

        Returns:
            None
        """
        self.__allowed_files__ = [
            "text/plain",
            "text/x-python",
            "application/json",
            "application/javascript",
            "text/html",
            "text/csv",
            "text/tab-separated-values",
            "text/css",
            "text/cache-manifest",
            "text/calendar",
        ]

    @staticmethod
    def check_file_type(file):
        """Checks for the supplied file type
        Args:
            file (str): Filename of file to check
        Returns:
            mime (str): Mime type
        """
        if not os.path.isfile(file):
            return (None, None)
        return mimetypes.guess_type(file)[0]

    def get_allowed_files(self):
        """Gets a list of allowed files
        Args:
            None
        Returns:
            allowed_file (list): List of allowed files
        """
        return self.__allowed_files__

    def allowed_file(self, file):
        """Checks if supplied file is allowed
        Checks the supplied file to see if it is in the allowed_files list
        Args:
            file (str): File to check
        Returns:
            False: File not found / File type is not allowed
            True: File is allowed
        """
        if not os.path.isfile(file):
            return False
        return mimetypes.guess_type(file)[0] in self.get_allowed_files()

    def redact(self, line=str, option=str):
        """Main function to redact
        Args:
            line (str) : line to be supplied to redact
            option (str): (optional) choice for redaction

        Returns:
            redacted_line (str): redacted line
        """
        # Refactor this to loop through and check for option.
        redacted_line = ''
        if option in ("dns", "domain"):
            dns = id_object.regexes[1]['pattern']
            redacted_line = re.sub(dns, self.block, line, flags=re.IGNORECASE)
        elif option in ("email", "emails"):
            email = id_object.regexes[0]['pattern']
            redacted_line = re.sub(
                email, self.block, line, flags=re.IGNORECASE)
        elif option in ("ip", "ipv4"):
            ipv4 = id_object.regexes[2]['pattern']
            redacted_line = re.sub(ipv4, self.block, line, flags=re.IGNORECASE)
        elif option in ("cc", "creditcard"):
            cc = id_object.regexes[3]['pattern']
            redacted_line = re.sub(cc, self.block, line, flags=re.IGNORECASE)
        elif option in ("nric", "fin"):
            nric = id_object.regexes[4]['pattern']
            redacted_line = re.sub(nric, self.block, line, flags=re.IGNORECASE)
        elif option == "ipv6":
            ipv6 = id_object.regexes[5]['pattern']
            redacted_line = re.sub(ipv6, self.block, line, flags=re.IGNORECASE)

        return redacted_line

    def redact_name(self, data=str):
        """Main function to redact
        Args:
            data (str) : data to be supplied to identify names

        Returns:
            data (str) : redacted names from the data
            name_count (int) : number of names redacted from the data
        """
        name_list = id_object.names(data)
        name_count = len(name_list)
        for name in name_list:
            data = data.replace(name, self.block)
        return data, name_count

    def process_file(self, filename, option=str, savedir="./"):
        """Function to process supplied file from cli.
        Args:
            filename (str): File to redact
            savedir (str): [Optional] directory to place results

        Returns:
            Creates redacted file.
        """
        count = 0
        try:
            # Open a file read pointer as target_file
            with open(filename, encoding="utf-8") as target_file:
                if savedir != "./" and savedir[-1] != "/":
                    savedir = savedir + "/"

                # created the directory if not present
                if not os.path.exists(os.path.dirname(savedir)):
                    print(
                        "[ + ] "
                        + os.path.dirname(savedir)
                        + " directory does not exist, creating it."
                    )
                    os.makedirs(os.path.dirname(savedir))

                print(
                    "[ + ] Processing starts now. This may take some time "
                    "depending on the file size. Monitor the redacted file "
                    "size to monitor progress"
                )

                # Open a file write pointer as result
                with open(
                    f"{savedir}redacted_{os.path.basename(filename)}",
                    "w",
                    encoding="utf-8",
                ) as result:
                    # Check if any redaction type option is given in argument. If none, will redact all sensitive data.
                    if type(option) is not str:
                        print(
                            f"[ + ] No option supplied, will be redacting all the sensitive data supported")
                        for line in target_file:
                            for p in id_object.regexes:
                                if re.search(p['pattern'], line, re.IGNORECASE):
                                    line = re.sub(p['pattern'], self.block, line,
                                                  flags=re.IGNORECASE)
                            result.write(line)
                            count += 1
                    # Separate option to redact names
                    elif option in ("name", "names"):
                        content = target_file.read()
                        data = self.redact_name(content)
                        result.write(data[0])
                        count = data[1]
                    else:
                        print(f"[ + ] Redacting {option} from the file")
                        for line in target_file:
                            line = self.redact(line, option)
                            result.write(line)
                            count += 1

                    print(f"[ + ] Redacted {count} targets...")
                    print(
                        f"[ + ] Redacted results saved to {savedir}redacted_{os.path.basename(filename)}")

        except UnicodeDecodeError:
            os.remove(f"{savedir}redacted_{os.path.basename(filename)}")
            print("[ - ] Removed incomplete redact file")
            sys.exit("[ - ] Unable to read file")

    def process_report(self, filename):
        """Function to process calculate and generate report of man hour saved.
        Args:
            filename (str): File to count the words

        Returns:
            Creates a report on estimated man hours/minutes saved.
        """
        try:
            # Open a file read pointer as target_file
            with open(filename, encoding="utf-8") as target_file:
                text_chunk = target_file.read()

                # Words per minute
                WPM = 75

                word_length = 5
                total_words = 0
                for current_text in text_chunk:
                    total_words += len(current_text)/word_length

                total_words = math.ceil(total_words)

                # Divide total words by words per minute read to get minutes and hour estimate.
                reading_minutes = math.ceil(total_words/WPM)
                reading_hours = math.floor(reading_minutes/60)

                word_report = f"[ + ] Estimated total words : {total_words}"
                minutes_saved = f"[ + ] Estimated total minutes saved : {reading_minutes}"
                man_hours_saved = f"[ + ] Estimated total man hours saved : {reading_hours}"

                # Open a file write pointer as result
                with open(
                    f"manhours_saved_{os.path.basename(filename)}",
                    "w",
                    encoding="utf-8",
                ) as result:
                    result.write(word_report + "\n" +
                                 minutes_saved + "\n" + man_hours_saved)
                    print(
                        f"[ + ] Estimated man hours saved report saved as manhours_saved_{os.path.basename(filename)}")

        except UnicodeDecodeError:
            os.remove(f"manhour_saved_report_{os.path.basename(filename)}")
            print("[ - ] Removed incomplete report")
            sys.exit("[ - ] Unable to read target file")
