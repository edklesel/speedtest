import unittest
from Speedtest.influx import Connection, record_speed
from datetime import datetime as dt
from random import randint

testdb = 'speedtest_test'

class TestConnection(unittest.TestCase):

    def test_openconnection(self):
        with Connection() as client:
            self.assertEqual(type(client.ping()), str)
            
    
    def test_createdb(self):
        with Connection(testdb) as client:
            self.assertIn({'name': testdb}, client.get_list_database())

    @classmethod
    def tearDownClass(cls):
        with Connection(testdb) as client:
            client.drop_database(testdb)
        return super().tearDownClass()
    

class TestRecordSpeed(unittest.TestCase):

    def test_recordspeed(self):
        testdate = dt.utcnow()
        testdownload = randint(1, 999999999)
        testupload = randint(1,999999999)

        record_speed(
            download=testdownload,
            upload=testupload,
            server='Test Server',
            datetime=testdate,
            database=testdb
            )

        with Connection(testdb) as client:
            results = list(client.query('SELECT download_speed, upload_speed FROM speed').get_points('speed'))[0]
        
        self.assertTrue(
            # The Z has to be added manually as python does not include timezone info by default
            dt.strptime(results['time'],'%Y-%m-%dT%H:%M:%S.%fZ') == testdate,
            msg=f"""
            results: time={results['time']}
            expected: time={testdate.isoformat() + 'Z'}
            """
        )
        self.assertTrue(
            results['download_speed'] == testdownload,
            msg=f"""
            results: download={results['download_speed']}
            expected: download={testdownload}
            """
        )
        self.assertTrue(
            results['upload_speed'] == testupload,
            msg=f"""
            results: upload={results['upload_speed']}
            expected: upload={testupload}
            """
        )

    def tearDown(self):
        with Connection(testdb) as client:
            client.drop_database(testdb)
        return super().tearDown()
