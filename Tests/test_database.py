import unittest
import os
from Speedtest.database import Connection, record_speed
from datetime import datetime as dt

testdb = 'tests.db'

class TestConnection(unittest.TestCase):

    def test_createdb(self):
        with Connection(testdb) as c:
            pass
        self.assertTrue(os.path.exists(testdb))

    def test_executequery(self):

        with Connection(testdb) as c:
            with open('Tests/Queries/test_createtable.sql', 'r') as f:
                c.execute(f.read())
            
            with open('Tests/Queries/test_createtable_select.sql', 'r') as f:
                results = c.execute(f.read()).fetchone()

        self.assertTrue('TestTable' in results)
        
    def test_executescript(self):

        with Connection(testdb) as c:
            with open('Tests/Queries/test_insert.sql', 'r') as f:
                c.executescript(f.read()).fetchone()
        
            with open('Tests/Queries/test_insert_select.sql', 'r') as f:
                results = c.execute(f.read()).fetchall()

        self.assertEqual(('TestVal1', 1), results[0])
        self.assertEqual(('TestVal2', 2), results[1])

    @classmethod
    def tearDownClass(cls):
        os.remove(testdb)
        return super().tearDownClass()


class TestRecordSpeed(unittest.TestCase):

    def setUp(self):
        self.ProjectDir = os.getcwd()
        os.chdir('Tests')
        with Connection('speedtest.db') as c:
            with open('../Speedtest/Queries/table_speeds.sql', 'r') as f:
                c.executescript(f.read())
        return super().setUp()

    def test_recordspeed(self):
        testdate = dt.now()
        record_speed(download=1, upload=2, datetime=testdate)

        with Connection('speedtest.db') as c:
            with open('Queries/test_recordspeed_select.sql', 'r') as f:
                results = c.execute(f.read()).fetchone()
        
        self.assertEqual((str(testdate), 1, 2), results)
    
    def tearDown(self):
        os.remove('speedtest.db')
        os.chdir(self.ProjectDir)
        return super().tearDown()
