from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import os

class LinkBrowser:
    def __init__(self, input_file, output_file, save_spot_file):
        self.driver = webdriver.Chrome()
        with open(input_file, 'r') as f:
            self.links = [link.strip() for link in f.readlines()]
        self.current_link_index = 0
        self.output_file = output_file
        self.saved_links = []
        self.save_spot_file = save_spot_file

        # Load saved spot
        if os.path.isfile(self.save_spot_file):
            with open(self.save_spot_file, 'r') as f:
                saved_spot = f.readline().strip()
                if saved_spot in self.links:
                    self.current_link_index = self.links.index(saved_spot)

    def add_link(self):
        link = self.driver.current_url
        #if file doesn't exist, create it
        if not os.path.isfile(self.output_file):
            with open(self.output_file, 'w') as f:
                f.write('')
        self.saved_links.append(link)
        with open(self.output_file, 'a') as f:
            f.write(link + '\n')
        print(f"Link {link} added to the list")

    def remove_link(self):
        link = self.driver.current_url
        if link in self.links:
            self.links.remove(link)
            print(f"Link {link} removed from the list")
        else:
            print("This link is not in the list")

    def save_spot(self):
        link = self.driver.current_url
        #if file doesn't exist, create it
        if not os.path.isfile(self.save_spot_file):
            with open(self.save_spot_file, 'w') as f:
                f.write('')
        with open(self.save_spot_file, 'w') as f:
            f.write(link + '\n')
        print(f"Current spot saved at {link}")

    def go_to_next_link(self):
        if self.current_link_index < len(self.links) - 1:
            self.current_link_index += 1
            self.driver.get(self.links[self.current_link_index])
        else:
            print("This is the last link in the list")

    def go_to_previous_link(self):
        if self.current_link_index > 0:
            self.current_link_index -= 1
            self.driver.get(self.links[self.current_link_index])
        else:
            print("This is the first link in the list")

    def navigate_links(self):
        self.driver.get(self.links[self.current_link_index])

        while True:
            print("Press Enter for next link, 'a' to add the current link to list, 'b' to go back, 'q' to quit, 'r' to remove link from list, 's' to save current spot")
            command = input()

            if command == '':
                self.go_to_next_link()
            elif command.lower() == 'a':
                self.add_link()
            elif command.lower() == 'b':
                self.go_to_previous_link()
            elif command.lower() == 'q':
                break
            elif command.lower() == 'r':
                self.remove_link()
            elif command.lower() == 's':
                self.save_spot()
            else:
                print("Invalid command")

        self.driver.quit()

if __name__ == "__main__":
    browser = LinkBrowser('links.txt', 'saved_links.txt', 'save_spot.txt')
    browser.navigate_links()
