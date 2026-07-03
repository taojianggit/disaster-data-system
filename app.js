/* Disabled legacy static sample dataset.
const disasterRecords = [
  {
    disaster_type: "洪涝",
    start_time: "2026-06-17",
    location: "广东省梅州市平远县",
    affected_population: 386200,
    collapsed_houses: 1820,
    crop_affected_area: 53100,
    direct_economic_loss: 3650000000,
    damage_description: "连续强降雨引发山洪、城乡内涝和道路中断，部分村镇供电通信受影响。"
  },
  {
    disaster_type: "地震",
    start_time: "2025-01-07",
    location: "西藏自治区日喀则市定日县",
    affected_population: 61500,
    collapsed_houses: 3600,
    crop_affected_area: 420,
    direct_economic_loss: 890000000,
    damage_description: "地震造成部分农房倒损，交通、电力和通信设施受损，群众紧急转移安置。"
  },
  {
    disaster_type: "地质灾害",
    start_time: "2025-07-22",
    location: "四川省甘孜藏族自治州泸定县",
    affected_population: 18400,
    collapsed_houses: 240,
    crop_affected_area: 1260,
    direct_economic_loss: 126000000,
    damage_description: "强降雨诱发滑坡和泥石流，山区道路受阻，部分房屋和农田受损。"
  },
  {
    disaster_type: "洪涝",
    start_time: "2024-07-01",
    location: "湖南省岳阳市平江县",
    affected_population: 812000,
    collapsed_houses: 2230,
    crop_affected_area: 96500,
    direct_economic_loss: 5170000000,
    damage_description: "暴雨洪涝造成城区积水、河流水位上涨，农作物受灾面积较大。"
  },
  {
    disaster_type: "地震",
    start_time: "2023-12-18",
    location: "甘肃省临夏回族自治州积石山县",
    affected_population: 148700,
    collapsed_houses: 15000,
    crop_affected_area: 880,
    direct_economic_loss: 1300000000,
    damage_description: "地震造成大量房屋不同程度损坏，基础设施受损，灾区开展过渡安置。"
  },
  {
    disaster_type: "地质灾害",
    start_time: "2024-04-12",
    location: "云南省昭通市镇雄县",
    affected_population: 9200,
    collapsed_houses: 118,
    crop_affected_area: 510,
    direct_economic_loss: 67000000,
    damage_description: "边坡失稳导致滑坡，影响周边住户、乡村道路和局部农田。"
  },
  {
    disaster_type: "洪涝",
    start_time: "2023-08-01",
    location: "河北省保定市涿州市",
    affected_population: 1340000,
    collapsed_houses: 9200,
    crop_affected_area: 221000,
    direct_economic_loss: 10890000000,
    damage_description: "极端降雨和上游来水叠加，造成城乡内涝、人员转移和基础设施损毁。"
  },
  {
    disaster_type: "地质灾害",
    start_time: "2022-06-08",
    location: "贵州省毕节市织金县",
    affected_population: 27300,
    collapsed_houses: 360,
    crop_affected_area: 3400,
    direct_economic_loss: 218000000,
    damage_description: "持续降雨诱发崩塌、滑坡和泥石流，造成房屋、道路、水利设施受损。"
  },
  {
    disaster_type: "洪涝",
    start_time: "2021-07-20",
    location: "河南省郑州市",
    affected_population: 14500000,
    collapsed_houses: 89000,
    crop_affected_area: 872000,
    direct_economic_loss: 120060000000,
    damage_description: "特大暴雨引发严重城市内涝和河流洪水，交通、通信、市政设施受严重影响。"
  },
  {
    disaster_type: "地震",
    start_time: "2022-09-05",
    location: "四川省甘孜藏族自治州泸定县",
    affected_population: 117000,
    collapsed_houses: 5400,
    crop_affected_area: 2100,
    direct_economic_loss: 1540000000,
    damage_description: "地震造成房屋倒损、道路塌方和次生地质灾害风险，开展人员搜救和安置。"
  },
  {
    disaster_type: "洪涝",
    start_time: "2024-06-24",
    location: "广西壮族自治区桂林市",
    affected_population: 412000,
    collapsed_houses: 760,
    crop_affected_area: 64200,
    direct_economic_loss: 2110000000,
    damage_description: "强降雨导致漓江水位上涨、城区低洼区域积水，农业和旅游设施受影响。"
  },
  {
    disaster_type: "地质灾害",
    start_time: "2023-09-18",
    location: "重庆市巫山县",
    affected_population: 15600,
    collapsed_houses: 92,
    crop_affected_area: 1370,
    direct_economic_loss: 83000000,
    damage_description: "库区局地强降雨诱发滑坡险情，部分群众转移避险，乡村道路短时中断。"
  }
];

const csvFields = [
  "disaster_type",
  "start_time",
  "location",
  "affected_population",
  "collapsed_houses",
  "crop_affected_area",
  "direct_economic_loss",
  "damage_description"
];

let currentRows = [...disasterRecords];

const elements = {
  form: document.querySelector("#queryForm"),
  resetButton: document.querySelector("#resetButton"),
  downloadButton: document.querySelector("#downloadButton"),
  tableBody: document.querySelector("#tableBody"),
  emptyState: document.querySelector("#emptyState"),
  totalRecords: document.querySelector("#totalRecords"),
  resultCount: document.querySelector("#resultCount"),
  affectedTotal: document.querySelector("#affectedTotal"),
  houseTotal: document.querySelector("#houseTotal"),
  lossTotal: document.querySelector("#lossTotal"),
  filterState: document.querySelector("#filterState"),
  disasterType: document.querySelector("#disasterType"),
  startDate: document.querySelector("#startDate"),
  endDate: document.querySelector("#endDate"),
  locationKeyword: document.querySelector("#locationKeyword"),
  minAffected: document.querySelector("#minAffected"),
  minLoss: document.querySelector("#minLoss"),
  descriptionKeyword: document.querySelector("#descriptionKeyword")
};

function formatInteger(value) {
  return Number(value || 0).toLocaleString("zh-CN");
}

function formatCurrency(value) {
  const amount = Number(value || 0);

  if (amount >= 100000000) {
    return `${(amount / 100000000).toLocaleString("zh-CN", { maximumFractionDigits: 2 })} 亿元`;
  }

  if (amount >= 10000) {
    return `${(amount / 10000).toLocaleString("zh-CN", { maximumFractionDigits: 2 })} 万元`;
  }

  return `${amount.toLocaleString("zh-CN")} 元`;
}

function getFilters() {
  return {
    disasterType: elements.disasterType.value.trim(),
    startDate: elements.startDate.value,
    endDate: elements.endDate.value,
    locationKeyword: elements.locationKeyword.value.trim(),
    minAffected: elements.minAffected.value ? Number(elements.minAffected.value) : null,
    minLoss: elements.minLoss.value ? Number(elements.minLoss.value) : null,
    descriptionKeyword: elements.descriptionKeyword.value.trim()
  };
}

function applyFilters() {
  const filters = getFilters();
  currentRows = disasterRecords.filter((record) => {
    const matchesType = !filters.disasterType || record.disaster_type === filters.disasterType;
    const matchesStart = !filters.startDate || record.start_time >= filters.startDate;
    const matchesEnd = !filters.endDate || record.start_time <= filters.endDate;
    const matchesLocation = !filters.locationKeyword || record.location.includes(filters.locationKeyword);
    const matchesAffected = filters.minAffected === null || record.affected_population >= filters.minAffected;
    const matchesLoss = filters.minLoss === null || record.direct_economic_loss >= filters.minLoss;
    const matchesDescription =
      !filters.descriptionKeyword || record.damage_description.includes(filters.descriptionKeyword);

    return (
      matchesType &&
      matchesStart &&
      matchesEnd &&
      matchesLocation &&
      matchesAffected &&
      matchesLoss &&
      matchesDescription
    );
  });

  render();
}

function render() {
  renderTable();
  renderSummary();
}

function renderTable() {
  elements.tableBody.innerHTML = "";

  for (const record of currentRows) {
    const row = document.createElement("tr");
    const typeClass = getTypeClass(record.disaster_type);

    row.innerHTML = `
      <td><span class="type-pill ${typeClass}">${record.disaster_type}</span></td>
      <td class="number">${record.start_time}</td>
      <td>${record.location}</td>
      <td class="number">${formatInteger(record.affected_population)}</td>
      <td class="number">${formatInteger(record.collapsed_houses)}</td>
      <td class="number">${formatInteger(record.crop_affected_area)} 公顷</td>
      <td class="number">${formatCurrency(record.direct_economic_loss)}</td>
      <td class="description">${record.damage_description}</td>
    `;

    elements.tableBody.appendChild(row);
  }

  elements.emptyState.hidden = currentRows.length > 0;
  elements.downloadButton.disabled = currentRows.length === 0;
  elements.filterState.textContent = currentRows.length === disasterRecords.length ? "全部记录" : "已筛选";
}

function renderSummary() {
  const totals = currentRows.reduce(
    (sum, record) => {
      sum.affected += Number(record.affected_population || 0);
      sum.houses += Number(record.collapsed_houses || 0);
      sum.loss += Number(record.direct_economic_loss || 0);
      return sum;
    },
    { affected: 0, houses: 0, loss: 0 }
  );

  elements.totalRecords.textContent = `${disasterRecords.length} 条`;
  elements.resultCount.textContent = formatInteger(currentRows.length);
  elements.affectedTotal.textContent = formatInteger(totals.affected);
  elements.houseTotal.textContent = formatInteger(totals.houses);
  elements.lossTotal.textContent = formatCurrency(totals.loss);
}

function getTypeClass(type) {
  if (type === "地震") return "earthquake";
  if (type === "地质灾害") return "geology";
  return "";
}

function downloadCsv() {
  const csv = toCsv(currentRows);
  const blob = new Blob([`\uFEFF${csv}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const date = new Date().toISOString().slice(0, 10);
  const link = document.createElement("a");

  link.href = url;
  link.download = `disaster_records_${date}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function toCsv(rows) {
  const header = csvFields.join(",");
  const body = rows.map((row) => csvFields.map((field) => escapeCsv(row[field])).join(","));
  return [header, ...body].join("\r\n");
}

function escapeCsv(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return `"${text.replace(/"/g, '""')}"`;
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  applyFilters();
});

elements.resetButton.addEventListener("click", () => {
  elements.form.reset();
  currentRows = [...disasterRecords];
  render();
});

elements.downloadButton.addEventListener("click", downloadCsv);

render();
*/

let disasterRecords = [];
let currentRows = [];
let sourceErrors = [];
let sourceNotes = [];

const csvFields = [
  "disaster_type",
  "start_time",
  "location",
  "affected_population",
  "deaths_missing",
  "emergency_relocated",
  "collapsed_houses",
  "crop_affected_area",
  "direct_economic_loss",
  "damage_description",
  "source_name",
  "source_url"
];

const csvHeaders = {
  disaster_type: "灾害类型",
  start_time: "发生时间",
  location: "发生地点",
  affected_population: "受灾人口",
  deaths_missing: "死亡失踪",
  emergency_relocated: "紧急转移/救助",
  collapsed_houses: "倒塌房屋",
  crop_affected_area: "农作物受灾面积",
  direct_economic_loss: "直接经济损失",
  damage_description: "灾情描述",
  source_name: "数据来源",
  source_url: "来源链接"
};

const elements = {
  form: document.querySelector("#queryForm"),
  resetButton: document.querySelector("#resetButton"),
  refreshButton: document.querySelector("#refreshButton"),
  downloadButton: document.querySelector("#downloadButton"),
  tableBody: document.querySelector("#tableBody"),
  emptyState: document.querySelector("#emptyState"),
  totalRecords: document.querySelector("#totalRecords"),
  resultCount: document.querySelector("#resultCount"),
  affectedTotal: document.querySelector("#affectedTotal"),
  deathsTotal: document.querySelector("#deathsTotal"),
  relocatedTotal: document.querySelector("#relocatedTotal"),
  houseTotal: document.querySelector("#houseTotal"),
  lossTotal: document.querySelector("#lossTotal"),
  filterState: document.querySelector("#filterState"),
  sourceStatus: document.querySelector("#sourceStatus"),
  sourceName: document.querySelector("#sourceName"),
  disasterType: document.querySelector("#disasterType"),
  startDate: document.querySelector("#startDate"),
  endDate: document.querySelector("#endDate"),
  locationKeyword: document.querySelector("#locationKeyword"),
  minAffected: document.querySelector("#minAffected"),
  minLoss: document.querySelector("#minLoss"),
  descriptionKeyword: document.querySelector("#descriptionKeyword"),
  descriptionDialog: document.querySelector("#descriptionDialog"),
  dialogCloseButton: document.querySelector("#dialogCloseButton"),
  dialogMeta: document.querySelector("#dialogMeta"),
  dialogText: document.querySelector("#dialogText")
};

async function loadRecords(options = {}) {
  const refresh = options.refresh ? "?refresh=1" : "";
  setLoading(true, options.refresh ? "正在刷新官方网站数据..." : "正在加载真实数据...");

  try {
    const response = await fetch(`/api/disasters${refresh}`, { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`接口返回 ${response.status}`);
    }

    const payload = await response.json();
    disasterRecords = normalizeRecords(payload.records || []);
    sourceErrors = payload.errors || [];
    sourceNotes = payload.source_notes || [];
    currentRows = [...disasterRecords];

    populateSourceOptions();
    render();
    renderSourceStatus(payload.updated_at);
  } catch (error) {
    disasterRecords = [];
    currentRows = [];
    sourceErrors = [error.message || "真实数据接口加载失败"];
    sourceNotes = [];
    render();
    elements.sourceStatus.className = "source-status error";
    elements.sourceStatus.textContent = "未能加载真实数据。请先启动本地服务后再打开系统页面。";
  } finally {
    setLoading(false);
  }
}

function normalizeRecords(records) {
  return records.map((record) => ({
    disaster_type: String(record.disaster_type || "未分类"),
    start_time: String(record.start_time || ""),
    location: String(record.location || "未标明"),
    affected_population: toNullableNumber(record.affected_population),
    deaths_missing: toNullableNumber(record.deaths_missing),
    emergency_relocated: toNullableNumber(record.emergency_relocated),
    collapsed_houses: toNullableNumber(record.collapsed_houses),
    crop_affected_area: toNullableNumber(record.crop_affected_area),
    direct_economic_loss: toNullableNumber(record.direct_economic_loss),
    damage_description: String(record.damage_description || ""),
    source_name: String(record.source_name || "未知来源"),
    source_url: String(record.source_url || "")
  }));
}

function toNullableNumber(value) {
  if (value === null || value === undefined || value === "") return null;
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
}

function populateSourceOptions() {
  const selected = elements.sourceName.value;
  const names = [...new Set(disasterRecords.map((record) => record.source_name).filter(Boolean))].sort();

  elements.sourceName.innerHTML = `<option value="">全部来源</option>`;
  for (const name of names) {
    const option = document.createElement("option");
    option.value = name;
    option.textContent = name;
    elements.sourceName.appendChild(option);
  }

  if (names.includes(selected)) {
    elements.sourceName.value = selected;
  }
}

function setLoading(isLoading, message = "") {
  elements.refreshButton.disabled = isLoading;
  elements.downloadButton.disabled = isLoading || currentRows.length === 0;

  if (isLoading && message) {
    elements.sourceStatus.className = "source-status";
    elements.sourceStatus.textContent = message;
  }
}

function renderSourceStatus(updatedAt) {
  const parts = [];

  if (updatedAt) {
    parts.push(`更新时间：${updatedAt}`);
  }

  parts.push(`已接入 ${disasterRecords.length} 条真实记录`);

  if (sourceNotes.length > 0) {
    parts.push(sourceNotes.join("；"));
  }

  if (sourceErrors.length > 0) {
    elements.sourceStatus.className = "source-status warning";
    parts.push(`部分来源未成功：${sourceErrors.join("；")}`);
  } else {
    elements.sourceStatus.className = "source-status success";
  }

  elements.sourceStatus.textContent = parts.join("。");
}

function formatInteger(value) {
  if (value === null || value === undefined) return "-";
  return Number(value || 0).toLocaleString("zh-CN");
}

function formatCurrency(value) {
  if (value === null || value === undefined) return "-";
  const amount = Number(value || 0);

  if (amount >= 100000000) {
    return `${(amount / 100000000).toLocaleString("zh-CN", { maximumFractionDigits: 2 })} 亿元`;
  }

  if (amount >= 10000) {
    return `${(amount / 10000).toLocaleString("zh-CN", { maximumFractionDigits: 2 })} 万元`;
  }

  return `${amount.toLocaleString("zh-CN")} 元`;
}

function getFilters() {
  return {
    sourceName: elements.sourceName.value.trim(),
    disasterType: elements.disasterType.value.trim(),
    startDate: elements.startDate.value,
    endDate: elements.endDate.value,
    locationKeyword: elements.locationKeyword.value.trim(),
    minAffected: elements.minAffected.value ? Number(elements.minAffected.value) : null,
    minLoss: elements.minLoss.value ? Number(elements.minLoss.value) : null,
    descriptionKeyword: elements.descriptionKeyword.value.trim()
  };
}

function applyFilters() {
  const filters = getFilters();
  currentRows = disasterRecords.filter((record) => {
    const matchesSource = !filters.sourceName || record.source_name === filters.sourceName;
    const matchesType = !filters.disasterType || record.disaster_type.includes(filters.disasterType);
    const matchesStart = !filters.startDate || record.start_time >= filters.startDate;
    const matchesEnd = !filters.endDate || record.start_time <= filters.endDate;
    const matchesLocation = !filters.locationKeyword || record.location.includes(filters.locationKeyword);
    const matchesAffected =
      filters.minAffected === null ||
      (record.affected_population !== null && record.affected_population >= filters.minAffected);
    const matchesLoss =
      filters.minLoss === null ||
      (record.direct_economic_loss !== null && record.direct_economic_loss >= filters.minLoss);
    const matchesDescription =
      !filters.descriptionKeyword || record.damage_description.includes(filters.descriptionKeyword);

    return (
      matchesSource &&
      matchesType &&
      matchesStart &&
      matchesEnd &&
      matchesLocation &&
      matchesAffected &&
      matchesLoss &&
      matchesDescription
    );
  });

  render();
}

function render() {
  renderTable();
  renderSummary();
}

function renderTable() {
  elements.tableBody.innerHTML = "";

  currentRows.forEach((record, index) => {
    const row = document.createElement("tr");
    const typeClass = getTypeClass(record.disaster_type);
    const sourceText = record.source_url
      ? `<a href="${escapeAttribute(record.source_url)}" target="_blank" rel="noopener">${escapeHtml(record.source_name)}</a>`
      : escapeHtml(record.source_name);

    row.innerHTML = `
      <td><span class="type-pill ${typeClass}">${escapeHtml(record.disaster_type)}</span></td>
      <td class="number">${escapeHtml(record.start_time || "-")}</td>
      <td>${escapeHtml(record.location)}</td>
      <td class="number">${formatInteger(record.affected_population)}</td>
      <td class="number">${formatInteger(record.deaths_missing)}</td>
      <td class="number">${formatInteger(record.emergency_relocated)}</td>
      <td class="number">${formatInteger(record.collapsed_houses)}</td>
      <td class="number">${formatInteger(record.crop_affected_area)}${record.crop_affected_area === null ? "" : " 公顷"}</td>
      <td class="number">${formatCurrency(record.direct_economic_loss)}</td>
      <td class="description"><button class="detail-button" type="button" data-description-index="${index}">查看</button></td>
      <td class="source-cell">${sourceText}</td>
    `;

    elements.tableBody.appendChild(row);
  });

  elements.emptyState.hidden = currentRows.length > 0;
  elements.downloadButton.disabled = currentRows.length === 0;
  elements.filterState.textContent = currentRows.length === disasterRecords.length ? "全部记录" : "已筛选";
}

function renderSummary() {
  const totals = currentRows.reduce(
    (sum, record) => {
      sum.affected += Number(record.affected_population || 0);
      sum.deaths += Number(record.deaths_missing || 0);
      sum.relocated += Number(record.emergency_relocated || 0);
      sum.houses += Number(record.collapsed_houses || 0);
      sum.loss += Number(record.direct_economic_loss || 0);
      return sum;
    },
    { affected: 0, deaths: 0, relocated: 0, houses: 0, loss: 0 }
  );

  elements.totalRecords.textContent = `${disasterRecords.length} 条`;
  elements.resultCount.textContent = formatInteger(currentRows.length);
  elements.affectedTotal.textContent = formatInteger(totals.affected);
  elements.deathsTotal.textContent = formatInteger(totals.deaths);
  elements.relocatedTotal.textContent = formatInteger(totals.relocated);
  elements.houseTotal.textContent = formatInteger(totals.houses);
  elements.lossTotal.textContent = formatCurrency(totals.loss);
}

function getTypeClass(type) {
  if (type.includes("地震")) return "earthquake";
  if (type.includes("地质灾害")) return "geology";
  return "";
}

function downloadCsv() {
  const csv = toCsv(currentRows);
  const blob = new Blob([`\uFEFF${csv}`], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const date = new Date().toISOString().slice(0, 10);
  const link = document.createElement("a");

  link.href = url;
  link.download = `灾害信息_${date}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function toCsv(rows) {
  const header = csvFields.map((field) => escapeCsv(csvHeaders[field] || field)).join(",");
  const body = rows.map((row) => csvFields.map((field) => escapeCsv(row[field])).join(","));
  return [header, ...body].join("\r\n");
}

function escapeCsv(value) {
  const text = value === null || value === undefined ? "" : String(value);
  return `"${text.replace(/"/g, '""')}"`;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replace(/`/g, "&#096;");
}

function openDescription(index) {
  const record = currentRows[index];
  if (!record) return;

  elements.dialogMeta.textContent = [record.disaster_type, record.start_time, record.location]
    .filter(Boolean)
    .join(" · ");
  elements.dialogText.textContent = record.damage_description || "暂无灾情描述。";
  elements.descriptionDialog.hidden = false;
}

function closeDescription() {
  elements.descriptionDialog.hidden = true;
  elements.dialogMeta.textContent = "";
  elements.dialogText.textContent = "";
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  applyFilters();
});

elements.resetButton.addEventListener("click", () => {
  elements.form.reset();
  currentRows = [...disasterRecords];
  render();
});

elements.refreshButton.addEventListener("click", () => {
  loadRecords({ refresh: true });
});

elements.tableBody.addEventListener("click", (event) => {
  const button = event.target.closest("[data-description-index]");
  if (!button) return;
  openDescription(Number(button.dataset.descriptionIndex));
});

elements.dialogCloseButton.addEventListener("click", closeDescription);

elements.descriptionDialog.addEventListener("click", (event) => {
  if (event.target === elements.descriptionDialog) {
    closeDescription();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !elements.descriptionDialog.hidden) {
    closeDescription();
  }
});

elements.downloadButton.addEventListener("click", downloadCsv);

loadRecords();
