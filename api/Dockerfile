# 镜像基于python3.9版本
FROM python:3.9 
  
# 复制 api 目录到容器的 /app 目录  
COPY . /app  
  
# 设置工作目录为 /app  
WORKDIR /app  
  
# 从清华源安装依赖  
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 设置中国时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
  
# 暴露端口  
EXPOSE 80  
  
# 设置容器启动时执行的命令  
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]