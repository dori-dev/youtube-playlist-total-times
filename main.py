"""Times of playlist in youtube
"""

from typing import List
from bs4 import BeautifulSoup
from selenium import webdriver


class PlaylistTimes:
    """Extract playlist times and calculate it hours, and show this information
    """

    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_argument('--user-data-dir=./YouTube')
        self.youtube = webdriver.Chrome(
            executable_path="./chromedriver", chrome_options=option)
        self.times = []
        self.minute_times = []
        self.length = 0
        self.hours = 0

    def playlist_times(self, url: str) -> None:
        """Main function, manage all variable and function to show information

        Args:
            url (str): Link address of playlist in youtube
        """
        self.youtube.get(url)
        # wait for setup page
        input('To Start Calculate Total Time Press Enter...')

        source = self.youtube.page_source  # get source of url
        self.extract_all_times(source)
        self.length = len(self.times)

        self.calculate_minutes_times(self.times)
        self.calculate_hours(self.minute_times)

        self.show_information()

    def extract_all_times(self, source: str) -> List[str]:
        """Extract all times in playlist page source

        Args:
            source (str): Source of playlist page

        Returns:
            list[str]: List of string format like this xx:xx:xx
        """
        soup = BeautifulSoup(source, 'html.parser')

        # find all this tags for get all times
        times = soup.findAll('ytd-thumbnail-overlay-time-status-renderer')
        # get all time text and remove \n from first and end of text
        self.times = [time.text.strip() for time in times]

    def calculate_minutes_times(self, times: List[str]) -> List[int]:
        """Calculate minutes times with list of str format of minutes

        Args:
            times (list[str]): List of string format like this xx:xx:xx

        Returns:
            list[int]: List of total of hours and minutes in times
        """
        minute_times = []

        for time in times:
            # split time format with : and convert to integer
            split_time = [int(num) for num in time.split(':')]
            # any time fromat => 0:45 | 5:06:23 | 8:09
            # if length of split_time equal 2 means not have and hours
            # for write little code we insert 0 to first of split_time list
            if len(split_time) == 2:
                split_time.insert(0, 0)
            # unpack split_time to 3 variable
            hours, minute, second = split_time
            # round the second
            if second < 30:
                # if second smaller than 30, just add minute and hours*60(for minute)
                minute_times.append(minute+(hours*60))
            else:
                # if second biggest than 30, add minute+1 and hours*60(for minute)
                minute_times.append(minute+1+(hours*60))

        self.minute_times = minute_times

    def calculate_hours(self, minute_times: List[int]) -> int:
        """Calculate hours times with list of minute times

        Args:
            minute_times (list[int]): List of any minute

        Returns:
            int: Hours
        """
        total = sum(minute_times)

        # round hours of total minute time
        if total % 60 < 20:
            # if extra minutes smallest than 20 minute just calculate hours
            self.hours = total // 60
        else:
            # if extra minutes biggest than 20 minute calculate hours + 1
            self.hours = total // 60 + 1

    def show_information(self) -> None:
        """Show playlist information
        """
        print(f'Playlist haves {self.length} videos')
        print(f'Total times is {self.hours} hours')
        print(f"\n{'-'*30}\n")


youtube = PlaylistTimes()
input_url = input('Playlist Link: ')
while input_url != 'done':
    youtube.playlist_times(input_url)
    input_url = input('Playlist Link: ')
