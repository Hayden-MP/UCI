import unittest
import ds_protocol as dsp
import json
from Profile import Profile

#from ds_messenger import DirectMessage, DirectMessenger


class Testing(unittest.TestCase):

    def test_get_joinmsg(self):
        self.assertEqual(dsp.get_joinmsg(username="Smith", password="beeswax@000"),
        '{"join": {"username": "Smith","password": "beeswax@000","token":""}}',
        "get_joinmsg test failed")
        
        self.assertEqual(dsp.get_joinmsg(username="Tony", password="HansZimmerman"),
        '{"join": {"username": "Tony","password": "HansZimmerman","token":""}}',
        "get_joinmsg test failed")
        
    def test_get_rtrmsg(self):
        self.assertEqual(dsp.get_rtrmsg(token="1111", taip="new"),'{"token":"1111", "directmessage": "new"}',
                         "get_rtrmsg test failed")
        
    def test_load_srvmsg(self):
        json_obj=json.dumps({"response": {"type": "ok", "message": "Direct message sent"}})
        self.assertEqual(dsp.load_srvmsg(json_obj),{"response": {"type": "ok", "message": "Direct message sent"}},
                         "load_srvmsg test failed")
        
    def test_get_token(self):
         dic={'response': {'type': 'ok', 'message': 'Welcome back, Hayden',
                                           'token': '2898c1e2-40c7-4de8-889e-430655d53a4c'}}
         self.assertEqual(dsp.get_token(dic),"2898c1e2-40c7-4de8-889e-430655d53a4c",
                         "get_token test failed")
         
    def test_get_responseType(self):
        dic={'response': {'type': 'ok', 'message': 'Welcome to the ICS 32 Distributed Social!',
                          'token': '715ec892-55ba-41ae-ad51-a074608625e8'}}
        self.assertEqual(dsp.get_responseType(dic),"ok","get_responsetyoe test failed")

        dic={'response': {'type': 'unknown', 'message': 'Welcome to the ICS 32 Distributed Social!',
                          'token': '715ec892-55ba-41ae-ad51-a074608625e8'}}
        self.assertFalse(dsp.get_responseType(dic)=="ok","get_responsetyoe test failed")
                
        
if __name__ == '__main__':
    unittest.main()


#profile=Profile(dsuserver="168.235.86.101", username="King2020", password="0000")
#dm_kenzo=DirectMessenger(dsuserver="168.235.86.101", username="King2020", password="0000", port=3021)
#print(dm_kenzo.send(message="HI", recipient="Tom"))
dic={'response': {'type': 'ok', 'message': 'Welcome to the ICS 32 Distributed Social!',
                          'token': '715ec892-55ba-41ae-ad51-a074608625e8'}}
print(dsp.print_rMessage(dic))
"""
def test_print_rMessage(self):
        dic={'response': {'type': 'ok', 'message': 'Welcome to the ICS 32 Distributed Social!',
                          'token': '715ec892-55ba-41ae-ad51-a074608625e8'}}
        self.assertEqual(dsp.print_rMessage,"Welcome to the ICS 32 Distributed Social!","print_rMessage test failed")
        
        dic={'response': {'type': 'ok', 'message': 'Welcome back, Hayden',
                                           'token': '2898c1e2-40c7-4de8-889e-430655d53a4c'}}
        self.assertEqual(dsp.print_rMessage,"Welcome back, Hayden","print_rMessage test failed")

        dic={"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp": "1603167689.3928561"},
                                                     {"message":"Bzzzzz", "from":"thebeemoviescript","timestamp":"1603167689.3928561"}]}}
        self.assertEqual(dsp.print_rMessage,"Messages Successfully Retrieved.","print_rMessage test failed")
"""
