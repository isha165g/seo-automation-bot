async function analyzeWebsite() {
  const rawJson = document.getElementById("rawJson");
  rawJson.innerText = "Analyzing website...";

  const url = document.getElementById("url").value;
  const dynamic = document.getElementById("dynamic").checked;

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, dynamic })
    });

    const raw = await response.json();
    const data = JSON.parse(raw.output);  

    renderSummary(data.summary);
    console.log("Parsed pipeline JSON:", data);

    // Show JSON (debug-friendly)
    rawJson.innerText = JSON.stringify(data, null, 2);

    // Render summary cards
    if (data.summary) {
        renderSummary(data.summary);
        renderAISuggestions(data.ai_actions);
    } else {
        document.getElementById("summary").innerHTML =
            "<p style='color:red'>No SEO summary available</p>";
    }

  } catch (err) {
    rawJson.innerText = "Error: " + err.message;
  }
}

function renderSummary(summary) {
  if (!summary) return;

  const container = document.getElementById("summary");
  container.innerHTML = "";

  container.appendChild(
    createCard(
      "Meta Description",
      summary.meta_description === "present" ? "Present" : "Missing",
      summary.meta_description === "present"
    )
  );

  container.appendChild(
    createCard(
      "Title",
      summary.title === "ok" ? "SEO Friendly" : "Issues Found",
      summary.title === "ok"
    )
  );

  container.appendChild(
    createCard(
      "Images Missing Alt",
      summary.images_missing_alt ?? 0,
      (summary.images_missing_alt ?? 0) === 0
    )
  );
}

function createCard(title, value, isGood) {
  const card = document.createElement("div");
  card.style.padding = "16px";
  card.style.borderRadius = "8px";
  card.style.minWidth = "180px";
  card.style.background = isGood ? "#14532d" : "#7f1d1d";
  card.style.border = `2px solid ${isGood ? "#22c55e" : "#ef4444"}`;

  card.innerHTML = `
    <h3>${title}</h3>
    <p style="font-size:18px; font-weight:bold">${value}</p>
  `;

  return card;
}


function renderAISuggestions(ai) {
  const container = document.getElementById("aiSuggestions");
  container.innerHTML = "";

  // Meta Description
  container.appendChild(
    createSuggestionBlock(
      "Meta Description",
      ai.meta_description || "No change needed"
    )
  );

  // Title Rewrite
  container.appendChild(
    createSuggestionBlock(
      "Title Rewrite",
      ai.title || "No change needed"
    )
  );

  // Alt Text Suggestions
  const altTexts = ai.alt_texts || {};
  let altHtml = "";

  if (Object.keys(altTexts).length === 0) {
    altHtml = `<span>No alt text changes needed</span>`;
  } else {
    for (const idx in altTexts) {
      altHtml += `
        <div style="margin-bottom:6px;">
          <strong style="color:#facc15">Image ${idx}</strong>
          <span style="color:#e5e7eb"> → "${altTexts[idx]}"</span>
        </div>
      `;
    }
  }

  container.appendChild(
    createSuggestionBlock(
      "Image Alt Text Suggestions",
      altHtml
    )
  );
}

function createSuggestionBlock(title, value) {
  const div = document.createElement("div");

  div.style.padding = "14px";
  div.style.marginBottom = "14px";
  div.style.borderRadius = "8px";
  div.style.background = "#0f172a";
  div.style.border = "1px solid #475569";
  div.style.color = "#e5e7eb";

  div.innerHTML = `
    <div style="font-weight:bold; color:#38bdf8; margin-bottom:8px;">
      ${title}
    </div>
    <div>
      ${value}
    </div>
  `;

  return div;
}

