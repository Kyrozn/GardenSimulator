let errorPopup = document.createElement("div");
errorPopup.style.position = "fixed";
errorPopup.style.bottom = "0";
errorPopup.style.left = "50%";
errorPopup.style.transform = "translateX(-50%)";
errorPopup.style.padding = "10px";
errorPopup.style.border = "1px solid #f5c6cb";
errorPopup.style.borderRadius = "5px";
errorPopup.style.zIndex = "1000";
function showPopup(message, isError = false) {
  errorPopup.style.backgroundColor = isError ? "#f8d7da" : "#d4edda";
  errorPopup.style.color = isError ? "#721c24" : "#155724";
  errorPopup.innerText = message;
  document.body.appendChild(errorPopup);
  setTimeout(() => {
    errorPopup.remove();
  }, 3000);
}

function updateGame() {
  fetch("/update", {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      let garden = document.querySelector(".garden");
      let GameStats = document.querySelector("#GameStats");
      Plants = data.GameStats.plants;
      if (!data.GameStats.isNewGame) {
        console.log(data);
        garden.innerHTML = "";
        for (let i = 0; i < Object.keys(Plants).length; i++) {
          let plantHTML = `<div id="plot" class="plot" onclick="plant(this, ${
            i + 1
          })" data-plot-id="${i + 1}">
                        <div class="status"><h4>Plant : ${
                          Plants
                            ? Plants[i + 1]?.type ?? "No Seeds Planted"
                            : "No Seeds Planted"
                        }</h4>
                <h5>Water : ${Plants ? Plants[i + 1]?.myWatering ?? 0 : 0}/${
            Plants ? Plants[i + 1]?.waterRequired[1] ?? 0 : 0
          } L</h5>
                <h5>Fertilizer : ${
                  Plants ? Plants[i + 1]?.myfertilizer ?? 0 : 0
                }/${
            Plants ? Plants[i + 1]?.fertilizerRequired[1] ?? 0 : 0
          } g</h5>
                <h5>Light : ${Plants[i + 1]?.lightRequired[0]} - ${
            Plants[i + 1]?.lightRequired[1]
          } </h5>
                <h5>Health : ${Plants ? Plants[i + 1]?.Life ?? 0 : 0}</h5></div>
                        <p>${
                          Plants[i + 1] != null ? Plants[i + 1]?.icon : ""
                        }</p>
                    </div>`;
          garden.innerHTML += plantHTML;
        }
        GameStats.innerHTML = "";
        newStats = `<h6>Day: ${data.GameStats.day}</h6>
        <h6>Money: ${data.GameStats.MyMoney}$</h6>
        <h6>Light Status: ${data.GameStats.light}${
          data.GameStats.light >= 5000 ? "☀️" : "☁️"
        }<h6>
                <button onclick="BuyWater()"><h6>Enable Water: ${
                  data.GameStats.MyWater
                }L</h6></button>
                <button onclick="BuyFertilizer()"><h6>Enable Fertilizer: ${
                  data.GameStats.MyFertilizer
                }g</h6></button>
                <h6>Event of the day: ${
                  data.GameStats.event == null
                    ? "Nothing Special"
                    : data.GameStats.event
                }</h6>`;
        GameStats.innerHTML = newStats;
      } else {
        garden.innerHTML = `<div id="plot" class="plot" onclick="plant(this, 1) data-plot-id="1">
                  <div class="status"><h4>Status : No Seeds Planted</h4>
                <h5>Water : 0</h5>
                <h5>Fertilizer : 0</h5>
                <h5>Light : 0</h5>
                <h5>Health : 0</h5></div>
                <p></p>
                </div>`;
      }
    });
}
function AddPlot() {
  fetch("/SpendMoney", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "plot" }),
  })
    .then((response) => response.json())
    .then((data) => {
      updateGame();
    });
}
function BuyWater() {
  fetch("/SpendMoney", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "water" }),
  })
    .then((response) => response.json())
    .then((data) => {
      updateGame();
    });
}
function BuyFertilizer() {
  fetch("/SpendMoney", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "fertilizer" }),
  })
    .then((response) => response.json())
    .then((data) => {
      updateGame();
    });
}
document.addEventListener("DOMContentLoaded", () => {
  let draggedItem = null;

  // 🎯 Événement pour démarrer le drag
  document.querySelectorAll(".draggable-item").forEach((item) => {
    item.addEventListener("dragstart", (e) => {
      draggedItem = e.target;
      e.dataTransfer.setData("text/plain", draggedItem.dataset.itemId);
    });
  });

  // 🎯 Événements pour les plots (zones de drop)
  document.querySelector(".garden").addEventListener("dragover", (e) => {
    e.preventDefault();
  });

  document.querySelector(".garden").addEventListener("drop", (e) => {
    e.preventDefault();
    let plot = e.target.closest(".plot");
    if (plot && draggedItem) {
      let plotId = plot.dataset.plotId;
      let itemName = draggedItem.dataset.itemId;

      console.log("info : ", plotId, itemName);
      if (
        itemName == "tomato" ||
        itemName == "apple" ||
        itemName == "watermelon"
      ) {
        fetch("/plant", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ plotId: plotId, plantType: itemName }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.isError) {
              showPopup(data.text, true);
            } else {
              showPopup(data.text, false);
            }
            updateGame(); // Mise à jour du jardin
          });

        draggedItem = null; // Reset de l'item
      } else {
        let plotId = plot.dataset.plotId; // Récupè re l'ID de la parcelle sélectionnée
        let amount = 0;
        let action = draggedItem.dataset.itemId;
        if (action === "water") {
          amount = parseFloat(document.getElementById("waterAmount").value);
        } else if (action === "fertilizer") {
          amount = parseFloat(
            document.getElementById("fertilizerAmount").value
          );
        }

        fetch("/action", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ plotId, action, amount }),
        })
          .then((response) => response.json())
          .then((data) => {
            showPopup(data.text, false);
            updateGame();
          })
          .catch((error) => console.error("Erreur:", error));
      }
    }
  });
});
function nextDay() {
  fetch("/nextDay", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      showPopup(data.text, false);
      updateGame();
    })
    .catch((error) => console.error("Erreur:", error));
}
function SaveGame() {
  fetch("/Save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ SaveName: "save" }),
  })
    .then((response) => response.json())
    .then((data) => {
      showPopup(data.text, false);
      updateGame();
    })
    .catch((error) => console.error("Erreur:", error));
}
function OpenSave() {
  fetch("/openSave", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ SaveName: "save" }),
  })
    .then((response) => response.json())
    .then((data) => {
      showPopup(data.text, false);
      updateGame();
    })
    .catch((error) => console.error("Erreur:", error));
}
window.onload = (event) => {
  console.log("?");
  updateGame();
};
