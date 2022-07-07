# AUTO FUCK NCO ZJGSU

浙江工商大学 云战役 自动报送 Github版

fork自https://github.com/Hukeqing/FANZ
## 2022/6/5
学校甚至上AES了。。。

## 2022/5/27
- 【悲报】腾讯云上的云函数开始收费了，阿里云访问公网流出流量会计费。以防万一还是留Gayhub了。
- 学校新增了post的校验，已经跟着hkq更新了（大佬nb）。一共两项，一个是map了当前时间（这都能摸出来），一个和用户名、时间和一段固定字符串有关（看起来这玩意儿会被定期换掉）

## 2022/5/5 新签到来了，hkq更新了，那我这边也更新了
注意，新老版本的json格式不一样，其他都还是一样的。

新版本上线之后，我虽然有去抓包，然而又是只允许微信端登录又是要求定位的，还没法直接账号密码签到。

折腾半天看了下hkq的项目，原来早更新了，而且还是靠我的商大登录获取入口。。。

打死不下APP付出了血的教训。

再次感谢hkq没弃坑，懒人还有救（


魔改自[FUCK NCO ZJGSU](https://github.com/Hukeqing/FUCK-NCO-ZJGSU)。利用Github的Actions，让你不用准备任何东西，只需要白嫖微软的服务器，就能实现每天自动签到。

默认设置凌晨十二点半卡一次。不过因为Gayhub的机制，只能准时排队运行程序，所以实际运行时间往往会晚于预定时间。

## 使用方法

1. 点右上角Fork本项目。

2. 准备：

     进入项目的设置，添加所需信息：
     - Settings -> Secrets -> New reponsitory secret
     - Name: users
     - Value(example):
        ````Json
        [
            {
                "username": "your_student_num",
                "password": "your_password"
            },
            {
                "username": "your_student_num",
                "password": "your_password"
            }
        ]
        ````
     注意，密码是我的商大的登录密码。
     
     此外，还需要给一个[token](https://github.com/settings/tokens)。原则上给一个`workflow`权限就可以了。`secret`名叫`alive`。
     
     由于workflow会需要60天手动续一次，这里加一个每次签到前先续杯的模块。

     记得更改[keep_alive.py](keep_alive.py)，以实现每次签到自动续杯
     ````
     url = 'https://api.github.com/repos/你的用户名/AFANZ/actions/workflows/main.yml/enable'
     ````
     
     单独的续杯可以看[FC-Workflow-Keep-Alive](https://github.com/yujianke100/FC-Workflow-Keep-Alive)
     

3. 进入Actions，允许运行

4. 测试：进Action，选择左侧的Auto_Fuck_Nco_ZJGSU，能在右侧看到Run workflow

## ~~本体不是我写的，出问题别打我，传送门再给你一次，打[hkq](https://github.com/Hukeqing/FUCK-NCO-ZJGSU)去。~~


