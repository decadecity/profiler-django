from django.test import TestCase

from middleware import combine

class SimpleTest(TestCase):
    def test_combine_existing(self):
        server = {
            1: True,
            2: False,
        }
        client = {
            1: 0,
            2: 1,
        }
        result = {
            1: True,
            2: True,
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_pass(self):
        server = {
            1: 1,
            2: 0,
        }
        client = {}
        result = {
            1: True,
            2: False,
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_new(self):
        server = {}
        client = {
            1: 1,
            2: 0,
        }
        result = {
            1: True,
            2: False,
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_string_client(self):
        server = {}
        client = {
            1: '1',
            2: '0',
        }
        result = {
            1: True,
            2: False,
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_flickr_suffix_new(self):
        server = {}
        client = {
            'flickr_suffix': '_m',
        }
        result = {
            'flickr_suffix': '_m',
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_flickr_suffix_new_blank(self):
        server = {}
        client = {
            'flickr_suffix': '',
        }
        result = {
            'flickr_suffix': '',
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_flickr_suffix_existing(self):
        server = {
            'flickr_suffix': '_b',
        }
        client = {
            'flickr_suffix': '_m',
        }
        result = {
            'flickr_suffix': '_m',
        }
        self.assertEqual(combine(server, client), result)
    def test_combine_flickr_suffix_existing_blank(self):
        server = {
            'flickr_suffix': '_b',
        }
        client = {
            'flickr_suffix': '',
        }
        result = {
            'flickr_suffix': '',
        }
        self.assertEqual(combine(server, client), result)
