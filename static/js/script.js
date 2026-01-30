function fetchActions() {
  fetch("/api/actions")
    .then((response) => response.json())
    .then((data) => {
      const list = document.getElementById("action-list");
      list.innerHTML = "";

      if (data.length === 0) {
        list.innerHTML = "<p>No actions found yet.</p>";
        return;
      }

      data.forEach((item) => {
        const card = document.createElement("div");
        card.className = "action-card";

        let message = "";
        if (item.action === "PUSH") {
          message = `<b>${item.author}</b> pushed to "${item.to_branch}" on ${item.timestamp}`;
        } else if (item.action === "PULL_REQUEST") {
          message = `<b>${item.author}</b> submitted a pull request from "${item.from_branch}" to "${item.to_branch}" on ${item.timestamp}`;
        } else if (item.action === "MERGE") {
          message = `<b>${item.author}</b> merged branch "${item.from_branch}" to "${item.to_branch}" on ${item.timestamp}`;
        }

        card.innerHTML = `<p>${message}</p>`;
        list.appendChild(card);
      });
    })
    .catch((err) => console.error("Error fetching data:", err));
}

setInterval(fetchActions, 15000);
fetchActions();
