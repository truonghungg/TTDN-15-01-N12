[1mdiff --git a/README.md b/README.md[m
[1mindex 287a22a2..781241e3 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -41,6 +41,7 @@[m [mpip3 install -r requirements.txt[m
 [m
 Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.[m
 [m
[32m+[m[32mCREATE DATABASE hung;[m
 `sudo docker-compose up -d`[m
 [m
 # 3. Setup tham số chạy cho hệ thống[m
[36m@@ -70,4 +71,3 @@[m [mpython3 odoo-bin.py -c odoo.conf -u all[m
 Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.[m
 [m
 Hoàn tất[m
[31m-    [m
