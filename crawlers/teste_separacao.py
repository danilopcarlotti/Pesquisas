import re

a = """
\n\nPROC lá lá lá lá\nPROC blá blá blá\n\nPET blá blá blá\nPET
"""
b = "(\n\n)(PROC)"
text = re.sub(r"{}".format(b), r"\1@@\2", a)
text = re.sub(r"(\n\n)(PET)", r"\1@@\2", text)
print(re.split(r"@@", text))
