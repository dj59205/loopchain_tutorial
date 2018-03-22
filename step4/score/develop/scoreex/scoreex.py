import os
import sys
import leveldb
import json

from loopchain.blockchain import ScoreBase
from loopchain.tools.score_helper import ScoreHelper, ScoreDatabaseType, LogLevel

"""Utility function for JSON RPC 2.0
"""

def create_jsonrpc_error_response(_id, code, message=None, data=None):
    """Create jsonrpc error response json object.
    """
    response = create_jsonrpc_common_response(_id)
    response["error"] = create_jsonrpc_error_object(code, message, data)
    return response


def create_jsonrpc_success_response(_id, result):
    """Create jsonrpc success response json object.
    """
    response = create_jsonrpc_common_response(_id)
    response["result"] = result

    return response


def create_jsonrpc_common_response(_id):
    """Create common response json object
    """
    response = {
        "jsonrpc": "2.0",
        "id": _id,
    }
    return response

class SCOREExError(Exception):
    """Exception module for SCOREEx in error case.
    """
    def __init__(self, message=None):
        self.message = message


class UserScore(ScoreBase):
    """Example SCORE code.
    """
    def __init__(self, info=None):
        # Load package.py and initilize package. 
        super().__init__(info)
        if info is None:
            with open(dirname(__file__)+'/'+ScoreBase.PACKAGE_FILE, "r") as f:
                self.__score_info = json.loads(f.read())
                f.close()
        else:
            self.__score_info = info

        # Init SCORE helper.
        self.__score_helper = ScoreHelper()

        #Init database as levelDB.
        db = self.__score_helper.load_database(
                score_id='scoreex_db', # Use unique ID for each SCORE.
                database_type=ScoreDatabaseType.leveldb)
        self.__db = db

        # link function name and function for invoke.
        invoke_methods = {
            'invoke_foo': self.__invoke_foo
        }

        # link function name and function for query.
        query_methods = {
            'query_foo': self.__query_foo
        }


    def invoke(self, transaction, block):
        self.__score_helper.log("SCOREEX", "Invoke() begin.", LogLevel.DEBUG)

        # Parse data.
        data = transaction.get_data_string()
        params = json.loads(data)

        # Call function by name.
        method_name = params['method']
        method = invoke_methods.get(method_name, None)

        # Call pre-defined functions in package.json by the request in transaction.
        try:
            response = method(transaction, block, params['params'])
            return json.dumps(response)
        except:
            raise SCOREExError(f"No method like {method_name}.")

    def query(self, params):
        self.__score_helper.log("SCOREEX", "Query() begin.", LogLevel.DEBUG)

        # Parse data.
        data = transaction.get_data_string()
        params = json.loads(data)

        # Call function by name.
        method_name = params['method']

        try:
            response = invoke_methods.get(method_name, None)(params)
            return json.dumps(response)
        except:
            raise SCOREExError(f"No method like {method_name}.")

    def info(self):
        return self.__score_info

    def __invoke_foo(self, transaction, block, params):
        pass

    def __query_foo(self, params):
        pass
