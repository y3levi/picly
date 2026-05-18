const btnBuscar = document.getElementById("btn-buscar");
const inputBusca = document.getElementById("input-busca");
const grid = document.getElementById("grid-resultados");
const status = document.getElementById("status");
const filtroAtivoInfo = document.getElementById("filtro-ativo");
const modal = document.getElementById("modal");
const modalImg = document.getElementById("modal-img");
const modalDownload = document.getElementById("modal-download");
const modalFechar = document.getElementById("modal-fechar");
const modalOverlay = document.getElementById("modal-overlay");
const gridRelacionadas = document.getElementById("grid-relacionadas");
const filtroBtns = document.querySelectorAll(".filtro-btn");
const dropdown = document.getElementById("dropdown");
const abaBtns = document.querySelectorAll(".aba-btn");
const btnRembg = document.getElementById("btn-rembg");
const previewEditado = document.getElementById("preview-editado");
const imgEditada = document.getElementById("img-editada");
const downloadEditado = document.getElementById("download-editado");
const statusEdicao = document.getElementById("status-edicao");

let debounceTimer = null;
let paginaAtual = 1;
let termoBusca = "";
let filtroAtivo = "";
let carregando = false;
let semMais = false;
let msnry = null;
let urlImagemAtual = "";

// autocomplete
inputBusca.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  const val = inputBusca.value.trim();
  if (val.length < 2) {
    fecharDropdown();
    return;
  }
  debounceTimer = setTimeout(() => buscarSugestoes(val), 300);
});

document.addEventListener("click", (e) => {
  if (!e.target.closest(".input-wrapper")) fecharDropdown();
});
//filtrar tags erradas
const NSFW_SUBSTRINGS = [
  "nipple",
  "areola",
  "breast",
  "boob",
  "tit",
  "cleavage_cutout",
  "penis",
  "cock",
  "dick",
  "phallus",
  "glans",
  "foreskin",
  "erection",
  "vagina",
  "vulva",
  "pussy",
  "labia",
  "clitoris",
  "anus",
  "anal",
  "asshole",
  "butthole",
  "testicle",
  "balls",
  "scrotum",
  "semen",
  "cum",
  "ejacul",
  "sex",
  "fuck",
  "intercourse",
  "penetrat",
  "insertion",
  "masturbat",
  "fingering",
  "handjob",
  "blowjob",
  "fellatio",
  "cunnilingus",
  "anilingus",
  "rimjob",
  "rimming",
  "creampie",
  "gangbang",
  "orgy",
  "threesome",
  "rape",
  "molest",
  "grope",
  "orgasm",
  "squirt",
  "nude",
  "naked",
  "nudity",
  "topless",
  "bottomless",
  "nsfw",
  "hentai",
  "porn",
  "erotic",
  "lewd",
  "uncensor",
  "mosaic_censor",
  "bdsm",
  "bondage",
  "restraint",
  "handcuff",
  "whip",
  "spanking",
  "chastity",
  "ballgag",
  "tentacle",
  "oviposit",
  "inflation",
  "vore",
  "scat",
  "urine",
  "lactation",
  "milking",
  "breast_milk",
  "futanari",
  "futa",
  "bestiality",
  "zoophilia",
  "guro",
  "gore",
  "snuff",
  "incest",
  "netorare",
  "mind_break",
  "mind_control",
  "sex_slave",
  "glory_hole",
  "fisting",
  "object_insertion",
  "dildo",
  "vibrator",
  "sex_toy",
  "strapon",
  "rating:e",
  "rating:q",
];

const EXCECOES = new Set([
  "glasses",
  "sunglasses",
  "class",
  "brass",
  "assassin",
  "classic",
  "breast_pocket",
]);

const isSafe = (tag) =>
  EXCECOES.has(tag) || !NSFW_SUBSTRINGS.some((sub) => tag.includes(sub));

async function buscarSugestoes(q) {
  try {
    const res = await fetch(`/autocomplete?q=${encodeURIComponent(q)}`);
    const todos = await res.json();
    const itens = todos.filter((item) => isSafe(item.tag.toLowerCase())); // tirar tags nsfw e afins
    if (itens.length === 0) {
      fecharDropdown();
      return;
    }

    dropdown.innerHTML = "";
    itens.forEach((item) => {
      const div = document.createElement("div");
      div.className = "dropdown-item";
      div.innerHTML = `
        <span class="tag-nome">${item.tag}</span>
        <span class="tag-count">${item.count.toLocaleString()} posts</span>
      `;
      div.addEventListener("click", () => {
        inputBusca.value = item.tag;
        fecharDropdown();
        novaBusca(true);
      });
      dropdown.appendChild(div);
    });
    dropdown.classList.remove("hidden");
  } catch {
    fecharDropdown();
  }
}

function fecharDropdown() {
  dropdown.classList.add("hidden");
  dropdown.innerHTML = "";
}

// iniciar Masonry
function iniciarMasonry() {
  msnry = new Masonry(grid, {
    itemSelector: ".grid-item",
    columnWidth: ".grid-sizer",
    percentPosition: true,
    gutter: 12,
    transitionDuration: 0,
  });
}

// filtros
filtroBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (btn.classList.contains("ativo")) {
      btn.classList.remove("ativo");
      filtroAtivo = "";
      filtroAtivoInfo.textContent = "";
    } else {
      filtroBtns.forEach((b) => b.classList.remove("ativo"));
      btn.classList.add("ativo");
      filtroAtivo = btn.dataset.tags;
    }
    if (termoBusca) novaBusca(false);
  });
});

// busca
btnBuscar.addEventListener("click", () => novaBusca(true));
inputBusca.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    fecharDropdown();
    novaBusca(true);
  }
  if (e.key === "Escape") fecharDropdown();
});

window.addEventListener("scroll", () => {
  if (carregando || semMais) return;
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 400) {
    carregarMais();
  }
});

function novaBusca(atualizarTermo = true) {
  if (atualizarTermo) {
    const termo = inputBusca.value.trim();
    if (!termo) return;
    termoBusca = termo;
  }
  if (!termoBusca) return;

  paginaAtual = 1;
  semMais = false;
  grid.innerHTML = '<div class="grid-sizer"></div>';
  status.textContent = "Buscando...";

  if (filtroAtivo) {
    filtroAtivoInfo.textContent = `+ filtro: ${filtroAtivo}`;
  } else {
    filtroAtivoInfo.textContent = "";
  }

  iniciarMasonry();
  carregarMais();
}

async function carregarMais() {
  if (carregando || semMais) return;
  carregando = true;

  try {
    const params = new URLSearchParams({
      q: termoBusca,
      pagina: paginaAtual,
      ...(filtroAtivo && { filtro_tags: filtroAtivo }),
    });

    const res = await fetch(`/buscar?${params}`);
    const itens = await res.json();

    if (itens.length === 0) {
      semMais = true;
      status.textContent =
        paginaAtual === 1
          ? "Nenhuma imagem encontrada."
          : "Todas as imagens carregadas.";
      carregando = false;
      return;
    }

    status.textContent = "Clique em uma imagem para ampliar.";
    paginaAtual++;

    let carregadas = 0;
    const total = itens.length;

    itens.forEach((item) => {
      const div = document.createElement("div");
      div.className = "grid-item";
      const img = document.createElement("img");
      img.loading = "lazy";
      img.decoding = "async";
      img.src = item.url;

      img.addEventListener("load", () => {
        carregadas++;
        msnry.appended([div]);
        if (carregadas === total) msnry.layout();
      });

      img.addEventListener("error", () => {
        carregadas++;
        div.remove();
        if (carregadas === total) msnry.layout();
      });

      img.addEventListener("click", () => abrirModal(item));
      div.appendChild(img);
      grid.appendChild(div);
    });
  } catch (err) {
    console.error(err);
    status.textContent =
      "o Site ainda tá em fase de testes, contém alguns bugs. Tente novamente mais tarde.";
  }

  carregando = false;
}

// modal stuff

// abas do modal
abaBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    abaBtns.forEach((b) => b.classList.remove("ativo"));
    btn.classList.add("ativo");

    document
      .querySelectorAll(".aba-conteudo")
      .forEach((c) => c.classList.add("hidden"));
    document
      .getElementById(`aba-${btn.dataset.aba}`)
      .classList.remove("hidden");
  });
});

// rembg
btnRembg.addEventListener("click", async () => {
  if (!urlImagemAtual) return;

  statusEdicao.textContent = "Removendo fundo... pode demorar alguns segundos.";
  btnRembg.disabled = true;
  btnRembg.textContent = "Processando...";
  previewEditado.classList.add("hidden");

  try {
    const res = await fetch(
      `/processar?url=${encodeURIComponent(urlImagemAtual)}&op=rembg`,
    );
    const data = await res.json();

    if (!res.ok || data.error) {
      statusEdicao.textContent = "Erro ao processar imagem.";
    } else {
      imgEditada.src = data.imagem;
      downloadEditado.href = data.imagem;
      previewEditado.classList.remove("hidden");
      statusEdicao.textContent = "Pronto!";
    }
  } catch {
    statusEdicao.textContent = "Erro ao conectar com o servidor.";
  }

  btnRembg.disabled = false;
  btnRembg.textContent = "Aplicar";
});

// abrir modal
function fecharModal() {
  modal.classList.add("hidden");
  modalImg.src = "";
  gridRelacionadas.innerHTML = "";
  document.body.style.overflow = "";
}

modalFechar.addEventListener("click", fecharModal);
modalOverlay.addEventListener("click", fecharModal);
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") fecharModal();
});

async function carregarRelacionadas() {
  try {
    const res = await fetch(
      `/relacionadas?q=${encodeURIComponent(termoBusca)}`,
    );
    const itens = await res.json();
    gridRelacionadas.innerHTML = "";

    if (itens.length === 0) {
      gridRelacionadas.innerHTML =
        '<p style="color:#555; font-size:13px;">Nenhuma encontrada.</p>';
      return;
    }

    itens.forEach((item) => {
      const img = document.createElement("img");
      img.src = item.url;
      img.loading = "lazy";
      img.addEventListener("click", () => abrirModal(item));
      gridRelacionadas.appendChild(img);
    });
  } catch {
    gridRelacionadas.innerHTML =
      '<p style="color:#555; font-size:13px;">Erro ao carregar.</p>';
  }
}

function abrirModal(item) {
  urlImagemAtual = item.url;
  modalImg.src = item.url;
  modalDownload.href = `/download?url=${encodeURIComponent(item.url)}`;
  document.getElementById("modal-fonte").textContent = item.fonte;

  // reseta abas pro estado inicial
  abaBtns.forEach((b) => b.classList.remove("ativo"));
  abaBtns[0].classList.add("ativo");
  document
    .querySelectorAll(".aba-conteudo")
    .forEach((c) => c.classList.add("hidden"));
  document.getElementById("aba-relacionadas").classList.remove("hidden");

  // reseta editor
  previewEditado.classList.add("hidden");
  statusEdicao.textContent = "";
  btnRembg.textContent = "Aplicar";
  btnRembg.disabled = false;
  imgEditada.src = "";
  downloadEditado.href = "#";

  gridRelacionadas.innerHTML =
    '<p style="color:#555; font-size:13px;">Carregando...</p>';
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
  carregarRelacionadas();
}
