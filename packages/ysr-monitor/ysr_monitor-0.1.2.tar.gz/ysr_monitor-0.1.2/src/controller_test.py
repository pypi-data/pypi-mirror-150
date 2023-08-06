import time
import pathlib
from email_handler import GMailAcc, DriveAcc, SheetsAcc
from httplib2.error import ServerNotFoundError
import os

# todo ensure sensor and other errors work properly - sensor disconnect as warning emails? ensure controller keeps running
# todo build
# todo prevent spam warnings, if warning exists in inbox than do not send another

# data storage globals
DATA_FILE_NAME = 'data.txt'
DATA_FILEPATH = pathlib.Path(__file__).parent.resolve().joinpath(DATA_FILE_NAME)

# required spreadsheets globals
ALERTS_MEMBERS = 'Alerts - Members'
DEFAULT_ALERTS_MEMBERS = ['daniel.js.campbell@gmail.com']

ALERTS_TRACKING = 'Alerts - Tracking'
ENV_LIMITS = 'Environment - Limits'
OPERATING_PARAMETERS = 'Operating - Parameters'
DEFAULT_MEASUREMENT_FREQ = 3600

DEFAULT_SHEET_INFO = dict()

DEFAULT_MIN_TEMP = -10
DEFAULT_MAX_TEMP = 30
DEFAULT_MIN_HUM = 0
DEFAULT_MAX_HUM = 100
DEFAULT_MIN_PRESS = 90
DEFAULT_MAX_PRESS = 110

values = [
    ['Measurement Frequency [s]', DEFAULT_MEASUREMENT_FREQ],
]
body = {
    'values': values
}
DEFAULT_SHEET_INFO[OPERATING_PARAMETERS] = dict()
DEFAULT_SHEET_INFO[OPERATING_PARAMETERS]['body'] = body
DEFAULT_SHEET_INFO[OPERATING_PARAMETERS]['range'] = 'Sheet1!A1:B1'

values = [
    ['', 'Min.', 'Max.'],
    ['Temperature [C]', DEFAULT_MIN_TEMP, DEFAULT_MAX_TEMP],
    ['Pressure [kPa]', DEFAULT_MIN_PRESS, DEFAULT_MAX_PRESS],
    ['Humidity [%]', DEFAULT_MIN_HUM, DEFAULT_MAX_HUM]
]
body = {
    'values': values
}
DEFAULT_SHEET_INFO[ENV_LIMITS] = dict()
DEFAULT_SHEET_INFO[ENV_LIMITS]['body'] = body
DEFAULT_SHEET_INFO[ENV_LIMITS]['range'] = 'Sheet1!A1:D4'

values = [
    ['Members'],
    DEFAULT_ALERTS_MEMBERS,
]
body = {
    'values': values
}
DEFAULT_SHEET_INFO[ALERTS_MEMBERS] = dict()
DEFAULT_SHEET_INFO[ALERTS_MEMBERS]['body'] = body
DEFAULT_SHEET_INFO[ALERTS_MEMBERS]['range'] = 'Sheet1!A1:A2'


class Controller:
    def __init__(self):
        print("Initializing Controller...")

        # messages to send once initialized
        self.warnings = list()
        self.alerts = list()

        self.meas_freq = None

        self.T1 = None
        self.T2 = None
        self.TAvg = None

        self.H1 = None
        self.H2 = None
        self.HAvg = None

        self.P1 = None
        self.P2 = None
        self.PAvg = None

        self.gmail = GMailAcc()
        # self.gmail.clear_inbox()  # clear inbox on init to deal with old alerts

        self.gdrive = DriveAcc()
        self.gsheets = SheetsAcc()

        self.check_sheets()

        self.alerts_members = None
        self.get_alerts_members()

        self.env_limits = self.get_env_limits()
        self.meas_freq = self.get_frequency()

        self.deliver_warnings()
        self.deliver_alerts()

    def run(self, freq):
        """ typical controller run sequence - frequency in seconds [s]"""

        while True:
            self.update_status(freq)
            self.check_data_requests()

            # do shit

            self.deliver_warnings()
            self.deliver_alerts()

            time.sleep(freq)

    def check_data_requests(self):
        """ check for data requests and reply with data if desired """
        try:
            messages = self.gmail.service.users().messages().list(userId='me', labelIds=['INBOX']).execute()['messages']
            messages_ids = [x['id'] for x in messages]

            for mId in messages_ids:
                check = self.gmail.service.users().messages().get(userId="me", id=mId).execute()
                headers = check['payload']['headers']
                subject = [i['value'] for i in headers if i["name"].lower() == 'subject'][0]

                if 'data' in subject.lower():
                    data_from = self.gmail.address
                    data_to = [i['value'] for i in headers if i["name"].lower() == 'from'][0]
                    data_subject = subject
                    data_body = "See up to date measurement data attached."
                    att_fp = DATA_FILEPATH
                    data_response_email = self.gmail.create_message_wAttachment(data_from,
                                                                                data_to,
                                                                                data_subject,
                                                                                data_body,
                                                                                att_fp)
                    self.gmail.send_message(data_from, data_response_email)
                    self.gmail.service.users().messages().delete(userId="me", id=mId).execute()

        except KeyError:
            return

        except ServerNotFoundError:
            return

        return

    def deliver_warnings(self):
        """ send and clear all accumulated warning messages - controller will proceed despite warnings """

        if self.warnings:
            print('Sending warning messages to alerts members')
            for warning_message in self.warnings:
                self.gmail.send_message(self.gmail.address, warning_message)

        self.warnings = list()
        return

    def deliver_alerts(self):
        """ send and clear all accumulated alert messages - controller will not proceed without addressing alerts """

        if self.alerts:
            print('Sending alerts messages to alerts members')
            for alert_message in self.alerts:
                self.gmail.send_message(self.gmail.address, alert_message)

        self.alerts = list()
        return

    def get_alerts_members(self):
        """ get list of alerts - members from column A of sheet """
        print("Fetching Alerts Members...")

        all_sheets = self.gdrive.get_sheets()
        alerts_list = []

        for sheet in all_sheets:
            csheet = self.gsheets.get_sheet(sheet['id'])
            title = csheet['properties']['title']
            if title == ALERTS_MEMBERS:
                try:
                    sheet_temp = self.gsheets.service.spreadsheets().values().get(spreadsheetId=sheet['id'],
                                                                                  range='Sheet1!A:A').execute()['values']
                    # range returns rows as lists, parse into single list
                    alerts_list = [x[0] for x in sheet_temp]

                    # remove non-emails from list
                    for member in alerts_list:
                        if '@' and '.c' not in member:
                            alerts_list.remove(member)
                    self.alerts_members = alerts_list
                except KeyError:  # case where alerts - members sheet is empty
                    alerts_list = DEFAULT_ALERTS_MEMBERS
                    self.alerts_members = alerts_list

                    error_message = "No valid alerts members found in Alerts - Members sheet, please enter valid emails in column A of Alerts - Members. Alerts will only be sent to defaults!"
                    self.log_init_issue(error_message)

                if len(alerts_list) == 0:  # case where no valid email addresses are found
                    alerts_list = DEFAULT_ALERTS_MEMBERS
                    self.alerts_members = alerts_list

                    error_message = "No valid alerts members found in Alerts - Members sheet, please enter valid emails in column A of Alerts - Members. Alerts will only be sent to defaults!"
                    self.log_init_issue(error_message)

        return

    def get_env_limits(self):
        """ get default environment limits from sheet """
        print("Fetching Environment Limits...")

        all_sheets = self.gdrive.get_sheets()
        env_limits = dict()

        for sheet in all_sheets:
            csheet = self.gsheets.get_sheet(sheet['id'])
            title = csheet['properties']['title']
            if title == ENV_LIMITS:
                sheet_temp = self.gsheets.service.spreadsheets().values().get(spreadsheetId=sheet['id'], range='Sheet1!A1:D4').execute()['values']

                env_limits['temp'] = dict()
                env_limits['hum'] = dict()
                env_limits['press'] = dict()

                # set temperature limits
                try:
                    env_limits['temp']['min'] = int(sheet_temp[1][1])
                except (ValueError, IndexError):
                    env_limits['temp']['min'] = DEFAULT_MIN_TEMP
                    error_message = "Temperature Min. in Environment Limits is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MIN_TEMP)
                    self.log_init_issue(error_message)
                try:
                    env_limits['temp']['max'] = int(sheet_temp[1][2])
                except (ValueError, IndexError):
                    env_limits['temp']['max'] = DEFAULT_MAX_TEMP
                    error_message = "Temperature Max. in Environment Limits is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MAX_TEMP)
                    self.log_init_issue(error_message)

                # set pressure limits
                try:
                    env_limits['press']['min'] = int(sheet_temp[2][1])
                except (ValueError, IndexError):
                    env_limits['press']['min'] = DEFAULT_MIN_PRESS
                    error_message = "Pressure Min. in Environment Limits is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MIN_PRESS)
                    self.log_init_issue(error_message)
                try:
                    env_limits['press']['max'] = int(sheet_temp[2][2])
                except (ValueError, IndexError):
                    env_limits['press']['max'] = DEFAULT_MAX_PRESS
                    error_message = "Pressure Max. in Environment Limits is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MAX_PRESS)
                    self.log_init_issue(error_message)

                # set pressure limits
                try:
                    env_limits['hum']['min'] = int(sheet_temp[3][1])
                except (ValueError, IndexError):
                    env_limits['hum']['min'] = DEFAULT_MIN_HUM
                    error_message = "Humidity Min. in Environment Limits is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MIN_HUM)
                    self.log_init_issue(error_message)
                try:
                    env_limits['hum']['max'] = int(sheet_temp[3][2])
                except (ValueError, IndexError):
                    env_limits['hum']['max'] = DEFAULT_MAX_HUM
                    error_message = "Humidity Max. in Environment Limits is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MAX_HUM)
                    self.log_init_issue(error_message)

        return env_limits

    def get_frequency(self):
        """ get measurement frequency from sheet """
        print("Fetching Measurement Frequency...")

        all_sheets = self.gdrive.get_sheets()
        meas_freq = None

        for sheet in all_sheets:
            csheet = self.gsheets.get_sheet(sheet['id'])
            title = csheet['properties']['title']
            if title == OPERATING_PARAMETERS:
                sheet_temp = self.gsheets.service.spreadsheets().values().get(spreadsheetId=sheet['id'], range='Sheet1!A1:D4').execute()['values']

                # set temperature limits
                try:
                    meas_freq = int(sheet_temp[0][1])
                except ValueError:
                    meas_freq = DEFAULT_MEASUREMENT_FREQ
                    error_message = "Measurement Frequency in Operating - Parameters is non-numeric and cannot be parsed, " \
                                    "initialized using default value: {}C".format(DEFAULT_MEASUREMENT_FREQ)
                    self.log_init_issue(error_message)

        return meas_freq

    def log_init_issue(self, message):
        init_from = self.gmail.address
        init_subject = "Initialization Warning"
        message_body = message

        for member in self.alerts_members:
            init_to = member
            init_email = self.gmail.create_message(init_from, init_to, init_subject, message_body)
            self.warnings.append(init_email)

    def check_sheets(self):
        """ check if all sheets present for alerts system """
        print("Checking for required sheets and parameters... ")

        all_sheets = self.gdrive.get_sheets()

        required_titles = [ALERTS_MEMBERS, ALERTS_TRACKING, ENV_LIMITS, OPERATING_PARAMETERS]  # required info for alerts to work properly
        titles = []
        for sheet in all_sheets:
            csheet = self.gsheets.get_sheet(sheet['id'])
            titles.append(csheet['properties']['title'])

        for sheet in required_titles:
            if sheet not in titles:
                print(sheet + ' missing!')
                # create shete if missing
                new_sheet_id = self.gsheets.create_sheet(sheet)
                # update sheet to reflect defaults set above, only params required ofr operation are set as default
                if sheet in DEFAULT_SHEET_INFO.keys():  # only create defaults if set above
                    self.gsheets.edit_sheet(new_sheet_id, DEFAULT_SHEET_INFO[sheet]['range'], DEFAULT_SHEET_INFO[sheet]['body'])
            else:
                print(sheet + ' confirmed')

    def update_status(self, interval):
        """ update controller status via email"""

        status_to = self.gmail.address
        status_from = self.gmail.address
        status_subject = "Status"
        status_body = str(interval)

        status_email = self.gmail.create_message(status_from, status_to, status_subject, status_body)
        self.gmail.send_message(self.gmail.address, status_email)

        return


class EnvError(Exception):
    """ issue with one or more env variables """
    pass


class SensorError(Exception):
    """ issue with one or more env variables """
    pass


def log_env_issue(self, message):
    """ log initialization issues """

    env_from = self.gmail.address
    env_subject = "Environment Warning"
    message_body = message

    for member in self.alerts_members:
        env_to = member
        env_email = self.gmail.create_message(env_from, env_to, env_subject, message_body)
        self.warnings.append(env_email)

    # send warning to self as well to prevent warning spam
    env_to = self.gmail.address
    env_email = self.gmail.create_message(env_from, env_to, env_subject, message_body)
    self.warnings.append(env_email)


if __name__ == '__main__':
    controller = Controller()

    # create warnings

    controller.deliver_warnings()
