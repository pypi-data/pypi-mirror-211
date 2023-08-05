import builtins
import sys
import types
from inspect import getmembers, isbuiltin

from je_auto_control.utils.exception.exception_tags import action_is_null_error, add_command_exception_tag, \
    executor_list_error
from je_auto_control.utils.exception.exception_tags import cant_execute_action_error
from je_auto_control.utils.exception.exceptions import AutoControlActionException, AutoControlAddCommandException
from je_auto_control.utils.exception.exceptions import AutoControlActionNullException
from je_auto_control.utils.generate_report.generate_html_report import generate_html
from je_auto_control.utils.generate_report.generate_html_report import generate_html_report
from je_auto_control.utils.generate_report.generate_json_report import generate_json
from je_auto_control.utils.generate_report.generate_json_report import generate_json_report
from je_auto_control.utils.generate_report.generate_xml_report import generate_xml
from je_auto_control.utils.generate_report.generate_xml_report import generate_xml_report
from je_auto_control.utils.json.json_file import read_action_json
from je_auto_control.utils.package_manager.package_manager_class import package_manager
from je_auto_control.utils.project.create_project_structure import create_project_dir
from je_auto_control.utils.shell_process.shell_exec import ShellManager
from je_auto_control.utils.start_exe.start_another_process import start_exe
from je_auto_control.utils.test_record.record_test_class import record_action_to_list, test_record_instance
from je_auto_control.wrapper.auto_control_image import locate_all_image, locate_and_click, locate_image_center
from je_auto_control.wrapper.auto_control_keyboard import check_key_is_press
from je_auto_control.wrapper.auto_control_keyboard import get_special_table, get_keyboard_keys_table
from je_auto_control.wrapper.auto_control_keyboard import press_keyboard_key, release_keyboard_key, hotkey, \
    type_keyboard, write
from je_auto_control.wrapper.auto_control_mouse import get_mouse_position, press_mouse, release_mouse, click_mouse, \
    mouse_scroll
from je_auto_control.wrapper.auto_control_mouse import get_mouse_table
from je_auto_control.wrapper.auto_control_mouse import set_mouse_position
from je_auto_control.wrapper.auto_control_record import record, stop_record
from je_auto_control.wrapper.auto_control_screen import screenshot, screen_size


class Executor(object):

    def __init__(self):
        self.event_dict: dict = {
            # mouse
            "mouse_left": click_mouse,
            "mouse_right": click_mouse,
            "mouse_middle": click_mouse,
            "click_mouse": click_mouse,
            "get_mouse_table": get_mouse_table,
            "get_mouse_position": get_mouse_position,
            "press_mouse": press_mouse,
            "release_mouse": release_mouse,
            "mouse_scroll": mouse_scroll,
            "set_mouse_position": set_mouse_position,
            "get_special_table": get_special_table,
            # keyboard
            "get_keyboard_keys_table": get_keyboard_keys_table,
            "type_keyboard": type_keyboard,
            "press_keyboard_key": press_keyboard_key,
            "release_keyboard_key": release_keyboard_key,
            "check_key_is_press": check_key_is_press,
            "write": write,
            "hotkey": hotkey,
            # image
            "locate_all_image": locate_all_image,
            "locate_image_center": locate_image_center,
            "locate_and_click": locate_and_click,
            # screen
            "screen_size": screen_size,
            "screenshot": screenshot,
            # test record
            "set_record_enable": test_record_instance.set_record_enable,
            # only generate
            "generate_html": generate_html,
            "generate_json": generate_json,
            "generate_xml": generate_xml,
            # generate report
            "generate_html_report": generate_html_report,
            "generate_json_report": generate_json_report,
            "generate_xml_report": generate_xml_report,
            # record
            "record": record,
            "stop_record": stop_record,
            # execute
            "execute_action": self.execute_action,
            "execute_files": self.execute_files,
            "add_package_to_executor": package_manager.add_package_to_executor,
            "add_package_to_callback_executor": package_manager.add_package_to_callback_executor,
            # project
            "create_project": create_project_dir,
            # Shell
            "shell_command": ShellManager().exec_shell,
            # Another process
            "execute_process": start_exe,
        }
        # get all builtin function and add to event dict
        for function in getmembers(builtins, isbuiltin):
            self.event_dict.update({str(function[0]): function[1]})

    def _execute_event(self, action: list):
        event = self.event_dict.get(action[0])
        if len(action) == 2:
            if isinstance(action[1], dict):
                return event(**action[1])
            else:
                return event(*action[1])
        elif len(action) == 1:
            return event()
        else:
            raise AutoControlActionException(cant_execute_action_error + " " + str(action))

    def execute_action(self, action_list: [list, dict]) -> dict:
        """
        use to execute all action on action list(action file or program list)
        :param action_list the list include action
        for loop the list and execute action
        """
        if isinstance(action_list, dict):
            action_list: list = action_list.get("auto_control", None)
            if action_list is None:
                raise AutoControlActionNullException(executor_list_error)
        execute_record_dict = dict()
        try:
            if len(action_list) > 0 or isinstance(action_list, list):
                pass
            else:
                raise AutoControlActionNullException(action_is_null_error)
        except Exception as error:
            record_action_to_list("execute_action", action_list, repr(error))
            print(repr(error), file=sys.stderr, flush=True)
        for action in action_list:
            try:
                event_response = self._execute_event(action)
                execute_record = "execute: " + str(action)
                execute_record_dict.update({execute_record: event_response})
            except Exception as error:
                print(repr(error), file=sys.stderr, flush=True)
                print(action, file=sys.stderr, flush=True)
                record_action_to_list("execute_action", None, repr(error))
                execute_record = "execute: " + str(action)
                execute_record_dict.update({execute_record: repr(error)})
        for key, value in execute_record_dict.items():
            print(key, flush=True)
            print(value, flush=True)
        return execute_record_dict

    def execute_files(self, execute_files_list: list) -> list:
        """
        :param execute_files_list: list include execute files path
        :return: every execute detail as list
        """
        execute_detail_list: list = list()
        for file in execute_files_list:
            execute_detail_list.append(self.execute_action(read_action_json(file)))
        return execute_detail_list


executor = Executor()
package_manager.executor = executor


def add_command_to_executor(command_dict: dict):
    """
    :param command_dict: dict include command we want to add to event_dict
    """
    for command_name, command in command_dict.items():
        if isinstance(command, (types.MethodType, types.FunctionType)):
            executor.event_dict.update({command_name: command})
        else:
            raise AutoControlAddCommandException(add_command_exception_tag)


def execute_action(action_list: list) -> dict:
    return executor.execute_action(action_list)


def execute_files(execute_files_list: list) -> list:
    return executor.execute_files(execute_files_list)
