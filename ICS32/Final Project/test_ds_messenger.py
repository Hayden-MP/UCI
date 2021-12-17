import unittest
import socket
from ds_messenger import DirectMessenger


class Testing(unittest.TestCase):

    def test_send(self):
        messenger = DirectMessenger(username="testingcaseuser", password="pwd")
        self.assertEqual(True, messenger.send("message", "ohhimark"),"send method test failed")

    def test_retrieve_new(self):
        messenger = DirectMessenger(username="testingcaseuser", password="pwd")
        self.assertEqual([], messenger.retrieve_new(),"retrieve_new method test failed")

    def test_retrieve_all(self):
        messenger = DirectMessenger(username="testingcaseuser", password="pwd")
        self.assertEqual([], messenger.retrieve_all(), "retrive_all method test failed")

    def test__communicate_w_server(self):
        messenger = DirectMessenger(username="testingcaseuser", password="pwd")
        self.assertEqual(messenger._communicate_w_server(server="168.235.86.101", port=3021, taip="send", message="Hi!",
                              recipient="Tom"),{'response': {'type': 'ok', 'message': 'Direct message sent'}},
                         "_communicate_w_server test failed")
        
    def test_send_to_server(self):
        #attempting to run with unknown user
        messenger = DirectMessenger(username="Bobby", password="1234")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(("168.235.86.101",3021))
                joinresponse = messenger._send_to_server(client=client, username="Bobby", password="1234", typ="join")
                self.assertEqual(joinresponse,{'response': {'type': 'error', 'message': 'Invalid password or username already taken'}})

        #attempting to run with known user
        messenger = DirectMessenger(username="Hayden", password="0000")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.connect(("168.235.86.101",3021))
                joinresponse = messenger._send_to_server(client=client, username="Hayden", password="0000", typ="join")
                self.assertEqual(joinresponse,{'response': {'type': 'ok', 'message': 'Welcome back, Hayden',
                                                            'token': '2898c1e2-40c7-4de8-889e-430655d53a4c'}})
    

if __name__ == '__main__': 
    unittest.main()
