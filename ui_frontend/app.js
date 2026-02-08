async function analyzeWebsite() {
  const rawJson = document.getElementById("rawJson");
  rawJson.innerText = "Analyzing website...";

  const url = document.getElementById("url").value;
  const dynamic = document.getElementById("dynamic").checked;

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, dynamic })
    });

    const data = await res.json();
    rawJson.innerText = JSON.stringify(data, null, 2);

    renderSummary(data.summary);
    renderAISuggestions(data.ai_actions, data.ai_insights);

    document.getElementById("originalHtml").innerText =
      data.original_html || "Not available";

    document.getElementById("modifiedHtml").innerText =
      data.modified_html || "No changes generated";

  } catch (err) {
    rawJson.innerText = "Error: " + err.message;
  }
}

function renderSummary(summary) {
  const container = document.getElementById("summary");
  container.innerHTML = "";

  container.appendChild(createCard(
    "Meta Description",
    summary.meta_description,
    summary.meta_description === "present"
  ));

  container.appendChild(createCard(
    "Title",
    summary.title,
    summary.title === "ok"
  ));

  container.appendChild(createCard(
    "Images Missing Alt",
    summary.images_missing_alt,
    summary.images_missing_alt === 0
  ));
}

function createCard(title, value, isGood) {
  const div = document.createElement("div");
  div.className = `card ${isGood ? "good" : "bad"}`;
  div.innerHTML = `<h3>${title}</h3><p><b>${value}</b></p>`;
  return div;
}

function renderAISuggestions(ai, insightText) {
  const container = document.getElementById("aiSuggestions");
  container.innerHTML = "";

  container.innerHTML += `
    <div style="
        background:#020617;
        border-left:4px solid #38bdf8;
        padding:12px;
        margin-bottom:12px;
        border-radius:6px;
    ">
        <p>🧠 <b>AI Insight:</b></p>
        <p>${insightText || "No insights generated."}</p>
    </div>
    `;

  container.innerHTML += `<p><b>Meta Description:</b> ${ai.meta_description || "—"}</p>`;
  container.innerHTML += `<p><b>Title:</b> ${ai.title || "—"}</p>`;

  const alts = ai.alt_texts || {};
  if (Object.keys(alts).length === 0) {
    container.innerHTML += `<p><b>Alt Text:</b> No changes</p>`;
  } else {
    container.innerHTML += `<p><b>Alt Text Suggestions:</b></p>`;
    for (const k in alts) {
      container.innerHTML += `<p>Image ${k}: ${alts[k]}</p>`;
    }
  }
}

function copyModified() {
  const text = document.getElementById("modifiedHtml").innerText;
  navigator.clipboard.writeText(text);
  alert("Modified HTML copied to clipboard!");
}

function approve() {
  alert("Changes approved. You can now deploy or save the HTML.");
}

function reject() {
  alert("Changes rejected. Original HTML remains unchanged.");
}
