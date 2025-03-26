#该镜像是基于nginx:latest镜像构建的
FROM nginx

#添加说明
MAINTAINER onesummer

#删除目录下的default.conf文件
RUN rm /etc/nginx/conf.d/default.conf

#将default.conf复制到/etc/nginx/conf.d/下，用本地的default.conf配置来替换nginx镜像里的默认配置
ADD default.conf /etc/nginx/conf.d/

#将项目根目录下dist文件夹（构建之后才会生成）下的所有文件复制到镜像/usr/share/nginx/html/目录下
COPY dist/ /usr/share/nginx/html/