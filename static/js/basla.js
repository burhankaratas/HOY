function basla(callback) {
    var startDiv = document.createElement('div');
    startDiv.className = 'StartDiv';
    startDiv.style.width = '300px';
    startDiv.style.backgroundColor = '#3d12dc';
    startDiv.style.padding = '10px';
    startDiv.style.margin = 'auto';
    startDiv.style.marginTop = '150px';
    startDiv.style.color = 'white';
    startDiv.style.textAlign = 'center';
    startDiv.style.borderRadius = "10px"

    var baslikSpan = document.createElement('span');
    baslikSpan.id = 'baslikkk';
    baslikSpan.style.color = 'white';
    baslikSpan.style.textAlign = 'center';
    baslikSpan.style.fontWeight = '600';
    baslikSpan.style.fontSize = '20px';
    baslikSpan.innerHTML = 'Başlamaya Hazır Ol...';
    startDiv.appendChild(baslikSpan);

    var br2 = document.createElement('br');
    startDiv.appendChild(br2)

    var metinSpan = document.createElement('span');
    metinSpan.className = 'metincontent';
    metinSpan.style.color = 'white';
    metinSpan.innerHTML = 'Arkanıza yaslanın ve odaklanın';
    startDiv.appendChild(metinSpan);

    var br1 = document.createElement('br');
    startDiv.appendChild(br1)

    var timeoutSpan = document.createElement('span');
    timeoutSpan.className = 'timeout';
    timeoutSpan.style.color = 'white';
    startDiv.appendChild(timeoutSpan);

    document.body.appendChild(startDiv)

    for (let i = 5; i >= 0; i--) {
        setTimeout(() => {
            timeoutSpan.innerHTML = i;
            
            if (i == 0) {
                startDiv.style.display = "none";
                callback(); // Callback fonksiyonunu çağır
            }
        }, (5 - i) * 1000);
    }
}