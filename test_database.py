import unittest
from unittest.mock import patch, MagicMock
import main

class TestMongoTool(unittest.TestCase):

    @patch('pymongo.MongoClient')
    def test_mongo_tool(self, mock_mongo_client):
        # Mock the MongoDB client and database
        data = main.mongoTool()
        sum  = 0
        for order in data:
            sum += 1
            print(order)
            print('\n')
        print(sum)


if __name__ == '__main__':
    unittest.main()