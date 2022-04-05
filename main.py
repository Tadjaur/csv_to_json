import json as Gson
import sys


def extract_argv(list_args: list) -> dict:
    assert type(list_args) == list, "le parametre listArgs doit etre une liste"
    return dict(map(lambda e: tuple(e.split("--")[1].split("=")), list_args))


if __name__ == "__main__":
    finalData = []
    params = None
    try:
        params = extract_argv(sys.argv[1:])
        _separator = params.get("separator")
        if _separator is not None and _separator == '\\t':
            _separator = '\t'
        with open(params.get('file') or "data.text") as file:
            line = file.readline()
            headerList = line[:-1].split( _separator or "\t")
            ln = len(headerList)
            lineCount = 1
            while len(line) > 0:
                line = file.readline()
                lineCount = lineCount + 1
                lineSplit = line[:-1].split(_separator or "\t")
                if len(lineSplit) > ln:
                    print("error when parsing data, the number of separator is greater than ", len(headerList) - 1,
                          "\nline ", lineCount, " ::> ", line, "\n")
                    file.close()
                    exit(-255)
                ref = {}
                for i in range(ln):
                    vl = lineSplit[i].strip() if i < len(lineSplit) else None
                    if params.get('ignore') is not None and (vl == "" or vl is None):
                        continue
                    ref[headerList[i].strip()] = vl
                finalData.append(ref)
        print(Gson.dumps(finalData, sort_keys=True, indent=2))
    except :
        assert False, "enable to parse arguments"
