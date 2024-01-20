function tekmiciftmi() {
    let tekbulunan = 0;
    let ciftbulunan = 0;

    let tekciftcontainer = document.createElement('div');
    tekciftcontainer.style.textAlign = "center";

    let yazi1 = "Tekleri Bul";
    let yazi2 = "Çiftleri Bul";

    let yazilar = [yazi1, yazi2];
    let rastgeleYazi = yazilar[Math.floor(Math.random() * yazilar.length)];

    let tekSayilar = [];
    let ciftSayilar = [];
    

    let tekleriBulText = document.createElement("h2");
    tekleriBulText.innerHTML = rastgeleYazi;
    tekciftcontainer.appendChild(tekleriBulText);

    for (let i = 1; i < 5; i++) {
        let br = document.createElement('br');
        document.body.appendChild(br);
    }

    for (let i = 0; i < 12; i++) {
        let tekciftbutton = document.createElement('div');
        tekciftbutton.style.width = "250px";
        tekciftbutton.style.backgroundColor = "#007bff";
        tekciftbutton.style.padding = "15px";
        tekciftbutton.style.color = "white";
        tekciftbutton.style.display = "inline-block";
        tekciftbutton.style.marginLeft = "5px";
        tekciftbutton.style.marginRight = "5px";
        tekciftbutton.style.marginTop = "10px";


        tekciftcontainer.appendChild(tekciftbutton);

        let randomNum = Math.floor(Math.random() * (999 - 100 + 1)) + 100;

        if (randomNum % 2 == 1) {
            tekSayilar.push(randomNum);
        }

        else if (randomNum % 2 == 0) {
            ciftSayilar.push(randomNum);
        }



        if ((i + 1) % 2 === 0) {
            tekciftbutton.innerText = randomNum;

            let lineBreak = document.createElement('br');
            tekciftcontainer.appendChild(lineBreak);
        } else {
            tekciftbutton.innerText = randomNum;
        }

        document.body.appendChild(tekciftcontainer)


        if (rastgeleYazi == yazi1) {
            tekciftbutton.addEventListener("click", function() {
                if (tekciftbutton.innerText % 2 == 1) {
                    tekbulunan = tekbulunan + 1;
                    tekciftbutton.style.backgroundColor = "green";

                    if (tekbulunan == tekSayilar.length) {
                       bitir();
                    }

                } else if (tekciftbutton.innerText % 2 == 0) {
                    tekciftbutton.style.backgroundColor = "red";
                }
            })
        }

        else if (rastgeleYazi == yazi2) {
            tekciftbutton.addEventListener("click", function() {
                if (tekciftbutton.innerText % 2 == 1) {
                    tekciftbutton.style.backgroundColor = "red";
                } else if (tekciftbutton.innerText % 2 == 0) {
                    ciftbulunan = ciftbulunan + 1;
                    tekciftbutton.style.backgroundColor = "green";

                    if (ciftbulunan == ciftSayilar.length) {
                        bitir();
                    }
                }
            })
        }

    }
}