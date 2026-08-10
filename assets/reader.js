(() => {
  const storageKey = "redacoes-reader-preferences"
  const body = document.body
  const shell = document.querySelector(".reader-shell")
  const darkPdfButton = document.querySelector('[data-action="toggle-dark-pdf"]')
  const focusButton = document.querySelector('[data-action="toggle-focus"]')

  const prefersDark = window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false
  const state = {
    darkPdf: false,
    focusMode: false,
    siteDark: prefersDark,
  }

  try {
    const saved = localStorage.getItem(storageKey)
    if (saved) {
      const parsed = JSON.parse(saved)
      if (typeof parsed.darkPdf === "boolean") state.darkPdf = parsed.darkPdf
      if (typeof parsed.focusMode === "boolean") state.focusMode = parsed.focusMode
      if (typeof parsed.siteDark === "boolean") state.siteDark = parsed.siteDark
    }
  } catch {
    // Storage can be unavailable in hardened/private browser modes.
  }

  const sync = () => {
    body.classList.toggle("pdf-dark", state.darkPdf)
    body.classList.toggle("reader-theme-dark", state.siteDark || state.darkPdf)
    shell?.classList.toggle("reader-shell--focus", state.focusMode)

    if (darkPdfButton) {
      darkPdfButton.setAttribute("aria-pressed", String(state.darkPdf))
      darkPdfButton.textContent = `Modo escuro do PDF: ${state.darkPdf ? "ligado" : "desligado"}`
    }

    if (focusButton) {
      focusButton.setAttribute("aria-pressed", String(state.focusMode))
      focusButton.textContent = `Leitura confortável: ${state.focusMode ? "ligada" : "desligada"}`
    }

    try {
      localStorage.setItem(storageKey, JSON.stringify(state))
    } catch {
      // Keep controls functional even if preferences cannot be persisted.
    }
  }

  darkPdfButton?.addEventListener("click", () => {
    state.darkPdf = !state.darkPdf
    sync()
  })

  focusButton?.addEventListener("click", () => {
    state.focusMode = !state.focusMode
    sync()
  })

  sync()
})()
