def generate_recommendations(
    sound,
    light,
    touch,
    crowd,
    waiting,
    triggers,
    calming_methods
):
    """
    Duyusal profile göre hastane personeli için öneriler üretir.
    """

    recommendations = []

    if sound >= 4:
        recommendations.append("Sessiz bekleme alanına yönlendirme yapılmalıdır.")
        recommendations.append("Yüksek sesli anons ve ani ses uyaranları azaltılmalıdır.")

    if light >= 4:
        recommendations.append("Loş veya kontrollü ışıklı alan tercih edilmelidir.")
        recommendations.append("Parlak floresan ışıkların yoğun olduğu alanlardan kaçınılmalıdır.")

    if touch >= 4:
        recommendations.append("Fiziksel temas öncesinde bireye kısa ve net açıklama yapılmalıdır.")
        recommendations.append("Ani temaslardan kaçınılmalı, hazırlık süresi verilmelidir.")

    if crowd >= 4:
        recommendations.append("Kalabalık bekleme salonu yerine sakin bir alana alınmalıdır.")
        recommendations.append("Gereksiz insan yoğunluğu azaltılmalıdır.")

    if waiting >= 4:
        recommendations.append("Bekleme süresi mümkün olduğunca kısaltılmalıdır.")
        recommendations.append("Öncelikli sıra veya hızlı yönlendirme uygulanmalıdır.")

    if "İğne / kan alma" in triggers:
        recommendations.append("İğne veya kan alma işleminden önce sakin bir dille açıklama yapılmalıdır.")

    if "Yüksek ses" in triggers:
        recommendations.append("Kulaklık veya ses azaltıcı ekipman kullanımına izin verilmelidir.")

    if "Kalabalık ortam" in triggers:
        recommendations.append("Giriş ve bekleme süreci daha sakin alanlarda yönetilmelidir.")

    if "Ani temas" in triggers:
        recommendations.append("Ani fiziksel temas kesinlikle önlenmelidir.")

    if "Beyaz önlük" in triggers:
        recommendations.append("Personel yaklaşımı yumuşak olmalı, beyaz önlük kaynaklı kaygı azaltılmalıdır.")

    if "Veli yanında olmalı" in calming_methods:
        recommendations.append("Veli veya refakatçi süreç boyunca mümkün olduğunca yanında tutulmalıdır.")

    if "Tablet / görsel destek" in calming_methods:
        recommendations.append("Görsel destek veya dikkat dağıtıcı rahatlatıcı araçlar kullanılabilir.")

    if "Kısa açıklama yapılmalı" in calming_methods:
        recommendations.append("Tüm işlem adımları kısa, net ve sakin şekilde anlatılmalıdır.")

    if "Bekleme süresi azaltılmalı" in calming_methods:
        recommendations.append("Randevu ve sıra süreci beklemeyi azaltacak şekilde planlanmalıdır.")

    if "Loş ışık tercih edilmeli" in calming_methods:
        recommendations.append("Işık seviyesi daha düşük ve kontrollü bir alan tercih edilmelidir.")

    if not recommendations:
        recommendations.append(
            "Standart süreç uygulanabilir; yine de bireyin anlık tepkileri gözlemlenmelidir."
        )

    # Tekrar eden önerileri temizler.
    return list(dict.fromkeys(recommendations))