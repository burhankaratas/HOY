function bitir() {
    var blurDiv = document.createElement('div');
    blurDiv.style.position = 'fixed';
    blurDiv.style.top = '0';
    blurDiv.style.left = '0';
    blurDiv.style.width = '100%';
    blurDiv.style.height = '100%';
    blurDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';  // Arka plan rengi
    blurDiv.style.filter = 'blur(25px)';
    document.body.appendChild(blurDiv);

    var centeredDiv = document.createElement('div');
    centeredDiv.style.position = 'fixed';
    centeredDiv.style.top = '50%';
    centeredDiv.style.left = '50%';
    centeredDiv.style.transform = 'translate(-50%, -50%)';
    centeredDiv.style.width = '300px';
    centeredDiv.style.backgroundColor = '#48c0e8';
    centeredDiv.style.padding = '20px';
    centeredDiv.style.color = '#023706';
    centeredDiv.style.textAlign = 'center';

    centeredDiv.innerHTML = '<h3> Etkinlik Bitti </h3>';
    centeredDiv.appendChild(document.createElement('br'));

    var cancelBtn = document.createElement('button');
    cancelBtn.className = 'btn btn-primary';
    cancelBtn.style.float = "left";
    cancelBtn.innerHTML = 'İptal Et';
    cancelBtn.addEventListener('click', function() {
        document.body.removeChild(blurDiv);
        document.body.removeChild(centeredDiv);
    });
    centeredDiv.appendChild(cancelBtn);

    var confirmForm = document.createElement('form');
    confirmForm.method = 'post';
    var confirmBtn = document.createElement('button');
    confirmBtn.className = 'btn btn-success';
    confirmBtn.style.float = "right";
    confirmBtn.innerHTML = 'Onayla';
    confirmForm.appendChild(confirmBtn);
    centeredDiv.appendChild(confirmForm);

    document.body.appendChild(centeredDiv);
}