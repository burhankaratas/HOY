function tekmiciftmi() {
    let tekciftcontainer = document.createElement('div');
    tekciftcontainer.style.textAlign = "center";

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

        if ((i + 1) % 2 === 0) {
            let lineBreak = document.createElement('br');
            tekciftcontainer.appendChild(lineBreak);
        }
    }
}