import numpy as np
import matplotlib.pyplot as plt

# --- PARAMETRELER ---
K = 5                # Sunucu sayısı
STEPS = 2000         # Toplam istek (adım) sayısı
TAU = 0.3            # Softmax Sıcaklık Parametresi (Düşük = Sömürü, Yüksek = Keşif)
WALK_STD = 0.01      # Sunucu performanslarının ne kadar hızlı değişeceği (Gürültü)

class ServerCluster:
    def __init__(self, k):
        self.k = k
        # Her sunucunun başlangıçtaki gerçek gecikme süresi (rastgele 0.1s - 0.5s arası)
        self.real_latencies = np.random.uniform(0.1, 0.5, size=k)

    def get_latency(self, server_index):
        # Seçilen sunucunun o anki gecikmesini döndür + biraz rastgele gürültü ekle
        noise = np.random.normal(0, 0.01)
        latency = max(0.01, self.real_latencies[server_index] + noise)
        
        # NON-STATIONARY: Her adımda tüm sunucuların performansını biraz değiştir
        self.real_latencies += np.random.normal(0, WALK_STD, size=self.k)
        self.real_latencies = np.clip(self.real_latencies, 0.05, 1.0) # Gecikme 0.05-1s arası kalsın
        
        return latency

def softmax(q_values, tau):
    # Sayısal kararlılık için (overflow engellemek) değerlerden max çıkarılır
    exp_q = np.exp((q_values - np.max(q_values)) / tau)
    return exp_q / np.sum(exp_q)

# --- SİMÜLASYON ---

def simulate():
    cluster = ServerCluster(K)
    
    # Veri yapıları
    q_values = np.zeros(K)    # Sunucuların tahmini başarı puanları
    counts = np.zeros(K)      # Hangi sunucu kaç kez seçildi
    
    softmax_history = []      # Softmax gecikme kayıtları
    rr_history = []           # Round-Robin gecikme kayıtları
    
    # Karşılaştırma için aynı cluster yapısını kopyalayan bir yapı 
    rr_cluster = ServerCluster(K)
    rr_cluster.real_latencies = cluster.real_latencies.copy()

    for t in range(STEPS):
        # 1. SOFTMAX SEÇİMİ
        # Ödül olarak (1 / Latency) kullanıyoruz çünkü düşük gecikme = yüksek ödül
        probabilities = softmax(q_values, TAU)
        selected_server = np.random.choice(K, p=probabilities)
        
        # Gecikmeyi al ve ödülü hesapla
        latency = cluster.get_latency(selected_server)
        reward = 1.0 / latency # Ödül fonksiyonu
        
        # Q-değerini güncelle (Hareketli Ortalama - Non-stationary için önemlidir)
        alpha = 0.1 # Öğrenme oranı
        q_values[selected_server] += alpha * (reward - q_values[selected_server])
        softmax_history.append(latency)
        
        # 2. ROUND-ROBIN SEÇİMİ (Sırayla seçim)
        rr_server = t % K
        rr_latency = rr_cluster.get_latency(rr_server)
        rr_history.append(rr_latency)

    return softmax_history, rr_history

# --- GÖRSELLEŞTİRME ---

soft_h, rr_h = simulate()

# Kümülatif ortalama gecikmeyi hesapla (Grafiğin daha net görünmesi için)
soft_avg = np.cumsum(soft_h) / (np.arange(STEPS) + 1)
rr_avg = np.cumsum(rr_h) / (np.arange(STEPS) + 1)

plt.figure(figsize=(12, 6))
plt.plot(soft_avg, label=f'Softmax (tau={TAU})', color='blue', linewidth=2)
plt.plot(rr_avg, label='Round-Robin', color='red', linestyle='--', linewidth=2)
plt.title('Load Balancer Performansı: Softmax vs Round-Robin')
plt.xlabel('İstek Sayısı')
plt.ylabel('Ortalama Gecikme (Saniye)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
print("Simülasyon tamamlandı, grafik açılıyor...")
print(f"Softmax Final Ortalama Gecikme: {soft_avg[-1]:.4f}s")
print(f"Round-Robin Final Ortalama Gecikme: {rr_avg[-1]:.4f}s")
