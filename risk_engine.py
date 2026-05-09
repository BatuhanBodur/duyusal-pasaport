def calculate_risk(sound, light, touch, crowd, waiting):
    """
    Duyusal hassasiyet skorlarından genel risk seviyesi hesaplar.

    Değerler:
    1 = düşük hassasiyet
    5 = yüksek hassasiyet
    """

    score = (
        sound * 0.25 +
        light * 0.20 +
        touch * 0.20 +
        crowd * 0.20 +
        waiting * 0.15
    )

    if score < 2.4:
        return round(score, 2), "Düşük", "badge-low"

    if score < 3.7:
        return round(score, 2), "Orta", "badge-mid"

    return round(score, 2), "Yüksek", "badge-high"