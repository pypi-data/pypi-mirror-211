"""doc"""
import ctyparser

cty = ctyparser.BigCty()
# cty.import_dat("./cty.dat")
# cty.dump("./cty.json")
print(cty.version)
print(f"{cty.update()}")
cty.dump("./test.json")
