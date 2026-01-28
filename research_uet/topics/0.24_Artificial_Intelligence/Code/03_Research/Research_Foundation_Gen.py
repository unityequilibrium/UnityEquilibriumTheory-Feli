import os
import random

# Configuration
OUTPUT_DIR = r"..\..\Data\00_Foundation"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "foundation_basics.txt")


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def generate_math_axioms(n=100):
    lines = []
    lines.append("# DOMAIN: MATHEMATICS & LOGIC")
    for _ in range(n):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        lines.append(f"{a} + {b} = {a+b}")
        lines.append(f"{a} - {b} = {a-b}")
        if a < b:
            lines.append(f"{a} < {b}")
        elif a > b:
            lines.append(f"{a} > {b}")
        else:
            lines.append(f"{a} == {b}")
    return lines


def generate_geometry_facts():
    facts = [
        "# DOMAIN: GEOMETRY & SPACE",
        "Circle is strict, maximal area for fixed perimeter.",
        "Triangle is rigid, stable structure.",
        "Square is regular, ordered grid.",
        "Line is shortest path between two points (in Euclidean).",
        "Sphere is minimal surface area for volume.",
        "Symmetry implies conservation laws.",
        "Parallel lines never meet in flat space.",
        "Curvature represents energy density.",
        "Dimension is a degree of freedom.",
        "Point has zero dimension.",
        "Line has one dimension.",
        "Plane has two dimensions.",
        "Space has three dimensions.",
        "Time is the fourth dimension of becoming.",
    ]
    return facts


def generate_logic_rules():
    rules = [
        "# DOMAIN: LOGIC & CAUSALITY",
        "If A implies B, and A is True, then B is True.",
        "A cannot be both True and False (Law of Non-Contradiction).",
        "Either A is True or A is False (Law of Excluded Middle).",
        "Effect follows Cause unless Time is reversed.",
        "Structure determines Function.",
        "Energy flows from High to Low.",
        "Order requires Energy input.",
        "Disorder increases without Energy input (Entropy).",
        "Information is Resolution of Uncertainty.",
    ]
    return rules


def generate_basic_thai_grammar(n=100):
    lines = []
    lines.append("# DOMAIN: LANGUAGE STRUCTURE (THAI)")
    subjects = ["ฉัน", "เขา", "แมว", "นก", "ระบบ", "ธรรมชาติ", "พลังงาน", "จักรวาล"]
    verbs = ["กิน", "เดิน", "วิ่ง", "มี", "เป็น", "ชอบ", "สร้าง", "ทำลาย"]
    objects = ["ข้าว", "น้ำ", "ปลา", "บ้าน", "สมดุล", "ความรู้", "พลัง", "เวลา"]

    for _ in range(n):
        s = random.choice(subjects)
        v = random.choice(verbs)
        o = random.choice(objects)
        lines.append(f"{s} {v} {o}")
        lines.append(f"{s} คือ {o} หรือไม่?")
        lines.append(f"ถ้า {s} {v} {o} แล้ว {s} จะมีความสุข")

    return lines


def main():
    ensure_dir(OUTPUT_DIR)

    data = []
    data.extend(generate_math_axioms(200))
    data.extend(generate_geometry_facts())
    data.extend(generate_logic_rules())
    data.extend(generate_basic_thai_grammar(200))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(data))

    print(f"✅ Foundation Data Generated: {len(data)} lines at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
