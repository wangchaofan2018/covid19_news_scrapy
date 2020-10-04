# 此爬虫爬取不同地区政务网站发布的新冠疫情历史发布会,用于数据分析,用到的技术栈有 scrapy、selenium、mongodb

# 需要下载最新环境chromedriver
 sudo mv ~/Downloads/chromedriver /usr/bin

 vi ~/.bash_profile

 export PATH=$PATH:/usr/local/bin/ChromeDriver

# 下载mongodb
# 进入 /usr/local
cd /usr/local
# 下载
sudo curl -O https://fastdl.mongodb.org/osx/mongodb-osx-ssl-x86_64-4.0.9.tgz
# 解压
sudo tar -zxvf mongodb-osx-ssl-x86_64-4.0.9.tgz
# 重命名为 mongodb 目录
sudo mv mongodb-osx-x86_64-4.0.9/ mongodb
# 安装完成更新bash_profile
export PATH=/usr/local/mongodb/bin:$PATH
# 数据存放路径：
sudo mkdir -p /usr/local/var/mongodb
# 日志文件路径：
sudo mkdir -p /usr/local/var/log/mongodb
# 后台启动mongodb服务 启动之前记得更新配置 source ~/.bash_profile
mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork

# 安装 python包
pip3 install selenium
pip3 install scrapy
pip3 install xlwt