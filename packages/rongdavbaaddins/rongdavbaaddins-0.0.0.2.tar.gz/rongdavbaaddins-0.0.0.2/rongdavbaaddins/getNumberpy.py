from getNumber import GetFunNum
import  sys
if __name__ == "__main__":
    functionName = sys.argv[1]
    token = sys.argv[2]
    # functionName = "OCR"
    # token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDAyODEzIiwiaXAiOiIxNzIuMTYuNzMuMSIsIm1hYyI6IjAwMmI2N2UyMmQ1OCJ9.AodD4YiUvl6rVdY0xk3ExnRMVSNxwx0un3vyjZWVDcU'
    GetFunNum(functionName, token)