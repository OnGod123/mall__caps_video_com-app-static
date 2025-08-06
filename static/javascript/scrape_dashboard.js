async function runScrape(url) {
    document.getElementById("status").textContent = "Running " + url + "...";
    try {
        const res = await fetch(url, { credentials: "include" });
        const text = await res.text();
        document.getElementById("status").textContent = text || "Done!";
    } catch (err) {
        document.getElementById("status").textContent = "Error: " + err.message;
    }
}

document.getElementById("scrape_v01").addEventListener("click", () => {
    runScrape("/scrape/version_0_1_mini");
});

document.getElementById("scrape_v03").addEventListener("click", () => {
    runScrape("/scrape/version_0_3_mini");
});

