
import hashlib
import json
import os
import subprocess
import sys
import time
import bztt_requests


# 校验软件信息
class checkSoftware():
    
    api_url = ""
    authorization = ""
    software_id = -1
    def __init__(self,software_info):
        self.api_url = software_info["api_url"]
        self.authorization = software_info["authorization"]
        self.software_id = software_info["software_id"]

        pass

    def run(self):
        self.check_software()
        pass

    # 校验软件
    def check_software(self):
        print("校验软件")
        #  校验软件
        check_url = self.api_url + "v1/my_software/status"
        headers = {
            "authorization": self.authorization,
            "Content-Type": "application/json"
        }
        updata = {
            "id": self.software_id
        }

        data = bztt_requests.post(check_url, data=json.dumps(updata), headers=headers, timeout=3)
        
        status_code = data.status_code
        datastr = data.json()

        if status_code == 401:
            raise Exception("token校验失败")
        elif  status_code != 200:
            raise Exception("服务器异常")

        my_type = int(datastr["detail"]["type"])
        if my_type == 0:
            print("校验正常")
            return

        elif my_type == 1 or my_type == 2 or my_type == 4 or my_type == 6:  # 失败
            raise Exception(datastr["detail"]["msg"])

        elif my_type == 3:  # 可选更新
            # 读取配置文件
            while 1:
                flag = input("输入<y>进行更新，输入<n>暂时不更新")
                if flag == "y":
                    print("正在更新")
                    do_updata_json = {
                        "md5": datastr["detail"]["loc"][0]["md5"],
                        "file_jwt": datastr["detail"]["loc"][0]["file_jwt"],
                    }
                    self.do_updata(do_updata_json)
                elif flag == "n":
                    return

        elif my_type == 5:  # 可选更新
            print("正在更新")
            do_updata_json = {
                "md5": datastr["detail"]["loc"][0]["md5"],
                "file_jwt": datastr["detail"]["loc"][0]["file_jwt"],
            }
            self.do_updata(do_updata_json)

    # 执行更新
    def do_updata(self,do_updata_json):
        wed_md5 = do_updata_json["md5"]
        num = 0
        # 获取文件
        while 1:
            if num > 3:
                raise Exception("文件下载失败")

            a = self.get_new_app(do_updata_json["file_jwt"])
            if not a:
                time.sleep(1)
                print("1秒后，重新下载")
                num += 1
                continue

            # 校验文件
            check_software_md5_json = {
                "wed_md5": wed_md5,
                "file_name": a["file_name"]
            }

            if self.check_software_md5(check_software_md5_json):
                break
            else:
                print("文件校验失败，稍后重试", num)
                time.sleep(1)
            num += 1

        # 重新启动
        print("程序将3秒后重启...")
        self.WriteRestartCmd(a["file_name"])

    def check_software_md5(self,check_software_md5_json):
        wed_md5 = check_software_md5_json["wed_md5"]
        file_name = check_software_md5_json["file_name"]

        md5_hash = hashlib.md5()
        my_md5 = ""
        with open(file_name, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
            my_md5 = md5_hash.hexdigest()
        if wed_md5 == my_md5:
            return True
        else:
            return False

    def get_file_name(self,url, headers):
        filename = ''
        if 'Content-Disposition' in headers and headers['Content-Disposition']:
            disposition_split = headers['Content-Disposition'].split(';')
            if len(disposition_split) > 1:
                if disposition_split[1].strip().lower().startswith('filename='):
                    file_name = disposition_split[1].split('=')
                    if len(file_name) > 1:
                        filename = unquote(file_name[1])
        if not filename and os.path.basename(url):
            filename = os.path.basename(url).split("?")[0]
        if not filename:
            return time.time()
        return filename

    def get_new_app(self,file_jwt):
        version_new = "123"
        url = self.api_url + 'v1/file_info/download/' + file_jwt
        try:
            from tqdm import tqdm
            get_file = bztt_requests.get(url=url, stream=False, allow_redirects=False, timeout=10)

            file_size = float(get_file.headers['Content-Length'])
            file_name = self.get_file_name(url, get_file.headers)
            file_name = file_name.replace("\"", "")

            with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, ascii=True,
                      desc=file_name) as bar:  # 打印下载时的进度条，实时显示下载速度
                with bztt_requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_name, 'wb') as fp:
                        for chunk in r.iter_content(chunk_size=512):
                            if chunk:
                                fp.write(chunk)
                                bar.update(len(chunk))  # 实时更新已完成的数据量
            return {
                "file_name": file_name,
                "file_size": file_size
            }
        except Exception as e:
            print('【版本更新】网络错误' + str(e))
            return False

    # 编写bat脚本，删除旧程序，运行新程序
    def WriteRestartCmd(self,exe_name):
        b = open("upgrade.bat", 'w')
        TempList = "@echo off\n";  # 关闭bat脚本的输出
        TempList += "if not exist " + exe_name + " exit \n";  # 新文件不存在,退出脚本执行
        TempList += "choice /t 3 /d y /n >nul\n"  # 3秒后删除旧程序（3秒后程序已运行结束，不延时的话，会提示被占用，无法删除）
        TempList += "del \"" + os.path.realpath(sys.argv[0]) + "\"\n"  # 删除当前文件
        TempList += "start " + exe_name  # 启动新程序
        b.write(TempList)
        b.close()
        subprocess.Popen("upgrade.bat")
        sys.exit()  # 进行升级，退出此程序
