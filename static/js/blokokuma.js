function blokokuma(kelimeSayisi, yazi) {
    console.log("blokokuma is active")
    let containerDiv = document.createElement("div");
    containerDiv.classList.add("container");

    let rowDiv = document.createElement("div");
    rowDiv.classList.add("row");

    let colDiv = document.createElement("div");
    colDiv.classList.add("col-sm");
    colDiv.style.height = "600px";
    colDiv.style.width = "600px";
    colDiv.style.margin = "auto";
    colDiv.style.borderRadius = "20px";
    colDiv.style.textAlign = "center";
    colDiv.id = "yaziEkrani";

    for (let i = 0; i < 6; i++) {
        let brElement = document.createElement("br");
        colDiv.appendChild(brElement);
    }

    let spanElement = document.createElement("span");
    spanElement.style.fontSize = "50px";
    spanElement.style.padding = "20px";
    spanElement.style.backgroundColor = "black";
    spanElement.style.color = "white";
    spanElement.id = "yaziYer";

    colDiv.appendChild(spanElement);
    rowDiv.appendChild(colDiv);
    containerDiv.appendChild(rowDiv);
    document.body.appendChild(containerDiv);

    let yaziYer = document.querySelector("#yaziYer");

    let kelimeler = yazi.split(" ");

    for (let i = 0; i < kelimeler.length; i += parseInt(kelimeSayisi)) {
        setTimeout(() => {
            let yazi = kelimeler.slice(i, i + parseInt(kelimeSayisi)).join(" ");
            yaziYer.innerHTML = yazi;

            if (i + parseInt(kelimeSayisi) >= kelimeler.length) {
                setTimeout(() => {
                    yaziYer.innerHTML = "";
                    containerDiv.style.display = "none";
                }, 1500);
            }
        }, i / parseInt(kelimeSayisi) * 1500);
    }
}