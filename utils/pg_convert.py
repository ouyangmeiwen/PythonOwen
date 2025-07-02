import os

boolean_fields = ["IsDeleted", "IsTree", "IsEnable","IsDefault","IsSupportUpgrade", "IsSupportOpen", "IsNeedActivate"]

def parse_fields(field_str):
    # 字段格式：[Id], [CreationTime], ...
    fields = []
    cur = ""
    in_brackets = False
    for ch in field_str:
        if ch == '[':
            in_brackets = True
            cur = ""
        elif ch == ']':
            in_brackets = False
            fields.append(cur.strip())
        elif in_brackets:
            cur += ch
    return fields

def split_values(value_str):
    # 简单逗号分割，不支持复杂字符串中逗号的场景
    parts = []
    current = ""
    in_str = False
    quote_char = ''
    for ch in value_str:
        if in_str:
            current += ch
            if ch == quote_char:
                in_str = False
        else:
            if ch in ("'", '"'):
                in_str = True
                quote_char = ch
                current += ch
            elif ch == ',':
                parts.append(current.strip())
                current = ""
            else:
                current += ch
    if current.strip():
        parts.append(current.strip())
    return parts

def replace_boolean_values(values, fields):
    for i, field in enumerate(fields):
        if field in boolean_fields and i < len(values):
            val = values[i]
            # 处理常见0/1的表示
            if val in ("0", "N'0'", "'0'"):
                values[i] = "false"
            elif val in ("1", "N'1'", "'1'"):
                values[i] = "true"
    return values

def process_segment(segment):
    # 找 INSERT INTO ... (...) VALUES (...)
    segment = segment.strip()
    if not segment:
        return segment

    # 找出字段列表和values部分
    insert_idx = segment.upper().find("INSERT INTO")
    values_idx = segment.upper().find("VALUES")
    if insert_idx == -1 or values_idx == -1:
        return segment  # 非INSERT语句不处理

    # 拿字段部分，找到第一个圆括号内内容
    fields_part_start = segment.find('(', insert_idx)
    fields_part_end = segment.find(')', fields_part_start)
    fields_str = segment[fields_part_start+1:fields_part_end]

    # 拿values部分，找VALUES后面的括号内容
    values_part_start = segment.find('(', values_idx)
    values_part_end = segment.rfind(')')
    values_str = segment[values_part_start+1:values_part_end]

    fields = parse_fields(fields_str)
    values = split_values(values_str)
    new_values = replace_boolean_values(values, fields)

    # 重组SQL
    new_segment = (segment[:fields_part_start+1] + ", ".join(f"[{f}]" for f in fields) + segment[fields_part_end:values_part_start+1]
                   + ", ".join(new_values) + segment[values_part_end:])
    return new_segment

def process_sql_text(sql_text):
    segments = sql_text.split("\nGO\n")
    new_segments = [process_segment(s) for s in segments]
    return "\nGO\n".join(new_segments)

def process_sql_file(input_path, output_path):
    with open(input_path, encoding="utf-8") as f:
        text = f.read()
    new_text = process_sql_text(text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"✅ 处理完成 {input_path} -> {output_path}")

def batch_process_dir(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for fname in os.listdir(input_dir):
        if fname.lower().endswith(".sql"):
            process_sql_file(os.path.join(input_dir, fname), os.path.join(output_dir, fname))
    print("🎉 所有文件处理完成！")
if __name__ == "__main__":
    input_directory = "./sql_files"   # 你的输入目录
    output_directory = "./converted"  # 你的输出目录

    batch_process_dir(input_directory, output_directory)