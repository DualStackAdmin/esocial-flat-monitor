# 🏢 E-Social Flat Monitor (Azərbaycan)

Bu layihə, Azərbaycan Respublikası Əmək və Əhalinin Sosial Müdafiəsi Nazirliyinin (e-social.gov.az) mənzil portalında boş mənzilləri avtomatik izləmək və tapıldıqda anında Telegram vasitəsilə bildiriş göndərmək üçün hazırlanmış açıq mənbəli (open-source) Python skriptidir. 

Vətəndaşların günlərlə ekran qarşısında oturub səhifəni yeniləmək (F5) əziyyətini aradan qaldırmaq və prosesi avtomatlaşdırmaq məqsədi daşıyır.

---

## ⚠️ Diqqət: Qanuni və Etik İstifadə (Disclaimer)
**BU LAYİHƏ BİR "HACKING" VƏ YA KİBERHÜCUM ALƏTİ DEYİLDİR.** * Bu skript heç bir dövlət serverinə qeyri-qanuni müdaxilə etmir, məlumat bazalarını sındırmır və DDoS xarakterli sorğular göndərmir.
* Sistem sadəcə vətəndaşlara onsuz da açıq olan (Public) veb-səhifəni avtomatik olaraq ziyarət edir (Web Scraping / Browser Automation) və ekrandakı rəqəmləri oxuyur.
* Skript hər hansı bir istifadəçi məlumatını oğurlamır və ya kənar serverlərə ötürmür. 
* Layihə tədris və şəxsi rutini avtomatlaşdırmaq (Personal Automation) məqsədi ilə yazılmışdır. Saytın işinə xələl gətirəcək şəkildə (məsələn, saniyədə onlarla sorğu atmaq) aqressiv istifadəyə görə məsuliyyət istifadəçinin öz üzərinə düşür. Lütfən, skripti ağlabatan intervallarla (məsələn, 1-2 dəqiqədən bir) işlədin.

---

## 🛠️ İstifadə Olunan Texnologiyalar (Tech Stack)

Bu sistemin arxa planında resurslara maksimum qənaət edən və stabil işləyən müasir texnologiyalardan istifadə olunmuşdur:

* **Python (3.x):** Sistemin əsas proqramlaşdırma dili.
* **Selenium (Webdriver):** Veb səhifələrlə insan kimi qarşılıqlı əlaqə qurmaq, JavaScript ilə yüklənən dinamik məlumatları oxumaq üçün istifadə olunur. (Skript `Headless` rejimdə, yəni qrafik interfeys olmadan, arxa fonda çalışır).
* **Webdriver Manager:** Chrome brauzeri üçün uyğun drayverlərin (chromedriver) əl ilə deyil, sistem tərəfindən avtomatik tapılıb yüklənməsini təmin edir.
* **Telegram Bot API:** Mənzil tapıldığı an gecikmədən (real-time) istifadəçinin telefonuna bildirişlərin göndərilməsi üçün daxili `urllib` kitabxanası vasitəsilə API inteqrasiyası qurulub.
* **Linux Crontab & Flock:** Skriptin serverdə 7/24 dayanmadan, fasiləsiz işləməsi üçün `Crontab` istifadə edilir. Eyni anda iki skriptin işə düşüb serverin RAM-nı (yaddaşını) doldurmasının qarşısını almaq üçün isə Linux-un `flock` (File Lock) mexanizmindən istifadə olunmuşdur.

---

## 🚀 Özəllikləri (Features)

* **Çoxlu Layihə İzləmə:** Eyni anda həm Ramana, həm Kürdəxanı, həm də sistemə əlavə edəcəyiniz istənilən qədər layihəni növbə ilə yoxlaya bilir.
* **Aşağı Resurs İstehlakı (Low RAM Mode):** Brauzer işə düşərkən `GPU`, `Extensions` və lazımsız vizual elementlər bloklanır. İş bitdikdən dərhal sonra "Zombie" proseslərin qarşısını almaq üçün brauzer yaddaşdan silinir (`driver.quit()`).
* **Sıfır Gecikmə (Zero Downtime):** Şəbəkə xətası və ya saytın çökməsi halında skript dayanmır, xətanı loglara yazaraq növbəti dövrdə işinə qaldığı yerdən davam edir.
* **Ağıllı Bildiriş:** Yalnızca mənzil tapıldıqda sizi narahat edir. Boş yoxlamalar zamanı səssizcə işləyir.

---

## ⚙️ Qurulum və İstifadə (Installation)

### 1. Tələblərin Yüklənməsi
Sisteminizdə Python3 quraşdırıldığından əmin olduqdan sonra, repozitoriyanı klonlayın və kitabxanaları yükləyin:

```bash
git clone [https://github.com/DualStackAdmin/esocial-flat-monitor.git](https://github.com/DualStackAdmin/esocial-flat-monitor.git)
cd esocial-flat-monitor
pip install -r requirements.txt
2. Konfiqurasiya
monitor.py faylını istənilən redaktorla açın və şəxsi məlumatlarınızı əlavə edin:

Python
# Öz Telegram Bot Tokeninizi bura yazın (BotFather-dən alına bilər)
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"

# Mesajın gələcəyi Chat ID (öz ID-niz)
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
Layihə linklərini PROJECTS siyahısından dəyişdirə bilərsiniz. Boş evləri axtarmaq üçün linkin sonunda mütləq flatstatus=nonbooked olmalıdır.

3. Serverdə Avtomatik İşə Salma (Crontab)
Skripti Linux (Ubuntu/Debian/CentOS) serverinizdə arxa fonda daimi işlətmək üçün terminalda crontab -e yazın və ən alt sətrə bunu əlavə edin:

Bash
* * * * * /usr/bin/flock -n /home/ubuntu/monitor.lock /usr/bin/python3 /home/ubuntu/esocial-flat-monitor/monitor.py >> /home/ubuntu/monitor_cron.log 2>&1
(Qeyd: Fayl yollarını (/home/ubuntu/...) öz sisteminizə uyğun olaraq dəyişməyi unutmayın).

🤝 Töhfə Vermək (Contributing)
Layihəni inkişaf etdirmək, yeni xüsusiyyətlər əlavə etmək (məsələn: avtomatik login və bronlama modulu) istəyən hər kəs "Pull Request" göndərə bilər.

📄 Lisenziya
Bu layihə MIT License altında yayımlanır. Kodu istədiyiniz kimi kopyalaya, dəyişdirə və paylaya bilərsiniz.
