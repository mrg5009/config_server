### راهنمای نصب و پیکربندی ابزار Knockd

این راهنما بهتون یاد می‌ده چطور ابزار **knockd** رو نصب و پیکربندی کنید تا باهاش سرویس SSH رو مدیریت کنید. با این ابزار می‌تونید با فرستادن یک سری از پورت‌ها (بهش می‌گن "دنباله پورت")، دسترسی به SSH روی پورت 22 رو باز یا بسته کنید.

---

#### 1. نصب knockd

برای نصب knockd، این دستورها رو تو ترمینال وارد کنید:

```bash
sudo apt update
sudo apt install knockd
```

---

#### 2. ویرایش فایل‌های پیکربندی

##### 2.1 تنظیم فایل `/etc/knockd.conf`

حالا برای ویرایش فایل پیکربندی knockd این دستور رو بزنید:

```bash
sudo nano /etc/knockd.conf
```

توی این فایل، این تنظیمات رو اضافه کنید یا تغییر بدید:

```bash
[openSSH]
    sequence    = 7000,8000,9000
    seq_timeout = 5
    command     = /sbin/iptables -I INPUT -p tcp --dport 22 -j ACCEPT
    tcpflags    = syn

[closeSSH]
    sequence    = 1300,1400,1500
    seq_timeout = 5
    command     = /sbin/iptables -I INPUT -p tcp --dport 22 -j DROP
    tcpflags    = syn
```

**توضیحات**:
- **openSSH**: با این دنباله پورت‌ها (7000, 8000, 9000) می‌تونید دسترسی به SSH رو باز کنید.
- **closeSSH**: این یکی هم برای بستن دسترسی به SSH با دنباله معکوسه (1500, 1400, 1300).

##### 2.2 تنظیم فایل `/etc/default/knockd`

برای اینکه knockd همیشه با روشن شدن سیستم شروع به کار کنه، فایل `/etc/default/knockd` رو ویرایش کنید:

```bash
sudo nano /etc/default/knockd
```

این خط رو پیدا کنید:

```bash
START_KNOCKD=0
```

و به این تغییرش بدید:

```bash
START_KNOCKD=1
```

---

#### 3. ری‌استارت کردن سرویس knockd

بعد از تغییرات، باید سرویس knockd رو ری‌استارت کنید تا تغییرات اعمال بشه:

```bash
sudo systemctl restart knockd
```

---

#### 4. استفاده از knockd برای مدیریت دسترسی به SSH

##### 4.1 ساخت فایل `knock_open.bat`

برای باز کردن SSH، یه فایل به نام `knock_open.bat` بسازید:

```bash
nano knock_open.bat
```

و این دستورات رو داخلش بذارید:

```bash
nmap -p 7000 --scanflags SYN <ip server>
nmap -p 8000 --scanflags SYN <ip server>
nmap -p 9000 --scanflags SYN <ip server>
```

بعد فایل رو ذخیره کنید و برای اجرا کردنش این دستور رو بزنید:

```bash
bash knock_open.bat
```

##### 4.2 ساخت فایل `knock_close.bat`

برای بستن SSH، یه فایل به نام `knock_close.bat` بسازید:

```bash
nano knock_close.bat
```

این دستورات رو توش قرار بدید:

```bash
nmap -p 1300 --scanflags SYN <ip server>
nmap -p 1400 --scanflags SYN <ip server>
nmap -p 1500 --scanflags SYN <ip server>
```

بعد از ذخیره، فایل رو با این دستور اجرا کنید:

```bash
bash knock_close.bat
```

---

### نکات آخر

1. نیاز نیست فایروال UFW رو فعال کنید، ولی اگه دوست داشتید، می‌تونید پورت‌های 7000، 8000 و 9000 رو تغییر بدید.
2. مطمئن بشید که `nmap` روی سیستمتون نصب شده. اگه نصب نیست، این دستور رو بزنید:

   ```bash
   sudo apt install nmap
   ```

---

این راهنما شما رو قدم به قدم با نصب و پیکربندی knockd برای مدیریت دسترسی SSH آشنا کرد.
