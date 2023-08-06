#  """
#    Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
"""
Calculating Yield fraction by the following steps (with elaboration):
1)Counting the unique advas in AdvaProcess class
2)Counting number of tags in CountThread
3)Creating two threads in MultiThreadingCalculation in order to run AdvaProcess instance and CountThread instance
at the same time
4)Calculating the Yield fraction according to the results we got from the instances
5)Creating two threads in MainWindow class in order to calculate the fraction by MultiThreadingCalculation instance
and to run the GUI function (open_session) at the same time.
"""

from wiliot_core import *
import serial.tools.list_ports
import PySimpleGUI as sg
from configs.inlay_data import *
from wiliot_testers.utils.get_version import *
from wiliot_testers.utils.upload_to_cloud_api import *
import serial
import matplotlib.pyplot as plt
from wiliot_testers.tester_utils import dict_to_csv

inlay_types_dict = {item.name: item.value for item in InlayTypes}
today = datetime.date.today()
formatted_today = today.strftime("%Y%m%d")  # without -
formatted_date = today.strftime("%Y-%m-%d")
current_time = datetime.datetime.now()
cur_time_formatted = current_time.strftime("%I%M%S")  # without :
time_formatted = current_time.strftime("%I:%M:%S")


class AdvaProcess(object):
    """
    Counting the number of unique advas
    """

    def __init__(self, stop_event, received_channel, time_profile_val, energy_pattern_val, inlay_type):
        self.gw_instance = WiliotGateway(auto_connect=True,
                                         is_multi_processes=True)  # gw object, in order to connect with gw
        self.all_tags = set()
        self.gw_init()
        self.stop = stop_event
        self.received_channel = received_channel
        self.time_profile_val = time_profile_val
        self.energy_pattern_val = energy_pattern_val
        self.gw_reset_config()
        self.number_of_unq_adva = 0
        self.packets_queue = Queue(maxsize=1000)
        self.inlay_type = inlay_type

    def gw_init(self):
        """
        Initialize the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.reset_buffer()
            self.gw_instance.start_continuous_listener()
        else:
            print("No GateWay, please try to reconnect it.")
            exit()
        return

    def gw_reset_config(self):
        """
        Configs the gateway
        """
        if self.gw_instance.connected:
            self.gw_instance.start_continuous_listener()
            self.gw_instance.reset_gw(reset_port=False)
            self.gw_instance.reset_listener()
            if not self.gw_instance.is_gw_alive():
                print('gw_reset_and_config: wait more time since gw did not respond')
                time.sleep(5)
            self.gw_instance.write('!set_tester_mode 1', with_ack=True)
            self.gw_instance.write('!listen_to_tag_only 1', with_ack=True)
            self.gw_instance.write('!sub1g_sync 1', with_ack=True)
            self.gw_instance.config_gw(received_channel=self.received_channel, time_profile_val=self.time_profile_val,
                                       energy_pattern_val=self.energy_pattern_val,
                                       start_gw_app=False, with_ack=True,
                                       effective_output_power_val=22, sub1g_output_power_val=29)
        else:
            raise Exception('Could NOT connect to GW')

    def run(self):
        """
        Receives available data then counts and returns the number of unique advas
        """
        self.gw_instance.config_gw(start_gw_app=True)
        while not self.stop.is_set():
            time.sleep(0)
            if self.gw_instance.is_data_available():
                packet_list_in = self.gw_instance.get_packets(action_type=ActionType.ALL_SAMPLE,
                                                              tag_inlay=self.inlay_type)
                for packet in packet_list_in:
                    adva = packet.get_adva()
                    self.all_tags.add(adva)
                self.packets_queue.put(packet_list_in)
            else:
                continue
            self.number_of_unq_adva = len(self.all_tags)
            # check gw connection
            if not self.gw_instance.is_connected():
                print('GW was disconnected. trying to initiate connection...')
            if self.gw_instance.get_read_error_status():
                print('A GW reading Error was detected')

        self.gw_instance.exit_gw_api()

    def get_unq_advas(self):
        """
        returns the number of unique advas
        """
        return self.number_of_unq_adva

    def get_packets_queue(self):
        """
        Returns the packet queue that is created above
        """
        return self.packets_queue


class CountThread(object):
    """
    Counting the number of tags
    """

    def __init__(self, stop_event, rows=1):
        self.available_ports = [s.device for s in serial.tools.list_ports.comports()]
        self.get_ports_of_arduino(self)
        self.baud = '9600'
        self.ports = self.get_ports_of_arduino(self)
        try:
            self.comPortObj = serial.Serial(self.ports[0], self.baud, timeout=0.1)
        except serial.SerialException:
            print("NO ARDUINO")
        self.rows = rows
        self.stop = stop_event
        self.tested = 0

    @staticmethod
    def get_ports_of_arduino(self):
        """
        Gets all the ports we have, then chooses Arduino's ports
        """
        arduino_ports = []
        for p in serial.tools.list_ports.comports():
            if 'Arduino' in p.description:
                arduino_ports.append(p.device)
        if not arduino_ports:
            print('NO ARDUINO')
        return arduino_ports

    def run(self):
        """
        Tries to read data and then counts the number of tags
        """
        while not self.stop.is_set():
            time.sleep(1)
            data = ''
            try:
                data = self.comPortObj.readline()
            except Exception as e:
                print(f"NO READLINE: {e}")
            buf = b''
            if data.__len__() > 0:
                buf += data
                if b'\n' in buf:
                    try:
                        tmp = buf.decode().strip(' \t\n\r')
                        if "pulses detected" in tmp:
                            self.tested += self.rows

                    except Exception as e:
                        print(f'Warning: Could not decode counter data or Warning: {e}')
                        continue
        self.comPortObj.close()

    def get_tested(self):
        """
        returns the number of tags
        """
        return self.tested


class MainWindow:
    """
    The main class the runs the GUI and supervise the multi-threading process of fraction's calculation and GUI viewing
    """

    def __init__(self):
        self.adva_process = None
        self.adva_process_thread = None
        self.count_process = None
        self.count_process_thread = None
        self.folder_path = None
        self.py_wiliot_version = None
        self.d = None
        self.yield_test_app_data = None
        self.run_path = None
        self.final_path_run_data = None
        self.run_data_dict = None
        self.tags_num = 0
        self.stop = threading.Event()
        self.neg_col = 0
        self.selected = ''
        self.wafer_lot = ''
        self.wafer_number = ''
        self.operator = ''
        self.run_start_time = ''
        self.tester_type = 'yield-test'
        self.tester_station_name = ''
        self.comments = ''
        self.gw_version = ''
        self.rows_number = 1
        self.upload_flag = True
        self.cmn = ''
        self.final_path_packets_data = ''
        self.seen_advas = set()
        self.result = 0
        self.update_packet_data_flag = False

    def get_result(self):
        """
        Calculates the yield fraction
        """
        unq_advas = self.adva_process.get_unq_advas()
        tags_num = self.count_process.get_tested()
        if tags_num > 0:
            self.result = (unq_advas / tags_num) * 100
        return self.result

    def run(self):
        """
        Viewing the window and checking if the process stops
        """
        self.open_session()
        self.overlay_window()

    def init_run_data(self):
        self.py_wiliot_version = get_version()
        self.d = WiliotDir()
        self.d.create_tester_dir(tester_name='yield_tester')
        self.yield_test_app_data = self.d.get_tester_dir('yield_tester')
        self.cmn = self.wafer_lot + '.' + self.wafer_number
        self.run_path = os.path.join(self.yield_test_app_data, self.cmn)
        if not os.path.exists(self.run_path):
            os.makedirs(self.run_path)
        self.cmn = self.wafer_lot + '.' + self.wafer_number + '_' + formatted_today + '_' + cur_time_formatted
        self.folder_path = os.path.join(self.run_path, self.cmn)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        self.final_path_run_data = os.path.join(self.folder_path, self.cmn + '@run_data.csv')
        self.gw_version = self.adva_process.gw_instance.get_gw_version()[0]
        start_time = datetime.datetime.now()
        self.run_start_time = start_time.strftime("%I:%M:%S")
        value = csv_dictionary[self.selected]
        self.run_data_dict = {'common_run_name': self.cmn, 'tester_station_name': self.tester_station_name,
                              'operator': self.operator,
                              'run_start_time': formatted_date + ' ' + self.run_start_time, 'run_end_time': '',
                              'wafer_lot': self.wafer_lot, 'wafer_number': self.wafer_number,
                              'tester_type': self.tester_type,
                              'comments': self.comments, 'inlay': self.selected, 'total_run_tested': 0,
                              'total_run_responding_tags': 0,
                              'gw_version': self.gw_version,
                              'py_wiliot_version': self.py_wiliot_version,
                              'upload_date': formatted_date + ' ' + time_formatted,
                              'number_of_rows': value['number_of_rows'],
                              'received_channel': value['received_channel'],
                              'energy_pattern_val': value['energy_pattern_val'],
                              'time_profile_val': value['time_profile_val']}

    @staticmethod
    def update_run_data_file(run_data_path, run_data_dict, run_end_time, tags_num, advas, result):
        """
        Updates the run_data CSV file while running the program
        """
        run_data_dict['run_end_time'] = run_end_time
        run_data_dict['total_run_tested'] = tags_num
        run_data_dict['total_run_responding_tags'] = advas
        run_data_dict['yield'] = result
        dict_to_csv(dict_in=run_data_dict, path=run_data_path)

    def update_packet_data(self):
        """
        Updates the run_data CSV file while running the program
        """
        packets_queue = self.adva_process.get_packets_queue()
        if not packets_queue.empty():
            cur_p = PacketList()
            for _ in range(packets_queue.qsize()):
                cur_p.__add__(packets_queue.get())
            cur_p_df = cur_p.get_df()
            cur_p_df = cur_p_df.drop_duplicates(subset=['adv_address'])
            cur_p_df = cur_p_df.loc[~cur_p_df['adv_address'].isin(list(self.seen_advas))]

            for i in cur_p_df['adv_address']:
                self.seen_advas.add(i)
            if not self.update_packet_data_flag:
                # Initializing the packets_data file
                try:
                    cur_p_df.insert(loc=len(cur_p_df.columns), column='common_run_name', value=self.cmn)
                    self.final_path_packets_data = os.path.join(self.folder_path, self.cmn + '@packets_data.csv')
                    if "index" in cur_p_df:
                        cur_p_df.drop("index", axis=1, inplace=True)
                    cur_p_df.to_csv(self.final_path_packets_data, index=False)
                    self.update_packet_data_flag = True
                except Exception as e:
                    print(e)
            else:
                # updating packets_data_file
                cur_p_df.insert(loc=len(cur_p_df.columns), column='common_run_name', value=self.cmn)
                cur_p_df.to_csv(self.final_path_packets_data, mode='a', index=False, header=False)

    def stop_button(self, window, run_end_time, tags_num, advas, result):
        """
        Finishing the program and saves the last changes after pressing Stop in the second window
        """
        self.stop.set()
        window.close()
        plt.close()
        self.adva_process_thread.join()
        self.count_process_thread.join()

        self.update_run_data_file(self.final_path_run_data, self.run_data_dict,
                                  formatted_date + ' ' + run_end_time,
                                  tags_num, advas, result)
        self.update_packet_data()

        if self.upload_flag:
            try:
                is_uploaded = upload_to_cloud_api(self.cmn, self.tester_type,
                                                  run_data_csv_name=self.final_path_run_data,
                                                  packets_data_csv_name=self.final_path_packets_data,
                                                  env='test', is_path=True)
                if is_uploaded:
                    print("Successful upload")
                else:
                    print("Unsuccessful upload")
            except Exception as e:
                print(e)

    def init_processes(self, rec_channel, time_pro, energy_pat, inlay_select):
        """
        Initializing the two main instances and threads in order to start working
        """
        self.adva_process = AdvaProcess(self.stop, rec_channel, time_pro, energy_pat,
                                        inlay_select)
        self.adva_process_thread = threading.Thread(target=self.adva_process.run, args=())
        self.count_process = CountThread(self.stop, self.rows_number)
        self.count_process_thread = threading.Thread(target=self.count_process.run, args=())

    def start_processes(self):
        """
        Starting the work of the both threads
        """
        self.adva_process_thread.start()
        self.count_process_thread.start()

    def overlay_window(self):
        """
        The small window open session
        """

        yes_or_no = ['Yes', 'No']
        layout = [
            [sg.Text('Number of tags:', font=4), sg.Text(key='num_rows', font=4)],
            [sg.Text('Number of advas:', font=4), sg.Text(key='num_advas', font=4)],
            [sg.Text('Do you want to stop or upload?')],
            [sg.Button('Stop'), [sg.Text('Upload:', font=6)],
             [sg.Combo(values=yes_or_no, default_value=yes_or_no[0], key='upload', font=4, enable_events=True)]],
            [sg.Canvas(key='-CANVAS-', size=(10, 100))],
        ]

        sub = False
        window = sg.Window('Upload CSV files', layout, modal=True, finalize=True, location=(870, 200))

        # initialize num_advas and num_rows
        num_rows_text_elem = window['num_rows']
        num_advas_text_elem = window['num_advas']
        num_rows = (self.rows_number * self.neg_col)
        num_advas = self.adva_process.get_unq_advas()
        num_rows_text_elem.update(f"{num_rows}")
        num_advas_text_elem.update(f"{num_advas}")
        # initialize the graph
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['red'])
        fig, ax = plt.subplots()
        ax.set_xlabel('Number of tags')
        ax.set_ylabel('Yield %')
        ax.set_ylim([-2, 112])
        plt.ion()
        plt.show()
        prev_tests = 0
        prev_val = 0
        text_box = ax.text(0.68, 1.05, f"Yield: {prev_val:.2f} %", transform=ax.transAxes)

        while True:
            event, values = window.read(timeout=100)

            new_num_rows = self.count_process.get_tested() + (self.rows_number * self.neg_col)
            new_num_advas = self.adva_process.get_unq_advas()
            # updating number of rows
            if new_num_rows != num_rows:
                num_rows = new_num_rows
                num_rows_text_elem.update(f"{num_rows}")
            # updating number of advas
            if new_num_advas != num_advas:
                num_advas = new_num_advas
                num_advas_text_elem.update(f"{num_advas}")
            # updating the graph
            curr_tests = new_num_rows
            curr_val = self.get_result()
            plt.pause(0.01)
            if curr_val > 100:
                curr_val = 110
            ax.plot([prev_tests, curr_tests], [prev_val, curr_val], color='red')
            prev_tests = curr_tests
            prev_val = curr_val
            text_box.set_text(f"Yield : {curr_val:.2f} %")
            # updating run_data_file
            end_time = datetime.datetime.now()
            run_end_time = end_time.strftime("%I:%M:%S")
            advas = self.adva_process.get_unq_advas()
            tags_num = self.count_process.get_tested()
            result = self.get_result()
            self.update_run_data_file(self.final_path_run_data, self.run_data_dict, formatted_date + ' ' + run_end_time,
                                      tags_num, advas, result)
            self.update_packet_data()

            if event == sg.WIN_CLOSED or event in ('Stop', 'upload'):
                if event == 'upload':
                    if values['upload'] == 'No':
                        self.upload_flag = False
                    else:
                        self.upload_flag = True  # if we press No then yes
                if event == 'Stop':
                    self.stop_button(window, run_end_time, tags_num, advas, result)
                    sub = True
                    break
                if sub:
                    break

        return sub

    def open_session(self):
        """
        opening a session for the process
        """
        # save data to configs file
        if os.path.exists("configs/gui_input_do_not_delete.json"):
            with open("configs/gui_input_do_not_delete.json", "r") as f:
                previous_input = json.load(f)

        else:
            previous_input = {'inlay': '', 'number': '', 'number_of_rows': '', 'received_channel': '',
                              'energy_pattern_val': '', 'time_profile_val': '', 'tester_station_name': '',
                              'comments': '', 'operator': '', 'wafer_lot': '', 'wafer_num': ''}
        # update fields from configs
        selected_inlay = csv_dictionary[previous_input['inlay']]
        self.rows_number = selected_inlay['number_of_rows']
        energy_pat = selected_inlay['energy_pattern_val']
        time_pro = selected_inlay['time_profile_val']
        rec_channel = selected_inlay['received_channel']
        lst_inlay_options = list(inlay_types_dict.keys())


        layout = [

            [sg.Text('Wafer Lot:', font=4)],
            [sg.InputText(previous_input['wafer_lot'], key='wafer_lot', font=4)],

            [sg.Text('Wafer Number:', font=4)],
            [sg.InputText(previous_input['wafer_num'], key='wafer_num', font=4)],

            [sg.Text('Number of neglected columns:', font=4)],
            [sg.InputText(key='neg_col', font=4)],

            [sg.Text('Inlay:', font=4)],
            [sg.Combo(values=lst_inlay_options, default_value=previous_input['inlay'], key='inlay', font=4,
                      enable_events=True)],

            [
                sg.Column([[sg.Text('Energy Pattern:', font=4),
                            sg.Text(energy_pat, key='energy_pattern_val', font=4)]]),
                sg.Column([[sg.Text('Time Profile:', font=4),
                            sg.Text(time_pro, key='time_profile_val', font=4)]]),
                sg.Column([[sg.Text('Number of rows:', font=4), sg.Text(self.rows_number, key='rows', font=4)]]),
                sg.Column([[sg.Text('Received Channel:', font=4),
                            sg.Text(rec_channel, key='received_channel', font=4)]])],

            [sg.Text('Tester Station Name:', font=4)],
            [sg.InputText(previous_input['tester_station_name'], key='tester_station_name', font=4)],
            [sg.Text('Comments:', font=4)],
            [sg.InputText(previous_input['comments'], key='comments', font=4)],

            [sg.Text('Operator:', font=4)],
            [sg.InputText(previous_input['operator'], key='operator', font=4)],

            [sg.Submit()]]

        window = sg.Window('WILIOT Yield Tester', layout, finalize=True)

        inlay_select = ''
        while True:
            event, values = window.read(timeout=100)
            inlay_select = values['inlay']
            self.selected = values['inlay']
            if event == 'inlay':
                inlay_select = values['inlay']
                self.selected = values['inlay']

                if inlay_select in csv_dictionary:
                    selected_inlay = csv_dictionary[inlay_select]
                    self.rows_number = selected_inlay['number_of_rows']
                    energy_pat = selected_inlay['energy_pattern_val']
                    time_pro = selected_inlay['time_profile_val']
                    rec_channel = selected_inlay['received_channel']

                else:
                    self.rows_number = 'Invalid Selection'
                    energy_pat = 'Invalid Selection'
                    time_pro = 'Invalid Selection'
                    rec_channel = 'Invalid Selection'

                window.find_element('rows').Update(value=self.rows_number)
                window.find_element('energy_pattern_val').Update(value=energy_pat)
                window.find_element('time_profile_val').Update(value=time_pro)
                window.find_element('received_channel').Update(value=rec_channel)
            if event == 'Submit':  # Button clicked
                if (values['neg_col']) == '':
                    self.neg_col = 0
                else:
                    self.neg_col = int(values['neg_col'])
                self.wafer_lot = values['wafer_lot']
                self.wafer_number = values['wafer_num']
                self.comments = values['comments']
                self.tester_station_name = values['tester_station_name']
                self.operator = values['operator']

                self.init_processes(rec_channel, time_pro, energy_pat, inlay_select)
                self.init_run_data()
                self.start_processes()

                with open("configs/gui_input_do_not_delete.json", "w") as f:
                    json.dump(values, f)
                break
            elif event == sg.WIN_CLOSED:
                exit()

        window.close()


if __name__ == '__main__':
    m = MainWindow()
    m.run()
