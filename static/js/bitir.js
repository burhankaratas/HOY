function bitir() {
    for (let i = 0; i <= 5; i++) {
        var br = document.createElement("br");
        document.body.appendChild(br);
    }
    var centeredDiv = document.createElement('div');
    centeredDiv.style.width = "300px";
    centeredDiv.style.backgroundColor = "#48c0e8";
    centeredDiv.style.margin = "auto";
    centeredDiv.style.padding = "20px";
    centeredDiv.style.color = "#023706";

    var textDiv = document.createElement('div');
    textDiv.style.textAlign = "center";
    textDiv.innerHTML = '<h3> Etkinlik Bitti </h3>';

    var leftButtonSpan = document.createElement('span');
    leftButtonSpan.style.float = "left";
    leftButtonSpan.innerHTML = '<a href="/dashboard">  <button class="btn btn-primary"> İptal Et </button> </a>';

    var rightButtonSpan = document.createElement('span');
    rightButtonSpan.style.float = "right";
    rightButtonSpan.innerHTML = '<form method="post"><button class="btn btn-success"> Onayla </button></form>';

    centeredDiv.appendChild(textDiv);
    centeredDiv.appendChild(document.createElement('br'));
    centeredDiv.appendChild(leftButtonSpan);
    centeredDiv.appendChild(rightButtonSpan);
    centeredDiv.appendChild(document.createElement('br'));

    document.body.appendChild(centeredDiv);
}