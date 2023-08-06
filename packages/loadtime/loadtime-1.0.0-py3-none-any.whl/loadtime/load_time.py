import time
import threading
from datetime import timedelta
import os
import json


class LoadTime:
    def __init__(self, name="", message=None, pbar=True, dirname="loadtime", hf=False, fn=None, fn_print=None):
        """
        Initialize the LoadTime class

        :param name: Name of the long-term process. For loading HuggingFace models, specify the model name.
        :param message: Specify the message to be displayed. If omitted, the default message is used.
        :param pbar: Set to True to display the progress bar and percentage.
        :param dirname: Directory name for cache storage.
        :param hf: Set to True to use for time display for loading HuggingFace models. If the model data has not yet been downloaded to the disk, HuggingFace's loader displays the download progress, so this library does not display it.
        :param fn: Function to execute the long-term process.
        :param fn_print: Function to perform the display. If omitted, it will be output to the console.
        """
        self.name = name
        self.message = message
        self.start_time = None
        self.thread = None
        self.stop_event = threading.Event()  # Event to signal the thread to stop
        self.fn = fn
        self.dirname = dirname
        self.show_percentage = pbar
        self._load_data()  # Load cached data if exists
        self.last_message = None
        self.elapsed_time = -1
        self.fn_print = None
        self.hf = hf

        # If a print function is provided, use it, else print to the console
        if fn_print is not None:
            self.fn_print = fn_print
        else:
            def console_print_func(str):
                print(f'{str}', end='', flush=True)

            self.fn_print = console_print_func

        # If this is for a HuggingFace model and the model is not cached yet, suppress the output
        if self.hf is True and self.is_model_cached(self.name) is False:
            self.fn_print = None

        if self.fn is None:
            raise TypeError('fn not set')

    def clear_stored_data(self):
        """Clears stored time data from previous runs"""
        self._load_data()
        self.stored_data["total_time"] = None
        self.save_dict_to_json(self.stored_data)

    def _load_data(self):
        """Load stored data from previous runs, or initialize a new storage if none exists"""
        stored_data = self.load_dict_from_json()
        if stored_data is None:
            stored_data = {"total_time": None}

        self.save_dict_to_json(stored_data)
        self.stored_data = stored_data

    def _get_formatted_time(self, elapsed_time):
        """
        Formats time in seconds into the HH:MM:SS format.
        """
        formatted_time = str(timedelta(seconds=int(elapsed_time)))
        if elapsed_time < 3600:
            formatted_time = formatted_time[2:]  # mm:ss format

        return formatted_time

    def is_model_cached(self, model_path):
        """
        Check if a model is cached in the local directory.

        Args:
            model_path (str): The path of the model. The format should be 'organization/model-name-version'.

        Returns:
            bool: True if the model is cached locally, False otherwise.
        """
        # Convert the model path
        model_path = "models--" + model_path.replace("/", "--")

        # Build the full path
        home_dir = os.path.expanduser("~")
        full_path = os.path.join(home_dir, ".cache", "huggingface", "hub", model_path)

        # Check if the directory exists and if it contains any files
        if os.path.isdir(full_path) and os.listdir(full_path):
            return True
        else:
            return False

    def _display_time(self):
        """
        Runs in a separate thread to display the elapsed time, estimated total time, and progress bar if enabled.
        """
        while not self.stop_event.is_set():
            self.elapsed_time = time.time() - self.start_time
            formatted_time = self._get_formatted_time(self.elapsed_time)
            total_time_disp = f"{formatted_time}"
            total_time_in_sec = self.stored_data.get('total_time', None)

            progress_disp = ""

            if total_time_in_sec is not None and int(total_time_in_sec) != 0:
                total_time_disp = f"{formatted_time}/{self._get_formatted_time(total_time_in_sec)}"

                if self.show_percentage:
                    percentage = (self.elapsed_time / total_time_in_sec)
                    if percentage > 1:
                        percentage = 1

                    progress_disp = self._create_percentage_disp(percentage)

            if self.message is not None:
                self.last_message = f'\r{self.message}{total_time_disp}'
            else:
                self.last_message = f'\rLoading "{self.name}" ... {total_time_disp}'

            self.fn_print(f'\r{self.last_message}{progress_disp}')

            time.sleep(0.5)  # update every 0.5 seconds

    def _create_percentage_disp(self, percentage):
        """
        Creates a progress bar display string with the given completion percentage.
        """
        if not self.show_percentage:
            return ""

        bar_length = 20
        block = '█'  # Unicode full block
        blocks_len = int(round(bar_length * percentage))
        space_len = bar_length - blocks_len
        progress = block * blocks_len + ' ' * space_len

        if percentage > 1:
            percentage = 1
        percentage_disp = f" ({int(percentage * 100)}%)"

        progress_disp = f" [{progress}]{percentage_disp}"
        return progress_disp

    def __call__(self):
        """
        Allows the object to be callable, starting the time tracking and function execution when called.
        """
        return self.start()

    def start(self):
        """
        Starts the timer and the execution of the function, displaying the time tracking.
        """
        ret = None
        if self.thread is None:
            self.start_time = time.time()
            self.thread = threading.Thread(target=self._display_time)
            self.thread.start()
            ret = self.fn()
            self.fn = None
            self._stop()
        return ret

    def _stop(self):
        """
        Stops the timer and the thread, saves the elapsed time for future reference.
        """
        if self.thread is not None:
            if self.stored_data.get("total_time", None) is not None:
                self.fn_print(f'\r{self.last_message}{self._create_percentage_disp(1)}\n')
            else:
                self.fn_print(f'\r{self.last_message}\n')

            self.stop_event.set()
            self.thread.join()
            self.thread = None
            self.stop_event.clear()
            self.stored_data["total_time"] = self.elapsed_time
            self.save_dict_to_json(self.stored_data)
        return self

    def save_dict_to_json(self, data_dict):
        """
        Save a dictionary of data to a json file, named after the operation

        """

        try:
            filename = self.name.replace("\\", "_").replace("/", "_") + ".json"

            home_dir = os.path.expanduser("~")
            cache_dir = os.path.join(home_dir, ".cache", "loadtime")
            os.makedirs(cache_dir, exist_ok=True)
            file_path = os.path.join(cache_dir, filename)

            with open(file_path, 'w') as f:
                json.dump(data_dict, f)
        finally:
            pass


    def load_dict_from_json(self):
        """
        Load a dictionary of data from a json file, named after the operation.
        """
        filename = self.name.replace("\\", "_").replace("/", "_") + ".json"
        home_dir = os.path.expanduser("~")
        cache_dir = os.path.join(home_dir, ".cache", "loadtime")
        file_path = os.path.join(cache_dir, filename)

        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r') as f:
            data_dict = json.load(f)

        return data_dict
