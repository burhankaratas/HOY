function calistirSiraIle(etkinlikler) {
    var indeks = 0;

    function calistir() {
        if (indeks < etkinlikler.length) {
            var etkinlik = etkinlikler[indeks];
            etkinlik.fonksiyon(etkinlik.kelimeSayisi, etkinlik.yazi);

            var sure;

            if (etkinlik.fonksiyon == arabekle) {
                sure = etkinlik.sure;
            } else if (etkinlik.fonksiyon == blokokuma) {
                sure = etkinlik.sure * etkinlik.kelimeSayisi;
            }

            setTimeout(function () {
                indeks++;
                calistir();
            }, sure);
        }
    }

    calistir();
}