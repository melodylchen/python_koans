#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Create a Proxy Class
#
# In this assignment, create a proxy class (one is started for you
# below).  You should be able to initialize the proxy object with any
# object.  Any attributes called on the proxy object should be forwarded
# to the target object.  As each attribute call is sent, the proxy should
# record the name of the attribute sent.
#
# The proxy class is started for you.  You will need to add a method
# missing handler and any other supporting methods.  The specification
# of the Proxy class is given in the AboutProxyObjectProject koan.

# Note: This is a bit trickier than its Ruby Koans counterpart, but you
# can do it!

from runner.koan import *

class Proxy:
    def __init__(self, target_object):
        # WRITE CODE HERE
        self._messages = []
        
        #initialize '_obj' attribute last. Trust me on this!
        self._obj = target_object


    def __getattr__(self, attr_name):
        # Handles functions that are not in the Proxy class

        attr = getattr(self._obj, attr_name) #performs functions for the Parent class functions
        self._messages.append(attr_name) #appends parent function name to messages
        return attr  

        """

        Greg Malcolm's Solution: https://github.com/gregmalcolm/python_koans/blob/answers/python3/koans/about_proxy_object_project.py


        Also refer to: https://stackoverflow.com/questions/8554453/python-koans-class-proxy
        """       

    def __setattr__(self, attr_name, value):
        #returns the ability to set attributes if not in the parent class

        if "_" == attr_name[0]: #Performs set functions  for the Proxy class
            return object.__setattr__(self, attr_name, value)
        
    
        setattr(self._obj, attr_name, value) #Performs set functions for the Parent Class


        self._messages.append(attr_name) #Appends the function name to the messages

        """
        Greg Malcolm's Solution: https://github.com/gregmalcolm/python_koans/blob/answers/python3/koans/about_proxy_object_project.py

        
        """

    def messages(self):
        return self._messages

    def was_called(self, fn_name):
        if fn_name in self._messages:
            return True
        else:
            return False
    
    def number_of_times_called(self, fn_name):
        return self._messages.count(fn_name)
        

   

# The proxy object should pass the following Koan:
#
class AboutProxyObjectProject(Koan):
    def test_proxy_method_returns_wrapped_object(self):
        # NOTE: The Television class is defined below
        tv = Proxy(Television())

        self.assertTrue(isinstance(tv, Proxy))

    def test_tv_methods_still_perform_their_function(self):
        tv = Proxy(Television())

        tv.channel = 10
        tv.power()

        self.assertEqual(10, tv.channel)
        self.assertTrue(tv.is_on())

    def test_proxy_records_messages_sent_to_tv(self):
        tv = Proxy(Television())

        tv.power()
        tv.channel = 10

        self.assertEqual(['power', 'channel'], tv.messages())

    def test_proxy_handles_invalid_messages(self):
        tv = Proxy(Television())

        with self.assertRaises(AttributeError):
            tv.no_such_method()


    def test_proxy_reports_methods_have_been_called(self):
        tv = Proxy(Television())

        tv.power()
        tv.power()

        self.assertTrue(tv.was_called('power'))
        self.assertFalse(tv.was_called('channel'))

    def test_proxy_counts_method_calls(self):
        tv = Proxy(Television())

        tv.power()
        tv.channel = 48
        tv.power()

        self.assertEqual(2, tv.number_of_times_called('power'))
        self.assertEqual(1, tv.number_of_times_called('channel'))
        self.assertEqual(0, tv.number_of_times_called('is_on'))

    def test_proxy_can_record_more_than_just_tv_objects(self):
        proxy = Proxy("Py Ohio 2010")

        result = proxy.upper()

        self.assertEqual("PY OHIO 2010", result)

        result = proxy.split()

        self.assertEqual(["Py", "Ohio", "2010"], result)
        self.assertEqual(['upper', 'split'], proxy.messages())

# ====================================================================
# The following code is to support the testing of the Proxy class.  No
# changes should be necessary to anything below this comment.

# Example class using in the proxy testing above.
class Television:
    def __init__(self):
        self._channel = None
        self._power = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    def power(self):
        if self._power == 'on':
            self._power = 'off'
        else:
            self._power = 'on'

    def is_on(self):
        return self._power == 'on'

# Tests for the Television class.  All of theses tests should pass.
class TelevisionTest(Koan):
    def test_it_turns_on(self):
        tv = Television()

        tv.power()
        self.assertTrue(tv.is_on())

    def test_it_also_turns_off(self):
        tv = Television()

        tv.power()
        tv.power()

        self.assertFalse(tv.is_on())

    def test_edge_case_on_off(self):
        tv = Television()

        tv.power()
        tv.power()
        tv.power()

        self.assertTrue(tv.is_on())

        tv.power()

        self.assertFalse(tv.is_on())

    def test_can_set_the_channel(self):
        tv = Television()

        tv.channel = 11
        self.assertEqual(11, tv.channel)
