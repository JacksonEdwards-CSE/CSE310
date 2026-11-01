const DATA_URL = "filming-locations.geojson";
const DISPLAY_LIMIT = 5000;
const LIST_LIMIT = 150;
let markerScale = 1;
const FALLBACK_LOCATIONS = [["Q10400","Almería","Spain","city","Towns & cities",36.84167,-2.46389,"Municipality and capital of the province of Almeria, Spain","Indiana Jones and the Last Crusade"],["Q505208","Ouarzazate","Morocco","city","Towns & cities",30.91667,-6.91667,"City in Morocco","Paul the Apostle"],["Q10686","Belfast","United Kingdom","city","Towns & cities",54.59667,-5.93,"Capital city of Northern Ireland","Game of Thrones"],["Q8717","Seville","Spain","city","Towns & cities",37.38861,-5.995,"Municipality of Andalusia, Spain","Alatriste"],["Q7038","Girona","Spain","city","Towns & cities",41.98333,2.81667,"City in Catalonia, Spain","Game of Thrones"],["Q1722","Dubrovnik","Croatia","city","Towns & cities",42.64028,18.10833,"Historic city on the Adriatic coast","Game of Thrones"],["Q1252715","Doune Castle","United Kingdom","castle","Castles & palaces",56.18516,-4.05025,"Castle in Stirling, Scotland","Outlander"],["Q216939","Essaouira","Morocco","city","Towns & cities",31.51302,-9.7687,"City in Morocco","Jerusalem"],["Q170488","Gozo","Malta","nature","Landscapes & nature",36.045,14.25889,"Island of the Maltese archipelago","By the Sea"],["Q15678","Cáceres","Spain","city","Towns & cities",39.47306,-6.37111,"Town of Extremadura, Spain",""],["Q1663","Split","Croatia","city","Towns & cities",43.51,16.44,"City in Split-Dalmatia County, Croatia",""],["Q1431801","Fort Ricasoli","Malta","castle","Castles & palaces",35.8975,14.52583,"Fort in Malta","Game of Thrones"],["Q207277","Mdina","Malta","city","Towns & cities",35.88583,14.40306,"Historic city in Malta","Game of Thrones"],["Q7487953","Shane's Castle ruins","United Kingdom","castle","Castles & palaces",54.7274,-6.26807,"Country house ruins in Northern Ireland",""],["Q1968","Vatnajökull","Iceland","nature","Landscapes & nature",64.4,-16.8,"Ice cap and national park in Iceland","Interstellar"],["Q181136","Walls of Dubrovnik","Croatia","castle","Castles & palaces",42.641,18.11,"Historic city walls in Dubrovnik","Game of Thrones"],["Q103983","Ballintoy","United Kingdom","city","Towns & cities",55.241,-6.371,"Village on the north coast of County Antrim","Game of Thrones"],["Q1015969","Carncastle","United Kingdom","city","Towns & cities",54.887,-5.935,"Village in County Antrim, Northern Ireland","Game of Thrones"],["Q18091","Córdoba","Spain","city","Towns & cities",37.888,-4.779,"City in Andalusia, Spain","The Other Boleyn Girl"],["Q1908","Dimmuborgir","Iceland","nature","Landscapes & nature",65.591,-16.912,"Lava field in northern Iceland","Game of Thrones"]].map((location,index)=>({type:"Feature",geometry:{type:"Point",coordinates:[location[6],location[5]]},properties:{qid:location[0],name:location[1],country:location[2],category:location[3],category_label:location[4],latitude:location[5],longitude:location[6],description:location[7],top_productions:location[8],fame_rank:index+1}}));

const map = L.map("map", { worldCopyJump: true, zoomControl: true }).setView([25, 10], 2);
const streetTiles = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
L.control.layers({ "Street map": streetTiles }).addTo(map);

function createMarkerIcon() { const size = 25 * markerScale; return L.icon({ iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png", shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png", iconSize: [size, size * 1.64], iconAnchor: [size / 2, size * 1.64], popupAnchor: [0, -size * 1.64] }); }

const markerLayer = L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 45 }).addTo(map);
const state = { locations: [], filtered: [], selected: null };
const els = {
  search: document.querySelector("#search"), category: document.querySelector("#category"),
  details: document.querySelector("#details"), list: document.querySelector("#location-list"),
  locationCount: document.querySelector("#location-count"), resultCount: document.querySelector("#result-count"), categoryCount: document.querySelector("#category-count"), countryCount: document.querySelector("#country-count"), markerSize: document.querySelector("#marker-size"), markerSizeValue: document.querySelector("#marker-size-value")
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function detailsHtml(p) {
  const films = p.top_productions ? escapeHtml(p.top_productions) : "No production titles listed.";
  const links = [p.wikipedia, p.url].filter(Boolean).map(link => `<a class="more-link" href="${escapeHtml(link)}" target="_blank" rel="noreferrer">Learn more ↗</a>`).join(" ");
  return `<h2 class="location-title">${escapeHtml(p.name)}</h2>
    <p class="location-meta">${escapeHtml(p.country)} · ${escapeHtml(p.category_label || p.category)} · ${p.latitude.toFixed(4)}, ${p.longitude.toFixed(4)}</p>
    ${p.description ? `<p class="location-description">${escapeHtml(p.description)}</p>` : ""}
    <div class="film-list"><strong>Films &amp; productions</strong><br>${films}</div>${links}`;
}

function selectLocation(location, pan = true) {
  state.selected = location;
  els.details.className = "location-card";
  els.details.innerHTML = detailsHtml(location.properties);
  document.querySelectorAll(".location-item").forEach(item => item.classList.toggle("active", item.dataset.qid === location.properties.qid));
  if (pan) map.flyTo([location.properties.latitude, location.properties.longitude], Math.max(map.getZoom(), 5), { duration: .7 });
  location.marker.openPopup();
}

function renderList() {
  els.resultCount.textContent = state.filtered.length.toLocaleString();
  els.categoryCount.textContent = new Set(state.filtered.map(location => location.properties.category).filter(Boolean)).size;
  els.countryCount.textContent = new Set(state.filtered.map(location => location.properties.country).filter(Boolean)).size;
}
function applyFilters() {
  const term = els.search.value.trim().toLowerCase();
  const category = els.category.value;
  state.filtered = state.locations.filter(location => {
    const p = location.properties;
    const searchable = [p.name, p.country, p.top_productions, p.description].filter(Boolean).join(" ").toLowerCase();
    return (category === "all" || p.category === category) && (!term || searchable.includes(term));
  });
  markerLayer.clearLayers();
  state.filtered.forEach(location => markerLayer.addLayer(location.marker));
  renderList();
}

async function loadLocations() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`Could not load ${DATA_URL}`);
    const geojson = await response.json();
    const features = geojson.features.filter(feature => feature.geometry?.type === "Point" && Number.isFinite(feature.properties?.latitude) && Number(feature.properties?.productions) > 0)
      .sort((a, b) => (a.properties.fame_rank ?? Number.MAX_SAFE_INTEGER) - (b.properties.fame_rank ?? Number.MAX_SAFE_INTEGER)).slice(0, DISPLAY_LIMIT);
    state.locations = features.map(feature => {
      const p = feature.properties;
      const marker = L.marker([p.latitude, p.longitude], { icon: createMarkerIcon() }).bindPopup(`<h3 class="popup-title">${escapeHtml(p.name)}</h3><p class="popup-meta">${escapeHtml(p.country)} · Click for details</p>`);
      marker.on("click", () => selectLocation({ properties: p, marker }, false));
      return { properties: p, marker };
    });
    [...new Set(state.locations.map(location => location.properties.category).filter(Boolean))].sort().forEach(category => {
      const option = document.createElement("option"); option.value = category; option.textContent = state.locations.find(l => l.properties.category === category).properties.category_label || category; els.category.appendChild(option);
    });
    els.locationCount.textContent = state.locations.length;
    applyFilters();
    const bounds = L.latLngBounds(state.locations.map(location => [location.properties.latitude, location.properties.longitude]));
    map.fitBounds(bounds.pad(.12));
  } catch (error) {
    state.locations = FALLBACK_LOCATIONS.map(feature => { const p = feature.properties; const marker = L.marker([p.latitude, p.longitude], { icon: createMarkerIcon() }).bindPopup(`<h3 class="popup-title">${escapeHtml(p.name)}</h3><p class="popup-meta">${escapeHtml(p.country)} · Click for details</p>`); marker.on("click", () => selectLocation({ properties: p, marker }, false)); return { properties: p, marker }; });
    els.locationCount.textContent = state.locations.length;
    els.details.className = "empty-state";
    els.details.textContent = "The full dataset could not be loaded, so the site is showing 20 built-in locations. Use the local server command in README.md to load all 40 locations.";
    applyFilters();
    map.fitBounds(L.latLngBounds(state.locations.map(location => [location.properties.latitude, location.properties.longitude])).pad(.12));
    map.setMinZoom(map.getZoom());
  }
}

els.search.addEventListener("input", applyFilters);
els.category.addEventListener("change", applyFilters);
els.markerSize.addEventListener("input", () => { markerScale = Number(els.markerSize.value) / 100; els.markerSizeValue.textContent = `${els.markerSize.value}%`; state.locations.forEach(location => location.marker.setIcon(createMarkerIcon())); });
const settingsMenu = document.querySelector(".settings-menu");
settingsMenu.querySelectorAll("[data-theme]").forEach(option => option.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode", option.dataset.theme === "dark");
  settingsMenu.removeAttribute("open");
}));
settingsMenu.querySelectorAll("[data-sidebar]").forEach(option => option.addEventListener("click", () => {
  document.querySelector(".app-shell").classList.toggle("sidebar-collapsed", option.dataset.sidebar === "hide");
  setTimeout(() => map.invalidateSize(), 250);
  settingsMenu.removeAttribute("open");
}));
document.querySelector("#reset-view").addEventListener("click", () => {
  if (state.locations.length) map.fitBounds(L.latLngBounds(state.locations.map(location => [location.properties.latitude, location.properties.longitude])).pad(.12));
    map.setMinZoom(map.getZoom());
});
loadLocations();
window.addEventListener("resize", () => map.invalidateSize());
setTimeout(() => map.invalidateSize(), 250);
