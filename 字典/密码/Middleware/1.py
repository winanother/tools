# 读取weblogic.txt文件，根据用户选择提取斜杠前或斜杠后的内容并写入相应文件

# 添加用户交互功能
print("请选择提取内容：")
print("0 - 提取斜杠前的内容（用户名）")
print("1 - 提取斜杠后的内容（密码）")

# 修改输入验证逻辑，确保只接受有效输入
while True:
    choice = input("请输入选项（0或1）：").strip()
    if choice in ['0', '1']:
        break
    else:
        print("输入无效，请输入0或1！")

with open('weblogic.txt', 'r') as input_file:
    if choice == '0':
        # 提取斜杠前的内容并写入webLusr.txt
        with open('webLusr.txt', 'w') as output_file:
            for line in input_file:
                line = line.strip()
                if '/' in line:
                    # 提取斜杠前的内容
                    username = line.split('/')[0]
                    output_file.write(username + '\n')
        print("用户名已提取到webLusr.txt")
    else:
        # 提取斜杠后的内容并写入webLwp.txt
        with open('webLwp.txt', 'w') as output_file:
            for line in input_file:
                line = line.strip()
                if '/' in line:
                    # 提取斜杠后的内容
                    password = line.split('/')[-1]
                    output_file.write(password + '\n')
        print("密码已提取到webLwp.txt")