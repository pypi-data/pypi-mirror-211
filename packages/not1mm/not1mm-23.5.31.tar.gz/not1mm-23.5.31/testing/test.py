"""doc"""
import ctyparser

cty = ctyparser.BigCty()
cty.import_dat("./cty.dat")
cty.dump("./cty.json")
