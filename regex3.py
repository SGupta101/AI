import sys
idx = int(sys.argv[1])-50
myRegexLst = [r"/(\w)*\w*\1\w*/i",
r"/(\w)*(\w*\1){3}\w*/i",
r"/^(([10])\2*([01]*)?\2+|[01])$/",
r"/\b(?=\w*cat)\w{6}\b/i",
r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i",
r"/\b(?!\w*cat)\w{6}\b/i",
r"/\b(?!(\w)*\w*\1\w*)\w+/i",
r"/^((?!.*10011)[01]*)?$/",
r"/\w*([aeiou])(?!\1)[aeiou]\w*/i",
r"/^((?!.*1(0|1)1)[01]*|)$/"]
print(myRegexLst[idx])