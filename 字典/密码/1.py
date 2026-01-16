import hashlib

def generate_md5_from_file(input_file, output_file):
    """
    读取输入文件中的每一行，生成对应的MD5哈希值，
    并将原文和MD5值写入输出文件。
    """
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for line in infile:
            # 去除行末的换行符
            password = line.strip()
            
            # 生成MD5哈希值
            md5_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
            
            # 写入输出文件
            outfile.write(f"{md5_hash}\n")
            
    print(f"MD5哈希值已生成并保存到 {output_file}")

# 使用示例
input_filename = "top50.txt"
output_filename = "MD5.txt"

generate_md5_from_file(input_filename, output_filename)