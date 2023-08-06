bztt_checkSoftware
==============
校验软件


使用方法
```
from bztt_checkSoftware import checkSoftware

SOFTWARE_INFO = {
        "api_url" : "http:*******/",        # api地址
        "authorization" : "",   # token
        "software_id" : "",     # 软件编号
    }

my_checkSoftware = checkSoftware(SOFTWARE_INFO)
my_checkSoftware.run()

```


# 更新记录
# 变动类型说明
Added 新添加的功能。 [新增]

Changed 对现有功能的变更。 [修改]

Deprecated 已经不建议使用，准备很快移除的功能。 [荒废]

Removed 已经移除的功能。  [移除]

Fixed 对bug的修复 [修复]

Security 对安全的改进  [安全]

---
# [0.0.1] - 2022-05-11
## 新增
- 首次提交
