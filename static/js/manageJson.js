document.addEventListener("DOMContentLoaded", (event) => {
    let bullying = document.getElementById("bullying");
    if (bullying === null) {
        return;
    }
    bullying.onclick = (event) => {
        event.preventDefault();

        fetch("/worstPigeon", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((response) => response.json())
        .then((data) => {
            localStorage.setItem("pigeonData", JSON.stringify(data));
            window.location.href = '/worstPigeon';
        })
        .catch((error) => {
            console.error("Error:", error);
        });

        let pigeonData = JSON.parse(localStorage.getItem("pigeonData"));
        if (pigeonData) {
            document.getElementById("idPigeon").textContent = pigeonData.idPigeon;
            document.getElementById("prenomPigeon").textContent = pigeonData.prenomPigeon;
            document.getElementById("color").textContent = pigeonData.color;
            document.getElementById("place").textContent = pigeonData.place;
            document.getElementById("urlPhoto").textContent = pigeonData.urlPhoto;
            document.getElementById("moyenne").textContent = pigeonData.moyenne;
        } else {
            console.error("No pigeon found.");
        }
    };
});
