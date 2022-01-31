# Import các thư viện cần thiết
import copy
from collections import deque

def readFile(fileName, process_info: dict):
    """Hàm đọc tập tin dữ liệu đầu vào và lưu vào cấu trúc dữ liệu đã được thiết kế"""
    with open(fileName, 'r') as f:
        read_data = f.readlines() # Đọc các dòng trong tập tin đầu vào vào 1
                                  # danh sách mỗi phần tử của danh sách là 1 
                                  # dòng trong tập tin
        temp_list = read_data[0].split('\t') # Tách dòng đầu tiên theo kí tự '\t'
        process_info["number_of_process"] = int(temp_list[0]) # Lấy được số tiến trình
        process_info["time_quantum"] = int(temp_list[1]) # Lấy được thời gian quantum
        # Tạo 1 dict để lưu tạm thông tin của 1 tiến trình
        temp_process = {
            "name": "",
            "arrival_time": "",
            "CPU_burst": "",
            "priority": "",
            }
        # Lặp và thực hiện cắt chuỗi, xử lý với n - 1 dòng cuối cùng trong tập tin để lấy được 
        # thông tin của các tiến trình
        for i in range(1, len(read_data)):
            temp_list = read_data[i].split('\t')
            temp_process["name"] = temp_list[0]
            temp_process["arrival_time"] = int(temp_list[1])
            temp_process["CPU_burst"] = int(temp_list[2])
            if (temp_list[3][-1] == '\n'):
                temp_list[3] = temp_list[3][:-1]
            temp_process["priority"] = int(temp_list[3])
            # Thêm thông tin của tiến trình vừa lấy được vào danh sách các tiến trình
            process_info["process_list"].append(copy.deepcopy(temp_process))

def writeFile(fileName, writen_data):
    """Hàm viết dữ liệu vào tập tin"""
    with open(fileName, 'w') as f:
        for i in range(len(writen_data)):
            # Mỗi phần tử trong danh sách writen_data được viết thành 1 dòng trong tập tin
            f.write(writen_data[i])


def FCFSScheduling(processes):
    """Hàm mô phỏng chiến lược FCFS"""
    n = processes["number_of_process"] # Lấy số tiến trình
    process_list = processes["process_list"] # Lấy danh sách tiến trình
    WT = [0 for i in range(n)] # Mảng lưu waiting time
    TT = [0 for i in range(n)] # Mảng lưu turn around time
    CT = [0 for i in range(n)] # Mảng lưu complete time
    # Tính complete time và waiting time
    for i in range(1, n):
        CT[i] = (CT[i - 1] + process_list[i - 1]["CPU_burst"])
        WT[i] = CT[i] - process_list[i]["arrival_time"]
    # Tính turn around time   
    for i in range(n):
        TT[i] = process_list[i]["CPU_burst"] + WT[i]
    # Tính waiting time trung bình và turn around time trung bình
    total_wt = 0
    total_tt = 0
    for i in range(n):
        total_wt += WT[i]
        total_tt += TT[i]
    average_wt = round(total_wt/n, 2);
    average_tt = round(total_tt/n, 2);
    # Chuẩn bị dữ liệu để viết vào tập tin đầu ra
    writen_data = []
    line = "Scheduling chart: "
    for i in range(n):
        line = line + str(CT[i]) + '~' + process_list[i]["name"] + '~'
    line = line + str(CT[n - 1] + process_list[n - 1]["CPU_burst"]) + '\n'
    writen_data.append(line)
    for i in range(n):
        name = process_list[i]["name"]
        line = f"{name}:\tTT = {TT[i]}\tWT = {WT[i]}\n"
        writen_data.append(line)
    line = f"Average:\tTT = {average_tt}\tWT = {average_wt}"
    writen_data.append(line)
    # Viết dữ liệu vào tập tin đầu ra
    writeFile("FCFS.txt", writen_data)


def SJFScheduling(processes):
    """Hàm mô phỏng chiến lược SJF"""
    n = processes["number_of_process"] # Lấy số tiến trình
    process_list = processes["process_list"] # Lấy danh sách tiến trình
    WT = [0 for i in range(n)] # Mảng lưu waiting time
    TT = [0 for i in range(n)] # Mảng lưu turn around time
    RT = [0 for i in range(n)] # Mảng lưu thời gian còn chạy lại (remaining time)
                               # của mỗi tiến trình
	# Ban đầu, mỗi tiến trình đều có remaining time bằng CPU burst
    for i in range(n):
        RT[i] = process_list[i]["CPU_burst"]
        
    completed_process = 0 # Lưu số tiến trình đã chạy xong
    time = 0 # Biến lưu thời gian
    minm = 999999999 # Biến lưu thời gian chạy còn lại nhỏ nhất
    shortest = 0 # Biến lưu chỉ mục của tiến trình có remaining time nhỏ nhất
    last_executed = -1 # Biến lưu chỉ mục của tiến trình được chạy gần đây nhất
    check = False # Biến kiểm tra xem có tiến trình nào chuẩn bị được chạy hay không
    schedulingChart = "" # Biến lưu scheduling chart
	# Lặp cho đến khi tất cả tiến trình đều chạy xong
    while (completed_process != n):		
		# Tìm tiến trình có thời gian chạy còn lại nhỏ nhất và đã arrive vào hàng đợi (ready_queue)
        for j in range(n):
            if ((process_list[j]["arrival_time"] <= time) and (RT[j] < minm) and RT[j] > 0):
                minm = RT[j]
                shortest = j
                check = True
                
        if (check == False):
            time += 1
            continue
        # Cập nhật scheduling chart
        if (shortest != last_executed):
            schedulingChart = schedulingChart + str(time) + '~' + process_list[shortest]["name"] + '~'
            last_executed = shortest
		
        RT[shortest] -= 1 # Giảm thời gian chạy còn lại của tiến trình đi 1
        minm = RT[shortest] # Cập nhật thời gian chạy còn lại nhỏ nhất
        if (minm == 0):
            minm = 999999999
		# Nếu tiến trình này đã chạy xong
        if (RT[shortest] == 0):
            completed_process += 1 # Tăng số tiến trình đã chạy xong thêm 1
            check = False
			# Tính waiting time của tiến trình này
            WT[shortest] = (time + 1 - process_list[shortest]["CPU_burst"] - process_list[shortest]["arrival_time"])

            if (WT[shortest] < 0):
                WT[shortest] = 0
		# Tăng thời gian thêm 1
        time += 1
    # Cập nhật scheduling chart
    schedulingChart = schedulingChart + str(time) + '\n'
    # Tính turn around time
    for i in range(n):
    	TT[i] = process_list[i]["CPU_burst"] + WT[i]
    # Tính waiting time trung bình và turn around time trung bình
    total_wt = 0
    total_tt = 0
    for i in range(n):
        total_wt += WT[i]
        total_tt += TT[i]
    average_wt = round(total_wt/n, 2)
    average_tt = round(total_tt/n, 2)
    # Chuẩn bị dữ liệu để viết vào tập tin đầu ra
    writen_data = []
    line = "Scheduling chart: " + schedulingChart
    writen_data.append(line)
    for i in range(n):
        name = process_list[i]["name"]
        line = f"{name}:\tTT = {TT[i]}\tWT = {WT[i]}\n"
        writen_data.append(line)
    line = f"Average:\tTT = {average_tt}\tWT = {average_wt}"
    writen_data.append(line)
    # Viết dữ liệu vào tập tin đầu ra
    writeFile("SJF.txt", writen_data)


def RoundRobinScheduling(processes):
    """Hàm mô phỏng chiến lược Round Robin"""
    n = processes["number_of_process"] # Lấy số tiến trình
    process_list = processes["process_list"] # Lấy danh sách tiến trình
    WT = [0 for i in range(n)] # Mảng lưu waiting time
    TT = [0 for i in range(n)] # Mảng lưu turn around time
    quantum = processes["time_quantum"] # Lấy thời gian quantum
    completed_process = 0 # Lưu số tiến trình đã chạy xong
    ready_queue = deque([]) # Khởi tạo hàng đợi
    time = 0 # Biến lưu thời gian
    schedulingChart = "" # Biến lưu scheduling chart 
    
    queue_element = []
    # Thêm các phần tử vào hàng đợi, mỗi phần tử gồm thông tin của tiến trình và thời gian chạy còn lại của tiến trình
    for process in process_list:
        queue_element = [process, process["CPU_burst"]] # Ban đầu thời gian chạy còn lại của tiến trình chính là CPU burst
        ready_queue.append(queue_element)
    # Lặp cho đến khi chỉ còn 1 tiến trình trong hàng đợi, n - 1 tiến trình còn lại đã chạy xong   
    while(completed_process != n - 1):    
        for i in range(len(ready_queue)):
            current_process = ready_queue.popleft() # Lấy ra 1 tiến trình
            if (current_process[0]["arrival_time"] > time):
                ready_queue.append(current_process)
                continue
            
            schedulingChart = schedulingChart + str(time) + '~' # Cập nhật scheduling chart
            
            if current_process[1] < quantum: # Nếu tiến trình này có thời gian chạy còn lại nhỏ hơn thời gian quantum
                time += current_process[1] # Tăng thời gian thêm 1 lượng bằng thời gian chạy còn lại của tiến trình
                # Tình waiting time của tiến trình
                WT[int(current_process[0]["name"][1:]) - 1] = time - current_process[0]["CPU_burst"] - current_process[0]["arrival_time"]
                completed_process += 1 # Tăng số tiến trình đã chạy xong thêm 1
            else: # Nếu tiến trình này có thời gian chạy còn lại lớn hơn thời gian quantum thì cho nó chạy trong thời gian
                  # quantum rồi block và đưa về cuối hàng đợi
                time += quantum # Tăng thời gian thêm 1 lượng bằng thời gian quantum
                queue_element = [current_process[0], current_process[1] - quantum] # Giảm thời gian chạy còn lại của tiến trình
                                                                                   # đi 1 lượng bằng thời gian quantum
                ready_queue.append(queue_element) # Thêm tiến trình vào cuối hàng đợi
                
            schedulingChart = schedulingChart + current_process[0]["name"] + '~' # Cập nhật scheduling chart
    
    last_process = ready_queue.popleft() # Lấy ra phần tử cuối cùng trong hàng đợi và cho nó chạy
    schedulingChart = schedulingChart + str(time) + '~' + last_process[0]["name"] + '~' # Cập nhật scheduling chart
    time += last_process[1] # Tăng thời gian lên 1 lượng bằng thồi gian chạy còn lại của tiến trình
    # Tính waiting time của tiến trình
    WT[int(last_process[0]["name"][1:]) - 1] = time - last_process[0]["CPU_burst"] - last_process[0]["arrival_time"]
    schedulingChart = schedulingChart + str(time) + '\n' # Cập nhật scheduling chart
    # Tính turn around time
    for i in range(n):
    	TT[i] = process_list[i]["CPU_burst"] + WT[i]
     # Tính waiting time trung bình và turn around time trung bình
    total_wt = 0
    total_tt = 0
    for i in range(n):
        total_wt += WT[i]
        total_tt += TT[i]
    average_wt = round(total_wt/n, 2)
    average_tt = round(total_tt/n, 2)
    # Chuẩn bị dữ liệu để viết vào tập tin đầu ra
    writen_data = []
    line = "Scheduling chart: " + schedulingChart
    writen_data.append(line)
    for i in range(n):
        name = process_list[i]["name"]
        line = f"{name}:\tTT = {TT[i]}\tWT = {WT[i]}\n"
        writen_data.append(line)
    line = f"Average:\tTT = {average_tt}\tWT = {average_wt}"
    writen_data.append(line)
    # Viết dữ liệu vào tập tin đầu ra
    writeFile("RR.txt", writen_data)
    
def sortKey(e):
    """Hàm phục vụ cho việc sắp xếp các tiến trình theo độ ưu tiên"""
    return e[2]

def PriorityScheduling(processes):
    """Hàm mô phỏng chiến lược priority"""
    n = processes["number_of_process"] # Lấy số tiến trình
    process_list = [] # Tạo danh sách chứa các tiến trình và các thông tin liên quan
    WT = [0 for i in range(n)] # Mảng lưu waiting time
    TT = [0 for i in range(n)] # Mảng lưu turn around time
    completed_process = 0 # Biến lưu số tiến trình đã hoàn thành
    time = 0 # Biến lưu thời gian
    schedulingChart = "" # Biến lưu scheduling chart
    process_list_element = []
    last_executed_process = "" # Biến lưu tên tiến trình được chạy gần đây nhất
    # Thêm các phần tử vào danh sách chứa các tiến trình và các thông tin liên quan
    for process in processes["process_list"]:
        process_list_element = [process, process["CPU_burst"], process["priority"]] # Mỗi phần tử chứa thông tin của tiến trình
                                                                                    # thời gian chạy còn lại và độ ưu tiên
        process_list.append(process_list_element)
    # Lặp đến khi tất cả tiến trình đều chạy xong
    while(completed_process != n):
        process_list.sort(key = sortKey) # Sắp xếp các tiến trình theo độ ưu tiên
        i = 0
        current_process = process_list[i]
        # Lặp để tìm ra tiến trình có độ ưu tiên cao nhất và đã arrive vào ready queue
        while(current_process[0]["arrival_time"] > time):
            i += 1
            current_process = process_list[i]
                
        if (current_process[1] == 1): # Nếu thời gian chạy còn lại của tiến trình này là 1
            # Tính waiting time của tiến trình
            WT[int(current_process[0]["name"][1:]) - 1] = time + 1 - current_process[0]["CPU_burst"] - current_process[0]["arrival_time"]
            completed_process += 1 # Tăng số tiến trình đã hoàn thành thêm 1
            process_list.pop(i) # Lấy tiến trình này ra khỏi danh sách
        else: # Ngược lại, nếu tiến trình này chưa chạy xong thì giảm thời gian chạy còn lại của nó đi 1
            process_list[i][1] -= 1
        
        # Cập nhật scheduling chart 
        if (last_executed_process != current_process[0]["name"]):
            schedulingChart = schedulingChart + str(time) + '~' + current_process[0]["name"] + '~'
            last_executed_process = current_process[0]["name"]
        time += 1 # Tăng thời gian thêm 1
    
    schedulingChart = schedulingChart + str(time) + '\n' # Cập nhật scheduling
    process_list = processes["process_list"]
    # Tính turn around time
    for i in range(n):
    	TT[i] = process_list[i]["CPU_burst"] + WT[i]
     # Tính waiting time trung bình và turn around time trung bình
    total_wt = 0
    total_tt = 0
    for i in range(n):
        total_wt += WT[i]
        total_tt += TT[i]
    average_wt = round(total_wt/n, 2)
    average_tt = round(total_tt/n, 2)
    # Chuẩn bị dữ liệu để viết vào tập tin đầu ra
    writen_data = []
    line = "Scheduling chart: " + schedulingChart
    writen_data.append(line)
    for i in range(n):
        name = process_list[i]["name"]
        line = f"{name}:\tTT = {TT[i]}\tWT = {WT[i]}\n"
        writen_data.append(line)
    line = f"Average:\tTT = {average_tt}\tWT = {average_wt}"
    writen_data.append(line)
    # Viết dữ liệu vào tập tin đầu ra
    writeFile("Priority.txt", writen_data)

    
def main():
    process_info = {
        "number_of_process": 0,
        "time_quantum": 0,
        "process_list": []
        }
    readFile("Input.txt", process_info)
    FCFSScheduling(process_info)
    SJFScheduling(process_info)
    RoundRobinScheduling(process_info)
    PriorityScheduling(process_info)
    
main()