from Vbalog import FunctionLog
import sys, datetime
if __name__ == "__main__":
    FuncitonId = sys.argv[1]
    token = sys.argv[2]
    useNumber = sys.argv[3]
    # startTime = sys.argv[4]
    # endTime = sys.argv[5]
    details = sys.argv[6]
    # FuncitonId = 91
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlwIjoiMTcyLjE2LjczLjEiLCJtYWMiOiIwMDJiNjdlMjJkNTgifQ.MU46YMN6XTcsIIUf6KsjuhcKlleQ8_56rCx0YfMuNIE'
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxOTIuMTY4LjEyLjkiLCJtYWMiOiJkODgwODM3NzYzN2MifQ.ZNi3wVfSDoBr29bcbfZLTySYGk__E62lpG05i0PXzEoeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAxNzMyIiwiaXAiOiIxOTIuMTY4LjEyLjkiLCJtYWMiOiJkODgwODM3NzYzN2MifQ.ZNi3wVfSDoBr29bcbfZLTySYGk__E62lpG05i0PXzEo'
    # useNumber = 10
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # details = ''
    FunctionLog(FuncitonId, token, useNumber, startTime, endTime, details)