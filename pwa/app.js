/**
 * =============================================================================
 *           ✨ STYVEDEV DOWNLOAD PRO — FRONTEND JAVASCRIPT (PWA)
 * =============================================================================
 * - Multi-langue complet : Français (fr), English (en), Español (es),
 *   Deutsch (de), Português (pt), العربية (ar) avec support RTL
 * - Icônes vectorielles SVG officielles pour toutes les plateformes
 * - Zéro émojis infantiles : Interface ultra-professionnelle & épurée
 * - Tailles exactes calculées avant téléchargement
 * - Support temps réel WebSocket & bouton d'arrêt instantané
 * =============================================================================
 */

// Résolution automatique de l'adresse du serveur
const API_BASE = window.location.origin;
const WS_PROTO = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
const WS_BASE = `${WS_PROTO}//${window.location.host}/ws/download`;

// =============================================================================
// ICÔNES VECTORIELLES SVG POUR TOUTES LES PLATEFORMES & ACTIONS
// =============================================================================
const SVG_ICONS = {
  globe: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>`,
  youtube: `<svg viewBox="0 0 24 24" fill="#FF0000" width="15" height="15"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>`,
  facebook: `<svg viewBox="0 0 24 24" fill="#1877F2" width="15" height="15"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>`,
  instagram: `<svg viewBox="0 0 24 24" fill="#E1306C" width="15" height="15"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>`,
  tiktok: `<svg viewBox="0 0 24 24" fill="#00F2FE" width="15" height="15"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.24 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>`,
  twitter: `<svg viewBox="0 0 24 24" fill="#FFFFFF" width="15" height="15"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>`,
  twitch: `<svg viewBox="0 0 24 24" fill="#9146FF" width="15" height="15"><path d="M2.149 0l-1.612 4.119v16.8h5.9v3.081h3.224l3.08-3.081h4.839l6.42-6.42v-14.499h-21.851zm19.702 13.433l-3.754 3.754h-5.367l-3.08 3.081v-3.081h-4.839v-15.034h17.04v11.28zM16.634 5.908h-2.686v5.372h2.686v-5.372zm-5.9 0h-2.687v5.372h2.687v-5.372z"/></svg>`,
  reddit: `<svg viewBox="0 0 24 24" fill="#FF4500" width="15" height="15"><path d="M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.197-2.512-.73a.326.326 0 0 0-.232-.095z"/></svg>`,
  vimeo: `<svg viewBox="0 0 24 24" fill="#1AB7EA" width="15" height="15"><path d="M23.977 6.416c-.105 2.338-1.739 5.543-4.894 9.609-3.268 4.247-6.026 6.37-8.29 6.37-1.409 0-2.578-1.294-3.553-3.881L5.322 11.4C4.603 8.816 3.834 7.522 3.01 7.522c-.179 0-.806.378-1.881 1.132L0 7.197c1.185-1.044 2.351-2.084 3.501-3.128C5.08 2.701 6.266 1.984 7.055 1.91c1.867-.18 3.016 1.1 3.447 3.838.465 2.953.789 4.789.971 5.507.539 2.45 1.131 3.674 1.776 3.674.502 0 1.256-.796 2.265-2.385 1.004-1.589 1.54-2.797 1.612-3.628.144-1.371-.395-2.061-1.612-2.061-.574 0-1.167.121-1.777.391 1.186-3.868 3.434-5.757 6.762-5.637 2.473.06 3.628 1.664 3.478 4.807l-.001.004z"/></svg>`,
  dailymotion: `<svg viewBox="0 0 24 24" fill="#0066DC" width="15" height="15"><path d="M12.003 0C5.374 0 0 5.374 0 12.003 0 18.629 5.374 24 12.003 24 18.629 24 24 18.629 24 12.003 24 5.374 18.629 0 12.003 0zm4.912 15.66c-.642.864-1.5 1.307-2.572 1.325-.574.012-1.147-.091-1.738-.312v.27H10.71V6.618h1.895v3.444c.61-.247 1.184-.372 1.726-.372 1.112 0 1.98.437 2.605 1.316.624.878.937 2.017.937 3.42 0 1.304-.32 2.378-.958 3.234zm-1.632-5.448c-.31-.468-.768-.7-1.376-.7-.357 0-.734.086-1.135.26v4.74c.389.16.759.24 1.11.24.635 0 1.102-.232 1.4-.696.298-.463.45-1.127.45-1.99 0-.93-.15-1.586-.449-2.054z"/></svg>`,
  music: `<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>`,
  video: `<svg viewBox="0 0 24 24" fill="currentColor" width="15" height="15"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`,
  openFile: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="14" height="14"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>`
};

// =============================================================================
// DICTIONNAIRE I18N EN 6 LANGUES
// =============================================================================
const TRANSLATIONS = {
  fr: {
    subtitle: "Téléchargeur universel haute vitesse • Estimation exacte de la taille avant téléchargement",
    themeDark: "Sombre",
    themeLight: "Clair",
    themeSystem: "Système",
    platformsLabel: "Plateformes :",
    inputTitle: "Coller le lien de la vidéo ou de l'audio",
    readyStatus: "Prêt",
    urlPlaceholder: "Collez un lien ici (ex: YouTube, Facebook, TikTok, Instagram, Twitter/X...)",
    btnPaste: "Coller",
    btnAnalyze: "Analyser",
    btnAnalyzeLoading: "Analyse...",
    singleVideoText: "Télécharger uniquement cette vidéo (Empêche de télécharger tout le Mix ou la Playlist)",
    previewPlaceholder: "Collez un lien ci-dessus pour afficher la vidéo et sa taille exacte avant téléchargement",
    settingsTitle: "Options de Téléchargement & Destination",
    formatLabel: "Format / Résolution :",
    destLabel: "Dossier de destination :",
    btnBrowse: "Parcourir...",
    statusReady: "Prêt",
    btnDownload: "TÉLÉCHARGER MAINTENANT",
    btnStop: "ARRÊTER",
    btnFolder: "Dossier",
    historyTitle: "Historique de la session",
    btnClear: "Effacer",
    historyEmpty: "Aucun téléchargement dans cette session",
    authorLabel: "Auteur :",
    exactSizeLabel: "Taille exacte :",
    calculating: "Calcul en cours...",
    unknown: "Inconnu",
    viewsSuffix: "vues",
    speedLabel: "Vitesse",
    openBtn: "Ouvrir",
    optBest: "Vidéo - Meilleure qualité (Auto / 4K / 1080p)",
    opt1080: "Vidéo - 1080p Full HD (MP4)",
    opt720: "Vidéo - 720p HD (MP4)",
    opt480: "Vidéo - 480p SD (MP4)",
    opt360: "Vidéo - 360p Mobile (MP4)",
    optMp3: "Audio seul - MP3 Haute Qualité (320 kbps)",
    optM4a: "Audio seul - M4A / AAC (Standard)",
    toastPasteSuccess: "Lien collé ! Analyse en cours...",
    toastPasteFail: "Veuillez coller le lien manuellement (Ctrl+V)",
    toastAnalyzeSuccess: "Vidéo analysée avec succès !",
    toastDownloadSuccess: "Téléchargement terminé avec succès !",
    toastCancelled: "Téléchargement interrompu",
    toastError: "Erreur",
    toastFolderSuccess: "Dossier ouvert dans l'explorateur",
    toastHistoryCleared: "Historique de session effacé",
    statusAnalyzing: "Analyse des flux et calcul des tailles exactes...",
    statusDownloading: "Téléchargement en cours",
    statusComplete: "Téléchargement terminé avec succès !",
    statusCancelledMsg: "Téléchargement interrompu par l'utilisateur.",
    statusStarting: "Démarrage du téléchargement...",
    statusConnecting: "Connexion au serveur...",
    statusStopping: "Arrêt en cours..."
  },
  en: {
    subtitle: "Universal high-speed downloader • Exact size computation before download",
    themeDark: "Dark",
    themeLight: "Light",
    themeSystem: "System",
    platformsLabel: "Platforms:",
    inputTitle: "Paste video or audio link",
    readyStatus: "Ready",
    urlPlaceholder: "Paste a link here (e.g. YouTube, Facebook, TikTok, Instagram, Twitter/X...)",
    btnPaste: "Paste",
    btnAnalyze: "Analyze",
    btnAnalyzeLoading: "Analyzing...",
    singleVideoText: "Download only this video (Prevents downloading entire Mix or Playlist)",
    previewPlaceholder: "Paste a link above to display video preview and exact size before downloading",
    settingsTitle: "Download Options & Destination",
    formatLabel: "Format / Quality:",
    destLabel: "Destination folder:",
    btnBrowse: "Browse...",
    statusReady: "Ready",
    btnDownload: "DOWNLOAD NOW",
    btnStop: "STOP",
    btnFolder: "Folder",
    historyTitle: "Session History",
    btnClear: "Clear",
    historyEmpty: "No downloads in this session",
    authorLabel: "Author:",
    exactSizeLabel: "Exact size:",
    calculating: "Calculating...",
    unknown: "Unknown",
    viewsSuffix: "views",
    speedLabel: "Speed",
    openBtn: "Open",
    optBest: "Video - Best Quality (Auto / 4K / 1080p)",
    opt1080: "Video - 1080p Full HD (MP4)",
    opt720: "Video - 720p HD (MP4)",
    opt480: "Video - 480p SD (MP4)",
    opt360: "Video - 360p Mobile (MP4)",
    optMp3: "Audio only - MP3 High Quality (320 kbps)",
    optM4a: "Audio only - M4A / AAC (Standard)",
    toastPasteSuccess: "Link pasted! Analyzing...",
    toastPasteFail: "Please paste the link manually (Ctrl+V)",
    toastAnalyzeSuccess: "Video analyzed successfully!",
    toastDownloadSuccess: "Download completed successfully!",
    toastCancelled: "Download cancelled",
    toastError: "Error",
    toastFolderSuccess: "Folder opened in file explorer",
    toastHistoryCleared: "Session history cleared",
    statusAnalyzing: "Analyzing streams and computing exact sizes...",
    statusDownloading: "Downloading",
    statusComplete: "Download completed successfully!",
    statusCancelledMsg: "Download cancelled by user.",
    statusStarting: "Starting download...",
    statusConnecting: "Connecting to server...",
    statusStopping: "Stopping..."
  },
  es: {
    subtitle: "Descargador universal de alta velocidad • Estimación exacta del tamaño antes de descargar",
    themeDark: "Oscuro",
    themeLight: "Claro",
    themeSystem: "Sistema",
    platformsLabel: "Plataformas:",
    inputTitle: "Pegar enlace de video o audio",
    readyStatus: "Listo",
    urlPlaceholder: "Pegue un enlace aquí (ej: YouTube, Facebook, TikTok, Instagram, Twitter/X...)",
    btnPaste: "Pegar",
    btnAnalyze: "Analizar",
    btnAnalyzeLoading: "Analizando...",
    singleVideoText: "Descargar solo este video (Evita descargar toda la lista de reproducción)",
    previewPlaceholder: "Pegue un enlace arriba para mostrar la vista previa y el tamaño exacto",
    settingsTitle: "Opciones de Descarga y Destino",
    formatLabel: "Formato / Resolución:",
    destLabel: "Carpeta de destino:",
    btnBrowse: "Examinar...",
    statusReady: "Listo",
    btnDownload: "DESCARGAR AHORA",
    btnStop: "DETENER",
    btnFolder: "Carpeta",
    historyTitle: "Historial de la sesión",
    btnClear: "Borrar",
    historyEmpty: "No hay descargas en esta sesión",
    authorLabel: "Autor:",
    exactSizeLabel: "Tamaño exacto:",
    calculating: "Calculando...",
    unknown: "Desconocido",
    viewsSuffix: "vistas",
    speedLabel: "Velocidad",
    openBtn: "Abrir",
    optBest: "Video - Mejor calidad (Auto / 4K / 1080p)",
    opt1080: "Video - 1080p Full HD (MP4)",
    opt720: "Video - 720p HD (MP4)",
    opt480: "Video - 480p SD (MP4)",
    opt360: "Video - 360p Móvil (MP4)",
    optMp3: "Solo audio - MP3 Alta Calidad (320 kbps)",
    optM4a: "Solo audio - M4A / AAC (Estándar)",
    toastPasteSuccess: "¡Enlace pegado! Analizando...",
    toastPasteFail: "Por favor pegue el enlace manualmente (Ctrl+V)",
    toastAnalyzeSuccess: "¡Video analizado con éxito!",
    toastDownloadSuccess: "¡Descarga completada con éxito!",
    toastCancelled: "Descarga cancelada",
    toastError: "Error",
    toastFolderSuccess: "Carpeta abierta en el explorador",
    toastHistoryCleared: "Historial de sesión borrado",
    statusAnalyzing: "Analizando flujos y calculando tamaños exactos...",
    statusDownloading: "Descargando",
    statusComplete: "¡Descarga completada con éxito!",
    statusCancelledMsg: "Descarga interrumpida por el usuario.",
    statusStarting: "Iniciando descarga...",
    statusConnecting: "Conectando al servidor...",
    statusStopping: "Deteniendo..."
  },
  de: {
    subtitle: "Universeller Hochgeschwindigkeits-Downloader • Exakte Größenberechnung vor dem Download",
    themeDark: "Dunkel",
    themeLight: "Hell",
    themeSystem: "System",
    platformsLabel: "Plattformen:",
    inputTitle: "Video- oder Audio-Link einfügen",
    readyStatus: "Bereit",
    urlPlaceholder: "Fügen Sie hier einen Link ein (z. B. YouTube, Facebook, TikTok...)",
    btnPaste: "Einfügen",
    btnAnalyze: "Analysieren",
    btnAnalyzeLoading: "Analysiere...",
    singleVideoText: "Nur dieses Video herunterladen (Verhindert das Laden der Playlist)",
    previewPlaceholder: "Fügen Sie oben einen Link ein, um Vorschau und exakte Größe anzuzeigen",
    settingsTitle: "Download-Optionen & Zielordner",
    formatLabel: "Format / Auflösung:",
    destLabel: "Zielordner:",
    btnBrowse: "Durchsuchen...",
    statusReady: "Bereit",
    btnDownload: "JETZT HERUNTERLADEN",
    btnStop: "STOPP",
    btnFolder: "Ordner",
    historyTitle: "Sitzungsverlauf",
    btnClear: "Löschen",
    historyEmpty: "Keine Downloads in dieser Sitzung",
    authorLabel: "Autor:",
    exactSizeLabel: "Exakte Größe:",
    calculating: "Wird berechnet...",
    unknown: "Unbekannt",
    viewsSuffix: "Aufrufe",
    speedLabel: "Geschwindigkeit",
    openBtn: "Öffnen",
    optBest: "Video - Beste Qualität (Auto / 4K / 1080p)",
    opt1080: "Video - 1080p Full HD (MP4)",
    opt720: "Video - 720p HD (MP4)",
    opt480: "Video - 480p SD (MP4)",
    opt360: "Video - 360p Mobil (MP4)",
    optMp3: "Nur Audio - MP3 Hohe Qualität (320 kbps)",
    optM4a: "Nur Audio - M4A / AAC (Standard)",
    toastPasteSuccess: "Link eingefügt! Analyse läuft...",
    toastPasteFail: "Bitte Link manuell einfügen (Strg+V)",
    toastAnalyzeSuccess: "Video erfolgreich analysiert!",
    toastDownloadSuccess: "Download erfolgreich abgeschlossen!",
    toastCancelled: "Download abgebrochen",
    toastError: "Fehler",
    toastFolderSuccess: "Ordner im Explorer geöffnet",
    toastHistoryCleared: "Sitzungsverlauf gelöscht",
    statusAnalyzing: "Streams werden analysiert und Größen berechnet...",
    statusDownloading: "Download läuft",
    statusComplete: "Download erfolgreich abgeschlossen!",
    statusCancelledMsg: "Download vom Benutzer abgebrochen.",
    statusStarting: "Download wird gestartet...",
    statusConnecting: "Verbindung zum Server...",
    statusStopping: "Wird gestoppt..."
  },
  pt: {
    subtitle: "Descarregador universal de alta velocidade • Cálculo exato do tamanho antes do download",
    themeDark: "Escuro",
    themeLight: "Claro",
    themeSystem: "Sistema",
    platformsLabel: "Plataformas:",
    inputTitle: "Colar link de vídeo ou áudio",
    readyStatus: "Pronto",
    urlPlaceholder: "Cole um link aqui (ex: YouTube, Facebook, TikTok, Instagram, Twitter/X...)",
    btnPaste: "Colar",
    btnAnalyze: "Analisar",
    btnAnalyzeLoading: "A analisar...",
    singleVideoText: "Descarregar apenas este vídeo (Evita descarregar toda a playlist)",
    previewPlaceholder: "Cole um link acima para exibir a pré-visualização e o tamanho exato",
    settingsTitle: "Opções de Download & Destino",
    formatLabel: "Formato / Resolução:",
    destLabel: "Pasta de destino:",
    btnBrowse: "Procurar...",
    statusReady: "Pronto",
    btnDownload: "DESCARREGAR AGORA",
    btnStop: "PARAR",
    btnFolder: "Pasta",
    historyTitle: "Histórico da sessão",
    btnClear: "Limpar",
    historyEmpty: "Nenhum download nesta sessão",
    authorLabel: "Autor:",
    exactSizeLabel: "Tamanho exato:",
    calculating: "A calcular...",
    unknown: "Desconhecido",
    viewsSuffix: "visualizações",
    speedLabel: "Velocidade",
    openBtn: "Abrir",
    optBest: "Vídeo - Melhor qualidade (Auto / 4K / 1080p)",
    opt1080: "Vídeo - 1080p Full HD (MP4)",
    opt720: "Vídeo - 720p HD (MP4)",
    opt480: "Vídeo - 480p SD (MP4)",
    opt360: "Vídeo - 360p Móvel (MP4)",
    optMp3: "Apenas áudio - MP3 Alta Qualidade (320 kbps)",
    optM4a: "Apenas áudio - M4A / AAC (Padrão)",
    toastPasteSuccess: "Link colado! A analisar...",
    toastPasteFail: "Por favor cole o link manualmente (Ctrl+V)",
    toastAnalyzeSuccess: "Vídeo analisado com sucesso!",
    toastDownloadSuccess: "Download concluído com sucesso!",
    toastCancelled: "Download cancelado",
    toastError: "Erro",
    toastFolderSuccess: "Pasta aberta no explorador",
    toastHistoryCleared: "Histórico de sessão limpo",
    statusAnalyzing: "A analisar fluxos e a calcular tamanhos exatos...",
    statusDownloading: "A transferir",
    statusComplete: "Download concluído com sucesso!",
    statusCancelledMsg: "Download interrompido pelo utilizador.",
    statusStarting: "A iniciar download...",
    statusConnecting: "A ligar ao servidor...",
    statusStopping: "A parar..."
  },
  ar: {
    subtitle: "أداة تحميل فائقة السرعة وشاملة • حساب الحجم الدقيق للملف قبل التحميل",
    themeDark: "داكن",
    themeLight: "فاتح",
    themeSystem: "النظام",
    platformsLabel: "المنصات:",
    inputTitle: "الصق رابط الفيديو أو الصوت",
    readyStatus: "جاهز",
    urlPlaceholder: "الصق الرابط هنا (يوتيوب، فيسبوك، تيك توك، إنستغرام، تويتر/X...)",
    btnPaste: "لصق",
    btnAnalyze: "تحليل",
    btnAnalyzeLoading: "جاري التحليل...",
    singleVideoText: "تحميل هذا الفيديو فقط (يمنع تحميل قائمة التشغيل أو الميكس كاملاً)",
    previewPlaceholder: "الصق رابطاً بالأعلى لعرض الفيديو والحجم الدقيق قبل التحميل",
    settingsTitle: "خيارات التحميل والمجلد",
    formatLabel: "الصيغة / الدقة:",
    destLabel: "مجلد الحفظ:",
    btnBrowse: "تصفح...",
    statusReady: "جاهز",
    btnDownload: "تحميل الآن",
    btnStop: "إيقاف",
    btnFolder: "المجلد",
    historyTitle: "سجل الجلسة",
    btnClear: "مسح",
    historyEmpty: "لا توجد تنزيلات في هذه الجلسة",
    authorLabel: "المؤلف:",
    exactSizeLabel: "الحجم الدقيق:",
    calculating: "جاري الحساب...",
    unknown: "غير معروف",
    viewsSuffix: "مشاهدة",
    speedLabel: "السرعة",
    openBtn: "فتح",
    optBest: "فيديو - أفضل جودة (تلقائي / 4K / 1080p)",
    opt1080: "فيديو - 1080p Full HD (MP4)",
    opt720: "فيديو - 720p HD (MP4)",
    opt480: "فيديو - 480p SD (MP4)",
    opt360: "فيديو - 360p جوال (MP4)",
    optMp3: "صوت فقط - MP3 جودة عالية (320 kbps)",
    optM4a: "صوت فقط - M4A / AAC (قياسي)",
    toastPasteSuccess: "تم لصق الرابط! جاري التحليل...",
    toastPasteFail: "يرجى لصق الرابط يدوياً (Ctrl+V)",
    toastAnalyzeSuccess: "تم تحليل الفيديو بنجاح!",
    toastDownloadSuccess: "اكتمل التحميل بنجاح!",
    toastCancelled: "تم إلغاء التحميل",
    toastError: "خطأ",
    toastFolderSuccess: "تم فتح المجلد في المستكشف",
    toastHistoryCleared: "تم مسح سجل الجلسة",
    statusAnalyzing: "جاري تحليل التدفقات وحساب الأحجام الدقيقة...",
    statusDownloading: "جاري التحميل",
    statusComplete: "اكتمل التحميل بنجاح!",
    statusCancelledMsg: "تم مقاطعة التحميل من قبل المستخدم.",
    statusStarting: "جاري بدء التحميل...",
    statusConnecting: "جاري الاتصال بالخادم...",
    statusStopping: "جاري الإيقاف..."
  }
};

// Langue courante
let currentLang = localStorage.getItem('styvedev-dl-lang') || 'fr';

function t(key) {
  const dict = TRANSLATIONS[currentLang] || TRANSLATIONS.fr;
  return dict[key] || TRANSLATIONS.fr[key] || key;
}

function applyLang(lang) {
  currentLang = lang;
  localStorage.setItem('styvedev-dl-lang', lang);

  // Direction RTL pour l'arabe
  if (lang === 'ar') {
    document.documentElement.setAttribute('dir', 'rtl');
  } else {
    document.documentElement.setAttribute('dir', 'ltr');
  }
  document.documentElement.setAttribute('lang', lang);

  // Traduction des textes avec data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (key && TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
      el.textContent = TRANSLATIONS[lang][key];
    }
  });

  // Traduction des placeholders avec data-i18n-ph
  document.querySelectorAll('[data-i18n-ph]').forEach(el => {
    const key = el.getAttribute('data-i18n-ph');
    if (key && TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
      el.placeholder = TRANSLATIONS[lang][key];
    }
  });

  // Mettre à jour les options de format
  updateFormatSelectLabels(currentVideoData ? (currentVideoData.sizes || {}) : {});

  // Mettre à jour l'aperçu si présent
  if (currentVideoData) {
    updateSizeDisplay();
    if (previewViewsText) {
      previewViewsText.textContent = formatViews(currentVideoData.view_count);
    }
    if (previewChannelText) {
      previewChannelText.textContent = `${t('authorLabel')} ${currentVideoData.uploader || t('unknown')}`;
    }
  }

  // Mettre à jour le badge de plateforme
  updatePlatformBadge(urlInput ? urlInput.value : '');

  // Mettre à jour l'historique
  renderHistory();
}

// =============================================================================
// ÉLÉMENTS DU DOM
// =============================================================================
const langSelect = document.getElementById('lang-select');
const themeSelect = document.getElementById('theme-select');
const toastEl = document.getElementById('toast');

const urlInput = document.getElementById('url-input');
const btnClear = document.getElementById('btn-clear');
const btnPaste = document.getElementById('btn-paste');
const btnAnalyze = document.getElementById('btn-analyze');
const chkSingleVideo = document.getElementById('chk-single-video');
const platformBadge = document.getElementById('platform-badge');
const platformText = document.getElementById('platform-text');

const previewPlaceholder = document.getElementById('preview-placeholder');
const previewContent = document.getElementById('preview-content');
const previewThumb = document.getElementById('preview-thumb');
const previewTitle = document.getElementById('preview-title');
const previewChannelText = document.getElementById('preview-channel-text');
const previewSizeBadge = document.getElementById('preview-size-badge');
const previewSizeText = document.getElementById('preview-size-text');
const previewPlatformBadge = document.getElementById('preview-platform-badge');
const previewPlatformIcon = document.getElementById('preview-platform-icon');
const previewPlatformText = document.getElementById('preview-platform-text');
const previewDurationText = document.getElementById('preview-duration-text');
const previewViewsText = document.getElementById('preview-views-text');

const formatSelect = document.getElementById('format-select');
const currentFormatSize = document.getElementById('current-format-size');
const destInput = document.getElementById('dest-input');
const btnBrowse = document.getElementById('btn-browse');

const btnDownload = document.getElementById('btn-download');
const btnCancel = document.getElementById('btn-cancel');
const btnOpenFolder = document.getElementById('btn-open-folder');

const statusText = document.getElementById('status-text');
const progressFill = document.getElementById('progress-fill');
const statsText = document.getElementById('stats-text');

const historyList = document.getElementById('history-list');
const btnClearHistory = document.getElementById('btn-clear-history');

// État global
let currentVideoData = null;
let selectedFormat = 'best';
let currentSocket = null;
let toastTimeout = null;

// =============================================================================
// GESTION DU THÈME
// =============================================================================
function initTheme() {
  const saved = localStorage.getItem('styvedev-dl-theme') || 'dark';
  applyTheme(saved);
  if (themeSelect) themeSelect.value = saved;

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (localStorage.getItem('styvedev-dl-theme') === 'system') {
      document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  });
}

function applyTheme(theme) {
  localStorage.setItem('styvedev-dl-theme', theme);
  if (theme === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
  } else {
    document.documentElement.setAttribute('data-theme', theme);
  }
}

themeSelect?.addEventListener('change', (e) => {
  applyTheme(e.target.value);
});

// =============================================================================
// TOAST NOTIFICATIONS
// =============================================================================
function showToast(message, type = 'info') {
  if (!toastEl) return;
  clearTimeout(toastTimeout);
  toastEl.textContent = message;
  toastEl.className = `toast show ${type}`;
  toastTimeout = setTimeout(() => {
    toastEl.classList.remove('show');
  }, 3500);
}

// =============================================================================
// DÉTECTION VECTORIELLE DE LA PLATEFORME (SANS ÉMOJIS)
// =============================================================================
function detectPlatform(url) {
  if (!url || !url.trim()) {
    return { name: t('readyStatus'), svg: SVG_ICONS.globe, color: 'var(--badge-text)' };
  }
  const u = url.toLowerCase();
  if (u.includes('youtube.com') || u.includes('youtu.be')) {
    return { name: 'YouTube', svg: SVG_ICONS.youtube, color: '#EF4444' };
  }
  if (u.includes('facebook.com') || u.includes('fb.watch') || u.includes('fb.com')) {
    return { name: 'Facebook', svg: SVG_ICONS.facebook, color: '#1877F2' };
  }
  if (u.includes('instagram.com')) {
    return { name: 'Instagram', svg: SVG_ICONS.instagram, color: '#E1306C' };
  }
  if (u.includes('tiktok.com')) {
    return { name: 'TikTok', svg: SVG_ICONS.tiktok, color: '#00F2FE' };
  }
  if (u.includes('twitter.com') || u.includes('x.com')) {
    return { name: 'Twitter / X', svg: SVG_ICONS.twitter, color: '#A1A1AA' };
  }
  if (u.includes('twitch.tv')) {
    return { name: 'Twitch', svg: SVG_ICONS.twitch, color: '#9146FF' };
  }
  if (u.includes('reddit.com')) {
    return { name: 'Reddit', svg: SVG_ICONS.reddit, color: '#FF4500' };
  }
  if (u.includes('vimeo.com')) {
    return { name: 'Vimeo', svg: SVG_ICONS.vimeo, color: '#1AB7EA' };
  }
  if (u.includes('dailymotion.com')) {
    return { name: 'Dailymotion', svg: SVG_ICONS.dailymotion, color: '#0066DC' };
  }
  return { name: 'Web', svg: SVG_ICONS.globe, color: '#3B82F6' };
}

function updatePlatformBadge(url) {
  const p = detectPlatform(url);
  if (platformBadge) {
    platformBadge.innerHTML = `${p.svg}<span>${p.name}</span>`;
    platformBadge.style.color = p.color;
  }
}

function cleanInputUrl(url) {
  let cleaned = (url || '').trim();
  if (chkSingleVideo?.checked) {
    if ((cleaned.includes('youtube.com/watch') || cleaned.includes('m.youtube.com/watch')) && cleaned.includes('v=')) {
      const match = cleaned.match(/[?&]v=([a-zA-Z0-9_-]{11})/);
      if (match) return `https://www.youtube.com/watch?v=${match[1]}`;
    }
    if (cleaned.includes('youtu.be/')) {
      const match = cleaned.match(/youtu\.be\/([a-zA-Z0-9_-]{11})/);
      if (match) return `https://www.youtube.com/watch?v=${match[1]}`;
    }
    if (cleaned.includes('&list=')) {
      cleaned = cleaned.split('&list=')[0];
    }
  }
  return cleaned;
}

urlInput?.addEventListener('input', () => {
  updatePlatformBadge(urlInput.value);
});

btnClear?.addEventListener('click', () => {
  if (urlInput) urlInput.value = '';
  updatePlatformBadge('');
  resetPreview();
  if (urlInput) urlInput.focus();
});

btnPaste?.addEventListener('click', async () => {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      urlInput.value = text.trim();
      updatePlatformBadge(urlInput.value);
      showToast(t('toastPasteSuccess'), 'info');
      analyzeUrl();
    }
  } catch (err) {
    showToast(t('toastPasteFail'), 'error');
  }
});

// =============================================================================
// FORMATAGE DES DURÉES ET VUES (SANS ÉMOJIS)
// =============================================================================
function formatDuration(seconds) {
  if (!seconds || seconds <= 0) return '00:00';
  const s = Math.floor(seconds);
  const hrs = Math.floor(s / 3600);
  const mins = Math.floor((s % 3600) / 60);
  const secs = s % 60;
  if (hrs > 0) {
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

function formatViews(n) {
  const suffix = t('viewsSuffix');
  if (!n || n <= 0) return `0 ${suffix}`;
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M ${suffix}`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k ${suffix}`;
  return `${n} ${suffix}`;
}

// =============================================================================
// ANALYSE DE L'URL & CALCUL DE TAILLE EXACTE
// =============================================================================
async function analyzeUrl() {
  const rawUrl = urlInput.value.trim();
  const url = cleanInputUrl(rawUrl);

  if (!url) {
    showToast(t('toastPasteFail'), 'error');
    urlInput.focus();
    return;
  }

  btnAnalyze.disabled = true;
  btnAnalyze.innerHTML = `
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16" style="animation:spin 1s linear infinite;"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg>
    <span>${t('btnAnalyzeLoading')}</span>
  `;
  statusText.textContent = t('statusAnalyzing');

  try {
    const res = await fetch(`${API_BASE}/api/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Erreur serveur' }));
      throw new Error(err.detail || `Erreur HTTP ${res.status}`);
    }

    const data = await res.json();
    currentVideoData = data;

    renderPreview(data);
    updateFormatSelectLabels(data.sizes || {});

    btnDownload.disabled = false;
    statusText.textContent = `${t('statusReady')} : ${data.title}`;
    showToast(t('toastAnalyzeSuccess'), 'success');

  } catch (err) {
    console.error('Erreur analyse:', err);
    showToast(`${t('toastError')}: ${err.message}`, 'error');
    statusText.textContent = `${t('toastError')}: ${err.message}`;
  } finally {
    btnAnalyze.disabled = false;
    btnAnalyze.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="16" height="16"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      <span data-i18n="btnAnalyze">${t('btnAnalyze')}</span>
    `;
  }
}

btnAnalyze?.addEventListener('click', analyzeUrl);

urlInput?.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') analyzeUrl();
});

function renderPreview(data) {
  previewPlaceholder.style.display = 'none';
  previewContent.style.display = 'flex';

  previewThumb.src = data.thumbnail || '/icons/icon-192.png';
  previewThumb.onerror = () => { previewThumb.src = '/icons/icon-192.png'; };
  previewTitle.textContent = data.title || 'Média sans titre';
  
  if (previewChannelText) {
    previewChannelText.textContent = `${t('authorLabel')} ${data.uploader || t('unknown')}`;
  }
  if (previewDurationText) {
    previewDurationText.textContent = formatDuration(data.duration);
  }
  if (previewViewsText) {
    previewViewsText.textContent = formatViews(data.view_count);
  }

  const p = detectPlatform(data.url);
  if (previewPlatformIcon) previewPlatformIcon.innerHTML = p.svg;
  if (previewPlatformText) previewPlatformText.textContent = p.name;
  if (previewPlatformBadge) previewPlatformBadge.style.color = p.color;

  updateSizeDisplay();
}

function resetPreview() {
  currentVideoData = null;
  previewPlaceholder.style.display = 'block';
  previewContent.style.display = 'none';
  btnDownload.disabled = true;
  statusText.textContent = t('statusReady');
  statsText.textContent = '0.0 Mo / 0.0 Mo • 0.0 Mo/s • ETA: --:--';
  if (currentFormatSize) currentFormatSize.textContent = '--';
  resetFormatSelectLabels();
}

function updateFormatSelectLabels(sizes) {
  const formatMap = {
    best: t('optBest'),
    '1080p': t('opt1080'),
    '720p': t('opt720'),
    '480p': t('opt480'),
    '360p': t('opt360'),
    mp3: t('optMp3'),
    m4a: t('optM4a')
  };

  const options = formatSelect.options;
  for (let i = 0; i < options.length; i++) {
    const val = options[i].value;
    const baseText = formatMap[val] || options[i].text.split(' [')[0];
    if (sizes && sizes[val] && sizes[val].human) {
      options[i].text = `${baseText} [${sizes[val].human}]`;
    } else {
      options[i].text = baseText;
    }
  }
  updateSizeDisplay();
}

function resetFormatSelectLabels() {
  updateFormatSelectLabels({});
}

function updateSizeDisplay() {
  if (!currentVideoData || !currentVideoData.sizes) return;
  const s = currentVideoData.sizes[selectedFormat];
  const sizeText = s && s.human ? s.human : (currentVideoData.sizes['best']?.human || t('calculating'));
  if (currentFormatSize) currentFormatSize.textContent = sizeText;
  if (previewSizeText) previewSizeText.textContent = `${t('exactSizeLabel')} ${sizeText}`;
}

formatSelect?.addEventListener('change', (e) => {
  selectedFormat = e.target.value;
  updateSizeDisplay();
});

// =============================================================================
// TÉLÉCHARGEMENT TEMPS RÉEL (WEBSOCKET & STOP INSTANTANÉ)
// =============================================================================
function startDownload() {
  const rawUrl = urlInput.value.trim();
  const url = cleanInputUrl(rawUrl);

  if (!url) {
    showToast(t('toastPasteFail'), 'error');
    return;
  }

  btnDownload.disabled = true;
  btnCancel.disabled = false;
  btnAnalyze.disabled = true;
  urlInput.disabled = true;

  progressFill.style.width = '0%';
  statusText.textContent = t('statusStarting');
  statsText.textContent = t('statusConnecting');

  try {
    currentSocket = new WebSocket(WS_BASE);

    currentSocket.onopen = () => {
      const payload = {
        url: url,
        format: selectedFormat
      };
      currentSocket.send(JSON.stringify(payload));
    };

    currentSocket.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        handleSocketMessage(msg);
      } catch (err) {
        console.error('Erreur lecture websocket message:', err);
      }
    };

    currentSocket.onerror = () => {
      statusText.textContent = `${t('toastError')}: WebSocket`;
      showToast(`${t('toastError')}: Communication WebSocket`, 'error');
      resetDownloadState();
    };

    currentSocket.onclose = () => {
      if (btnCancel && !btnCancel.disabled) {
        resetDownloadState();
      }
    };

  } catch (err) {
    showToast(`${t('toastError')}: ${err.message}`, 'error');
    resetDownloadState();
  }
}

function handleSocketMessage(msg) {
  switch (msg.type) {
    case 'status':
      statusText.textContent = msg.message;
      break;

    case 'progress':
      const percent = Math.min(100, Math.max(0, msg.percent || 0));
      progressFill.style.width = `${percent}%`;
      statusText.textContent = `${t('statusDownloading')} : ${percent}%`;
      statsText.textContent = `${msg.downloaded} / ${msg.total} • ${t('speedLabel')}: ${msg.speed} • ETA: ${msg.eta}s`;
      break;

    case 'done':
      progressFill.style.width = '100%';
      statusText.textContent = t('statusComplete');
      statsText.textContent = `${msg.filename}`;
      showToast(t('toastDownloadSuccess'), 'success');
      addToHistory({
        title: currentVideoData?.title || msg.filename,
        filename: msg.filename,
        format: selectedFormat,
        date: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      });

      // Téléchargement / sauvegarde automatique du fichier
      try {
        const fileUrl = `${API_BASE}/files/${encodeURIComponent(msg.filename)}`;
        const a = document.createElement('a');
        a.href = fileUrl;
        a.download = msg.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (err) {
        console.warn('Auto-save err:', err);
      }

      btnOpenFolder.disabled = false;
      resetDownloadState();
      break;

    case 'cancelled':
      statusText.textContent = t('statusCancelledMsg');
      statsText.textContent = t('statusCancelledMsg');
      showToast(t('toastCancelled'), 'info');
      resetDownloadState();
      break;

    case 'error':
      statusText.textContent = `${t('toastError')}: ${msg.message}`;
      statsText.textContent = msg.message;
      showToast(`${t('toastError')}: ${msg.message}`, 'error');
      resetDownloadState();
      break;
  }
}

function stopDownload() {
  if (currentSocket) {
    statusText.textContent = t('statusStopping');
    currentSocket.close();
    currentSocket = null;
  }
  showToast(t('toastCancelled'), 'info');
  resetDownloadState();
}

function resetDownloadState() {
  btnDownload.disabled = false;
  btnCancel.disabled = true;
  btnAnalyze.disabled = false;
  urlInput.disabled = false;
  currentSocket = null;
}

btnDownload?.addEventListener('click', startDownload);
btnCancel?.addEventListener('click', stopDownload);

// =============================================================================
// OUVRIR DOSSIER ET PARCOURIR
// =============================================================================
btnOpenFolder?.addEventListener('click', async () => {
  try {
    const res = await fetch(`${API_BASE}/api/open-folder`, { method: 'POST' });
    if (res.ok) {
      showToast(t('toastFolderSuccess'), 'success');
    }
  } catch (e) {
    showToast(destInput ? destInput.value : '', 'info');
  }
});

btnBrowse?.addEventListener('click', () => {
  showToast(destInput ? destInput.value : 'Downloads', 'info');
});

// =============================================================================
// HISTORIQUE DE SESSION AVEC VRAIS ICONES VECTORIELLES
// =============================================================================
function loadHistory() {
  try {
    const raw = sessionStorage.getItem('styvedev-dl-history');
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveHistory(list) {
  try {
    sessionStorage.setItem('styvedev-dl-history', JSON.stringify(list.slice(0, 10)));
  } catch (e) {}
}

function addToHistory(item) {
  const list = loadHistory();
  list.unshift(item);
  saveHistory(list);
  renderHistory();
}

function renderHistory() {
  const list = loadHistory();
  if (!historyList) return;

  if (list.length === 0) {
    historyList.innerHTML = `<div class="history-empty" data-i18n="historyEmpty">${t('historyEmpty')}</div>`;
    return;
  }

  historyList.innerHTML = '';
  list.forEach(item => {
    const el = document.createElement('div');
    el.className = 'history-item';
    const isAudio = item.format === 'mp3' || item.format === 'm4a';
    const iconSvg = isAudio ? SVG_ICONS.music : SVG_ICONS.video;

    el.innerHTML = `
      <span class="history-icon">${iconSvg}</span>
      <div class="history-name" title="${item.filename || item.title}">
        <div><strong>${item.title}</strong></div>
        <div style="font-size:0.7rem; color:var(--text-muted);">${item.format.toUpperCase()} • ${item.date}</div>
      </div>
      <button class="btn-open" onclick="openFile('${encodeURIComponent(item.filename)}')">
        ${SVG_ICONS.openFile}
        <span>${t('openBtn')}</span>
      </button>
    `;
    historyList.appendChild(el);
  });
}

window.openFile = (filename) => {
  const fileUrl = `${API_BASE}/files/${filename}`;
  const a = document.createElement('a');
  a.href = fileUrl;
  a.download = decodeURIComponent(filename);
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

btnClearHistory?.addEventListener('click', () => {
  sessionStorage.removeItem('styvedev-dl-history');
  renderHistory();
  showToast(t('toastHistoryCleared'), 'info');
});

// =============================================================================
// INFO SANTÉ SERVEUR & DOSSIER DESTINATION
// =============================================================================
async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (res.ok) {
      const data = await res.json();
      if (data.downloads_dir && destInput) {
        destInput.value = data.downloads_dir;
      }
    }
  } catch (err) {
    console.warn('Serveur en cours d’initialisation');
  }
}

// =============================================================================
// GESTION DU SÉLECTEUR DE LANGUE
// =============================================================================
langSelect?.addEventListener('change', (e) => {
  applyLang(e.target.value);
});

// =============================================================================
// SERVICE WORKER PWA
// =============================================================================
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(err => {
      console.warn('Service Worker non actif en HTTP local');
    });
  });
}

// =============================================================================
// INITIALISATION AU CHARGEMENT DE LA PAGE
// =============================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Synchroniser la sélection de langue
  if (langSelect) langSelect.value = currentLang;
  applyLang(currentLang);

  // Initialiser le thème
  initTheme();

  // Initialiser l'historique et la santé du serveur
  renderHistory();
  checkHealth();

  // Initialiser le badge de plateforme
  updatePlatformBadge('');
});
