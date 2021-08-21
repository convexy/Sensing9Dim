window.addEventListener("load", function () {
    document.getElementById("greet").innerText = "Hello World!";
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "data/abc");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log(JSON.parse(xhr.responseText));
            document.getElementById("data").innerText = xhr.responseText;
        }
    };
    xhr.send(null);
});