🚀 Adaptive Load Balancer Simulation
Softmax (Multi-Armed Bandit) vs Round-Robin

Bu proje, non-stationary (zamanla değişen) sunucu ortamında iki farklı load balancing yaklaşımını karşılaştırır:

🎯 Softmax (Multi-Armed Bandit)

🔄 Round-Robin

Amaç: Dinamik olarak değişen sunucu gecikmelerinde hangi yöntemin daha düşük ortalama latency ürettiğini gözlemlemek.

📌 Problem Tanımı

Gerçek sistemlerde sunucu performansı sabit değildir.

Trafik yoğunluğu değişir

Donanım yükü artar/azalır

Ağ gecikmesi dalgalanır

Bu projede her sunucunun gecikmesi zaman içinde küçük rastgele değişimlerle (random walk) evrimleşir.

Bu ortamda klasik Round-Robin ile, öğrenebilen bir yöntem olan Softmax Bandit karşılaştırılır.

🧠 Kullanılan Yöntemler
1️⃣ Softmax (Multi-Armed Bandit)

Softmax yöntemi her sunucu için bir Q-değeri (beklenen ödül) tutar.

Olasılık hesabı:

𝑃
(
𝑎
)
=
𝑒
𝑄
(
𝑎
)
/
𝜏
∑
𝑒
𝑄
(
𝑏
)
/
𝜏
P(a)=
∑e
Q(b)/τ
e
Q(a)/τ
	​


τ (tau) → sıcaklık parametresi

Küçük τ → daha fazla sömürü (en iyi bilinen sunucuya yönelme)

Büyük τ → daha fazla keşif

Ödül fonksiyonu:

𝑅
𝑒
𝑤
𝑎
𝑟
𝑑
=
1
𝐿
𝑎
𝑡
𝑒
𝑛
𝑐
𝑦
Reward=
Latency
1
	​


Çünkü düşük gecikme = yüksek performans.

2️⃣ Round-Robin

Sunucular sırayla seçilir

Öğrenme mekanizması yoktur

Her sunucuya eşit dağıtım yapar

⚙️ Simülasyon Özellikleri
Parametre	Açıklama
K = 5	Sunucu sayısı
STEPS = 2000	Toplam istek sayısı
TAU = 0.1	Softmax sıcaklık parametresi
WALK_STD = 0.01	Sunucu performans değişim hızı

Her adımda:

Seçilen sunucunun gecikmesi ölçülür

Tüm sunucuların gerçek gecikmesi küçük rastgele değişim geçirir

Latency aralığı: 0.05s – 1.0s

📊 Çıktı

Grafikte:

Mavi çizgi → Softmax ortalama gecikme

Kırmızı kesik çizgi → Round-Robin ortalama gecikme

Gösterilen değer:
Kümülatif Ortalama Gecikme

📈 Beklenen Sonuç

Non-stationary ortamda:

Softmax zamanla daha iyi sunucuları keşfeder

Performansı değişen sunuculara adapte olur

Genellikle Round-Robin'den daha düşük ortalama gecikme üretir

🛠️ Kurulum
pip install numpy matplotlib

▶️ Çalıştırma
python simulation.py

📚 Kavramsal Arka Plan

Bu proje şu alanlara dayanır:

Reinforcement Learning

Multi-Armed Bandit Problemi

Online Learning

Adaptive Systems

Load Balancing Algorithms

💡 Özet

Bu çalışma, klasik deterministik load balancing yaklaşımı ile öğrenebilen adaptif sistemleri karşılaştırarak:

"Statik sistemler mi, yoksa öğrenebilen sistemler mi daha verimli?"

sorusuna deneysel bir cevap sunar.
