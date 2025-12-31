from slugger import slugify

tests = [
    "What is the EU AI Act?",
    "Who is the all time best Bangladeshi cricketer?",
    "  Spaces   and --- symbols!!! ",
    "",
]

for t in tests:
    print(f"{t!r} → {slugify(t)}")
