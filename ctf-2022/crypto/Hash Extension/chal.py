import random
import string
import struct
import hashlib

FLAG_FILE = "flag.txt"


class Chal():
    def handle(self):
        self.flag = self.get_flag()
        salt = ''.join(random.choices(string.printable, k=8))

        self.send("WELCOME TO HASH MACHINE!\n")
        self.send("Your task is to guess the result of my hash function.\n")
        self.send(f"Flag length: {len(self.flag)}\n")
        self.send(f"Salt: {salt}\n")
        username = self.receive("Tell me your name:\n").decode()
        if (5 <= len(username) <= 15):
            message_1 = ''.join((username, ":", self.flag)).encode()
            print(f"Message 1: {message_1}")
            self.send(
                f"Message 1 hexdigest: {hashlib.sha256(message_1).hexdigest()}\n")

            message_2 = self._pad_message(message_1) + salt.encode()
            print(f"Message 2: {message_2}")
            print(f"Message 2 padd: {self._pad_message(message_2)}")
            user_input = self.receive(
                "Send hexdigest of message 2.\n").decode()
            if (user_input == hashlib.sha256(message_2).hexdigest()):
                self.send(
                    "Genius! You can know the message 2 hexdigest even if you don't know the flag.\n")
                self.send("Here is your flag.\n")
                self.send(self.flag + "\n")
            else:
                self.send("Sorry, you failed.\n")
                print(user_input, hashlib.sha256(message_2).hexdigest())
        else:
            self.send("Choose a username 5–15 characters long!\n")

    def _pad_message(self, message):
        # https://www.rfc-editor.org/rfc/rfc4634#page-6
        return b''.join((message, b'\x80', b'\x00' * (55 - len(message)), struct.pack('>LL', 8*len(message) >> 32, 8*len(message) & 0xffffffff)))

    def get_flag(self):
        with open(FLAG_FILE) as f:
            return f.readline()

    def send(self, string: str):
        print(string, end='')

    def receive(self, prompt):
        self.send(prompt)
        return input().strip().encode()


p = Chal()
p.handle()
