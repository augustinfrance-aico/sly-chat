// AVATARS SVG — 25 agents style bitmoji humain
// Chaque avatar = visage unique avec couleur de peau, coiffure, accessoires

const AVATARS = {

  OMEGA: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <!-- Fond cercle -->
    <circle cx="40" cy="40" r="38" fill="#1a1a2e"/>
    <!-- Cou -->
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c68642"/>
    <!-- Visage -->
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c68642"/>
    <!-- Cheveux noirs courts texturés -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#1a0a00"/>
    <rect x="22" y="24" width="36" height="8" rx="4" fill="#1a0a00"/>
    <!-- Sourcils épais -->
    <rect x="26" y="34" width="10" height="3" rx="2" fill="#0d0700"/>
    <rect x="44" y="34" width="10" height="3" rx="2" fill="#0d0700"/>
    <!-- Yeux perçants -->
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="3" fill="#7c3aed"/>
    <circle cx="49" cy="40" r="3" fill="#7c3aed"/>
    <circle cx="32" cy="39" r="1" fill="white"/>
    <circle cx="50" cy="39" r="1" fill="white"/>
    <!-- Nez -->
    <ellipse cx="40" cy="46" rx="3" ry="2" fill="#b5732a"/>
    <!-- Sourire confiant -->
    <path d="M32 52 Q40 58 48 52" stroke="#7a4a1a" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Cicatrice sourcil gauche — detail Omega -->
    <line x1="26" y1="33" x2="30" y2="37" stroke="#a05a20" stroke-width="1.5"/>
  </svg>`,

  MURPHY: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a2a1a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#f4c17a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#f4c17a"/>
    <!-- Cheveux roux courts côté -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#8B3A0F"/>
    <rect x="22" y="24" width="36" height="9" rx="4" fill="#8B3A0F"/>
    <!-- Lunettes rectangulaires -->
    <rect x="24" y="36" width="12" height="9" rx="2" fill="none" stroke="#333" stroke-width="2"/>
    <rect x="44" y="36" width="12" height="9" rx="2" fill="none" stroke="#333" stroke-width="2"/>
    <line x1="36" y1="40" x2="44" y2="40" stroke="#333" stroke-width="1.5"/>
    <!-- Yeux derrière lunettes -->
    <ellipse cx="30" cy="40" rx="3.5" ry="3.5" fill="#2563eb"/>
    <circle cx="31" cy="39" r="1" fill="white"/>
    <ellipse cx="50" cy="40" rx="3.5" ry="3.5" fill="#2563eb"/>
    <circle cx="51" cy="39" r="1" fill="white"/>
    <!-- Sourcils sérieux -->
    <rect x="25" y="33" width="10" height="2.5" rx="1" fill="#6B2D0F"/>
    <rect x="45" y="33" width="10" height="2.5" rx="1" fill="#6B2D0F"/>
    <!-- Nez -->
    <ellipse cx="40" cy="46" rx="2.5" ry="2" fill="#e0a85a"/>
    <!-- Expression neutre déterminée -->
    <line x1="32" y1="52" x2="48" y2="52" stroke="#c07a3a" stroke-width="2" stroke-linecap="round"/>
    <!-- Barbe courte roux -->
    <ellipse cx="40" cy="56" rx="12" ry="4" fill="#8B3A0F" opacity="0.4"/>
  </svg>`,

  PHILOMENE: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#2a0a2a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#e8b89a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#e8b89a"/>
    <!-- Chignon élégant -->
    <ellipse cx="40" cy="24" rx="16" ry="9" fill="#2d1b00"/>
    <circle cx="40" cy="17" r="7" fill="#2d1b00"/>
    <circle cx="40" cy="17" r="4" fill="#db2777" opacity="0.6"/>
    <!-- Boucles d'oreilles perles -->
    <circle cx="22" cy="44" r="3" fill="#fff" stroke="#db2777" stroke-width="1"/>
    <circle cx="58" cy="44" r="3" fill="#fff" stroke="#db2777" stroke-width="1"/>
    <!-- Yeux en amande avec mascara -->
    <ellipse cx="31" cy="40" rx="6" ry="4" fill="white"/>
    <ellipse cx="49" cy="40" rx="6" ry="4" fill="white"/>
    <ellipse cx="31" cy="40" rx="4" ry="3" fill="#2d1b00"/>
    <ellipse cx="49" cy="40" rx="4" ry="3" fill="#2d1b00"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Eyeliner -->
    <path d="M25 38 Q31 35 37 38" stroke="#1a0a00" stroke-width="1.5" fill="none"/>
    <path d="M43 38 Q49 35 55 38" stroke="#1a0a00" stroke-width="1.5" fill="none"/>
    <!-- Sourcils arqués -->
    <path d="M26 34 Q31 31 36 34" stroke="#2d1b00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M44 34 Q49 31 54 34" stroke="#2d1b00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- Rouge à lèvres -->
    <path d="M33 51 Q40 56 47 51" stroke="#db2777" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M33 51 Q36 49 40 50 Q44 49 47 51" stroke="#db2777" stroke-width="1.5" fill="#db2777" opacity="0.6"/>
  </svg>`,

  RICK: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a1500"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4956a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#d4956a"/>
    <!-- Cheveux gominés en arrière -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#1a0a00"/>
    <path d="M22 26 Q40 18 58 26 L58 22 Q40 12 22 22 Z" fill="#1a0a00"/>
    <!-- Sourcils sûrs de lui -->
    <path d="M26 35 Q31 33 36 35" stroke="#1a0a00" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M44 35 Q49 33 54 35" stroke="#1a0a00" stroke-width="3" fill="none" stroke-linecap="round"/>
    <!-- Yeux malins -->
    <ellipse cx="31" cy="41" rx="5" ry="4.5" fill="white"/>
    <ellipse cx="49" cy="41" rx="5" ry="4.5" fill="white"/>
    <ellipse cx="31" cy="41" rx="3.5" ry="3.5" fill="#f59e0b"/>
    <ellipse cx="49" cy="41" rx="3.5" ry="3.5" fill="#f59e0b"/>
    <circle cx="32" cy="40" r="1.2" fill="white"/>
    <circle cx="50" cy="40" r="1.2" fill="white"/>
    <!-- Nez aquilin -->
    <path d="M38 44 L40 48 L42 44" stroke="#b5732a" stroke-width="1.5" fill="none"/>
    <!-- Sourire d'un vendeur -->
    <path d="M31 52 Q40 59 49 52" stroke="#8B4513" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Dents visibles -->
    <path d="M33 53 Q40 58 47 53 L47 55 Q40 59 33 55 Z" fill="white" opacity="0.8"/>
    <!-- Fossettes -->
    <circle cx="29" cy="51" r="2" fill="#c07a3a" opacity="0.4"/>
    <circle cx="51" cy="51" r="2" fill="#c07a3a" opacity="0.4"/>
  </svg>`,

  NIKOLA: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#001a2a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8a882"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8a882"/>
    <!-- Cheveux foncés mi-longs désordonnés -->
    <ellipse cx="40" cy="26" rx="19" ry="11" fill="#1a0a00"/>
    <path d="M21 30 Q24 20 30 18 Q40 15 50 18 Q56 20 59 30" fill="#1a0a00"/>
    <path d="M21 30 Q19 38 22 44" fill="#1a0a00"/>
    <path d="M59 30 Q61 38 58 44" fill="#1a0a00"/>
    <!-- Yeux intelligents légèrement fatigués -->
    <ellipse cx="31" cy="40" rx="5.5" ry="4" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="4" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3" fill="#06b6d4"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3" fill="#06b6d4"/>
    <circle cx="32" cy="39" r="1" fill="white"/>
    <circle cx="50" cy="39" r="1" fill="white"/>
    <!-- Cernes légers (travaille la nuit) -->
    <ellipse cx="31" cy="43" rx="6" ry="2" fill="#a07050" opacity="0.3"/>
    <ellipse cx="49" cy="43" rx="6" ry="2" fill="#a07050" opacity="0.3"/>
    <!-- Sourcils concentrés -->
    <path d="M26 34 Q31 32 36 34" stroke="#1a0a00" stroke-width="2.5" fill="none"/>
    <path d="M44 34 Q49 32 54 34" stroke="#1a0a00" stroke-width="2.5" fill="none"/>
    <!-- Nez fin -->
    <ellipse cx="40" cy="46" rx="2.5" ry="2" fill="#b08860"/>
    <!-- Sourire discret -->
    <path d="M34 52 Q40 56 46 52" stroke="#907040" stroke-width="1.5" fill="none" stroke-linecap="round"/>
  </svg>`,

  STANLEY: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#001a0a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#8B4513"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#8B4513"/>
    <!-- Crâne rasé propre -->
    <ellipse cx="40" cy="28" rx="18" ry="10" fill="#5C2D0A"/>
    <!-- Barbe courte taillée -->
    <ellipse cx="40" cy="57" rx="14" ry="5" fill="#3d1a05" opacity="0.7"/>
    <ellipse cx="40" cy="54" rx="12" ry="3" fill="#3d1a05" opacity="0.5"/>
    <!-- Yeux chaleureux -->
    <ellipse cx="31" cy="40" rx="5" ry="4.5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="4.5" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3.5" fill="#10b981"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3.5" fill="#10b981"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils épais naturels -->
    <rect x="26" y="33" width="10" height="3" rx="2" fill="#3d1a05"/>
    <rect x="44" y="33" width="10" height="3" rx="2" fill="#3d1a05"/>
    <!-- Grand sourire -->
    <path d="M30 52 Q40 60 50 52" stroke="#5C2D0A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M32 53 Q40 59 48 53 L48 56 Q40 61 32 56 Z" fill="white" opacity="0.7"/>
  </svg>`,

  VITO: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a0a1a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8a882"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8a882"/>
    <!-- Cheveux gris argent peignés -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#888"/>
    <rect x="22" y="24" width="36" height="8" rx="4" fill="#888"/>
    <!-- Tempes grises distinctives -->
    <ellipse cx="23" cy="36" rx="5" ry="8" fill="#aaa"/>
    <ellipse cx="57" cy="36" rx="5" ry="8" fill="#aaa"/>
    <!-- Ride front (60 ans) -->
    <path d="M28 32 Q40 30 52 32" stroke="#b09060" stroke-width="1" fill="none" opacity="0.5"/>
    <!-- Yeux perçants foncés -->
    <ellipse cx="31" cy="40" rx="5" ry="4" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="4" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3" fill="#1e3a5f"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3" fill="#1e3a5f"/>
    <circle cx="32" cy="39" r="1" fill="white"/>
    <circle cx="50" cy="39" r="1" fill="white"/>
    <!-- Sourcils gris sévères -->
    <path d="M25 34 Q31 32 37 34" stroke="#666" stroke-width="3" fill="none"/>
    <path d="M43 34 Q49 32 55 34" stroke="#666" stroke-width="3" fill="none"/>
    <!-- Nez aristocratique -->
    <path d="M38 44 L40 50 L42 44" stroke="#b09060" stroke-width="2" fill="none"/>
    <!-- Expression grave/sage -->
    <line x1="32" y1="53" x2="48" y2="53" stroke="#a07840" stroke-width="2" stroke-linecap="round"/>
  </svg>`,

  MAYA: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0a2a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#7B3F00"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#7B3F00"/>
    <!-- Tresses/locks naturels -->
    <ellipse cx="40" cy="24" rx="19" ry="11" fill="#1a0800"/>
    <rect x="21" y="22" width="5" height="25" rx="2.5" fill="#1a0800"/>
    <rect x="27" y="20" width="5" height="30" rx="2.5" fill="#1a0800"/>
    <rect x="48" y="20" width="5" height="30" rx="2.5" fill="#1a0800"/>
    <rect x="54" y="22" width="5" height="25" rx="2.5" fill="#1a0800"/>
    <!-- Yeux vifs -->
    <ellipse cx="31" cy="40" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3.5" fill="#7c2d92"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3.5" fill="#7c2d92"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils naturels épais -->
    <path d="M26 34 Q31 31 36 34" stroke="#1a0800" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <path d="M44 34 Q49 31 54 34" stroke="#1a0800" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <!-- Boucles d'oreilles créoles -->
    <circle cx="22" cy="44" r="4" fill="none" stroke="#d4af37" stroke-width="2"/>
    <circle cx="58" cy="44" r="4" fill="none" stroke="#d4af37" stroke-width="2"/>
    <!-- Sourire décidé -->
    <path d="M33 52 Q40 57 47 52" stroke="#5a2a00" stroke-width="2" fill="none" stroke-linecap="round"/>
  </svg>`,

  BASQUIAT: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0a00"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#3d1a00"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#3d1a00"/>
    <!-- Dreads explosifs dans tous les sens -->
    <line x1="40" y1="23" x2="35" y2="8" stroke="#1a0a00" stroke-width="4" stroke-linecap="round"/>
    <line x1="40" y1="23" x2="42" y2="6" stroke="#1a0a00" stroke-width="4" stroke-linecap="round"/>
    <line x1="40" y1="23" x2="50" y2="10" stroke="#1a0a00" stroke-width="4" stroke-linecap="round"/>
    <line x1="40" y1="23" x2="30" y2="10" stroke="#1a0a00" stroke-width="4" stroke-linecap="round"/>
    <line x1="40" y1="23" x2="55" y2="16" stroke="#1a0a00" stroke-width="3" stroke-linecap="round"/>
    <line x1="40" y1="23" x2="25" y2="16" stroke="#1a0a00" stroke-width="3" stroke-linecap="round"/>
    <ellipse cx="40" cy="28" rx="16" ry="9" fill="#1a0a00"/>
    <!-- Tache de peinture rouge sur le front -->
    <circle cx="36" cy="30" r="3" fill="#dc2626" opacity="0.8"/>
    <!-- Yeux intenses artistiques -->
    <ellipse cx="31" cy="41" rx="5.5" ry="5" fill="white"/>
    <ellipse cx="49" cy="41" rx="5.5" ry="5" fill="white"/>
    <ellipse cx="31" cy="41" rx="4" ry="4" fill="#dc2626"/>
    <ellipse cx="49" cy="41" rx="4" ry="4" fill="#dc2626"/>
    <circle cx="32" cy="40" r="1.5" fill="white"/>
    <circle cx="50" cy="40" r="1.5" fill="white"/>
    <!-- Sourcils épais naturels -->
    <rect x="25" y="33" width="12" height="4" rx="2" fill="#0d0500"/>
    <rect x="43" y="33" width="12" height="4" rx="2" fill="#0d0500"/>
    <!-- Sourire décalé -->
    <path d="M32 52 Q38 57 48 51" stroke="#2a0d00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  </svg>`,

  ZARA: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0a00"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8855a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8855a"/>
    <!-- Cheveux longs hijab stylé -->
    <ellipse cx="40" cy="24" rx="20" ry="12" fill="#f97316"/>
    <rect x="20" y="30" width="40" height="18" rx="4" fill="#f97316"/>
    <ellipse cx="40" cy="48" rx="20" ry="6" fill="#f97316"/>
    <!-- Visage arrondi sympathique -->
    <!-- Yeux en amande expressifs -->
    <ellipse cx="31" cy="40" rx="5.5" ry="4" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="4" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3" fill="#1a0a00"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3" fill="#1a0a00"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils bien dessinés -->
    <path d="M26 35 Q31 32 36 35" stroke="#1a0a00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M44 35 Q49 32 54 35" stroke="#1a0a00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- Nez petit -->
    <ellipse cx="40" cy="46" rx="2.5" ry="2" fill="#b06040"/>
    <!-- Grand sourire chaleureux -->
    <path d="M31 52 Q40 59 49 52" stroke="#9a5030" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M33 53 Q40 58 47 53 L47 55 Q40 60 33 55Z" fill="white" opacity="0.8"/>
  </svg>`,

  GRIMALDI: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a1a2a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4b896"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#d4b896"/>
    <!-- Cheveux blancs impeccables -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#ccc"/>
    <rect x="22" y="24" width="36" height="8" rx="4" fill="#ccc"/>
    <!-- Lunettes fines cerclées or -->
    <rect x="24" y="36" width="11" height="8" rx="2" fill="none" stroke="#d4af37" stroke-width="1.5"/>
    <rect x="45" y="36" width="11" height="8" rx="2" fill="none" stroke="#d4af37" stroke-width="1.5"/>
    <line x1="35" y1="40" x2="45" y2="40" stroke="#d4af37" stroke-width="1.5"/>
    <!-- Yeux froids bleus acier -->
    <ellipse cx="30" cy="40" rx="3.5" ry="3" fill="#708090"/>
    <ellipse cx="51" cy="40" rx="3.5" ry="3" fill="#708090"/>
    <circle cx="31" cy="39" r="1" fill="white"/>
    <circle cx="52" cy="39" r="1" fill="white"/>
    <!-- Sourcils gris sévères -->
    <rect x="24" y="33" width="11" height="2.5" rx="1" fill="#999"/>
    <rect x="45" y="33" width="11" height="2.5" rx="1" fill="#999"/>
    <!-- Rides légères (45 ans) -->
    <path d="M26 30 Q40 28 54 30" stroke="#c0a080" stroke-width="0.8" fill="none" opacity="0.4"/>
    <!-- Expression neutre absolue -->
    <line x1="32" y1="53" x2="48" y2="53" stroke="#c0a080" stroke-width="2" stroke-linecap="round"/>
  </svg>`,

  LEON: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a1a0a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#f0d0a8"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#f0d0a8"/>
    <!-- Cheveux brun-roux ondulés -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#8B4513"/>
    <rect x="22" y="24" width="36" height="9" rx="5" fill="#8B4513"/>
    <!-- Quelques mèches rebelles -->
    <path d="M36 22 Q38 17 40 20" stroke="#6B2D0F" stroke-width="3" fill="none" stroke-linecap="round"/>
    <!-- Lunettes rondes écaille -->
    <circle cx="31" cy="40" r="7" fill="none" stroke="#8B6914" stroke-width="2"/>
    <circle cx="49" cy="40" r="7" fill="none" stroke="#8B6914" stroke-width="2"/>
    <line x1="38" y1="40" x2="42" y2="40" stroke="#8B6914" stroke-width="1.5"/>
    <!-- Yeux verts derrière lunettes -->
    <ellipse cx="31" cy="40" rx="4" ry="3.5" fill="#2E8B57"/>
    <ellipse cx="49" cy="40" rx="4" ry="3.5" fill="#2E8B57"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils professoral -->
    <path d="M25 33 Q31 31 37 33" stroke="#6B2D0F" stroke-width="2.5" fill="none"/>
    <path d="M43 33 Q49 31 55 33" stroke="#6B2D0F" stroke-width="2.5" fill="none"/>
    <!-- Hocher la tête pensif — léger sourire -->
    <path d="M33 52 Q40 56 47 52" stroke="#c0904a" stroke-width="2" fill="none" stroke-linecap="round"/>
  </svg>`,

  SPARTAN: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0000"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8956a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8956a"/>
    <!-- Cheveux noirs militaires très courts -->
    <ellipse cx="40" cy="27" rx="18" ry="9" fill="#0d0500"/>
    <rect x="22" y="25" width="36" height="7" rx="2" fill="#0d0500"/>
    <!-- Cicatrice fine sourcil gauche -->
    <line x1="26" y1="33" x2="30" y2="38" stroke="#a06040" stroke-width="1.5"/>
    <!-- Mâchoire carrée musclée -->
    <path d="M22 50 Q22 60 40 63 Q58 60 58 50" fill="#c8956a"/>
    <!-- Yeux intenses noisette -->
    <ellipse cx="31" cy="40" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3.5" fill="#8B4513"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3.5" fill="#8B4513"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils très épais droits -->
    <rect x="25" y="32" width="12" height="4" rx="1" fill="#0d0500"/>
    <rect x="43" y="32" width="12" height="4" rx="1" fill="#0d0500"/>
    <!-- Expression sérieuse/intense -->
    <line x1="31" y1="53" x2="49" y2="53" stroke="#9a6040" stroke-width="2.5" stroke-linecap="round"/>
    <!-- Barbe courte noire -->
    <ellipse cx="40" cy="58" rx="14" ry="5" fill="#0d0500" opacity="0.5"/>
  </svg>`,

  ORACLE: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a001a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8956a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8956a"/>
    <!-- Cheveux grisonnants élégants -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#555"/>
    <rect x="22" y="24" width="36" height="9" rx="4" fill="#555"/>
    <!-- Foulard en tissu persan sur les épaules -->
    <path d="M22 56 Q40 52 58 56 Q58 70 40 72 Q22 70 22 56Z" fill="#4B0082" opacity="0.7"/>
    <!-- Yeux perçants bruns profonds -->
    <ellipse cx="31" cy="40" rx="5.5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="5" fill="white"/>
    <ellipse cx="31" cy="40" rx="4" ry="4" fill="#4B0082"/>
    <ellipse cx="49" cy="40" rx="4" ry="4" fill="#4B0082"/>
    <circle cx="32" cy="39" r="1.5" fill="white"/>
    <circle cx="50" cy="39" r="1.5" fill="white"/>
    <!-- Petit sourire énigmatique -->
    <path d="M34 52 Q40 55 46 52" stroke="#a07040" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <!-- Sourcils arqués pensifs -->
    <path d="M26 33 Q31 30 36 33" stroke="#333" stroke-width="2.5" fill="none"/>
    <path d="M44 33 Q49 30 54 33" stroke="#333" stroke-width="2.5" fill="none"/>
    <!-- Ridules coins yeux (46 ans, beaucoup lu) -->
    <path d="M36 43 Q38 45 40 43" stroke="#b08060" stroke-width="0.8" fill="none" opacity="0.5"/>
  </svg>`,

  NASH: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#000a1a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4b090"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#d4b090"/>
    <!-- Cheveux noirs épais légèrement désordonnés -->
    <ellipse cx="40" cy="25" rx="19" ry="11" fill="#0d0500"/>
    <path d="M23 28 Q26 18 34 16 Q40 14 46 16 Q54 18 57 28" fill="#0d0500"/>
    <!-- Mèche sur le front -->
    <path d="M36 22 Q38 28 40 25 Q42 22 44 28" fill="#0d0500"/>
    <!-- Lunettes épaisses noires emblématiques -->
    <rect x="22" y="35" width="14" height="11" rx="3" fill="none" stroke="#111" stroke-width="3"/>
    <rect x="44" y="35" width="14" height="11" rx="3" fill="none" stroke="#111" stroke-width="3"/>
    <line x1="36" y1="40" x2="44" y2="40" stroke="#111" stroke-width="2.5"/>
    <!-- Yeux concentrés -->
    <ellipse cx="29" cy="40" rx="4" ry="3.5" fill="#1a237e"/>
    <ellipse cx="51" cy="40" rx="4" ry="3.5" fill="#1a237e"/>
    <circle cx="30" cy="39" r="1.2" fill="white"/>
    <circle cx="52" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils concentrés -->
    <rect x="23" y="32" width="13" height="3" rx="1.5" fill="#0d0500"/>
    <rect x="44" y="32" width="13" height="3" rx="1.5" fill="#0d0500"/>
    <!-- Doigts qui tapotent (implication) — post-it sur col -->
    <rect x="52" y="52" width="10" height="8" rx="1" fill="#fef08a" opacity="0.8"/>
    <line x1="53" y1="54" x2="61" y2="54" stroke="#888" stroke-width="0.8"/>
    <line x1="53" y1="56" x2="59" y2="56" stroke="#888" stroke-width="0.8"/>
    <!-- Expression neutre absorbée -->
    <line x1="32" y1="52" x2="48" y2="52" stroke="#b09070" stroke-width="1.5" stroke-linecap="round"/>
  </svg>`,

  GHOST: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#000a00"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#e8d0b0"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#e8d0b0"/>
    <!-- Cheveux noirs nets -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#0d0d0d"/>
    <rect x="22" y="24" width="36" height="8" rx="4" fill="#0d0d0d"/>
    <!-- Lunettes rondes fines -->
    <circle cx="31" cy="40" r="7" fill="none" stroke="#444" stroke-width="1.5"/>
    <circle cx="49" cy="40" r="7" fill="none" stroke="#444" stroke-width="1.5"/>
    <line x1="38" y1="40" x2="42" y2="40" stroke="#444" stroke-width="1.5"/>
    <!-- Yeux sombres observateurs -->
    <ellipse cx="31" cy="40" rx="4" ry="3.5" fill="#00FF41" opacity="0.8"/>
    <ellipse cx="49" cy="40" rx="4" ry="3.5" fill="#00FF41" opacity="0.8"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils fins calmes -->
    <path d="M25 33 Q31 31 37 33" stroke="#0d0d0d" stroke-width="2" fill="none"/>
    <path d="M43 33 Q49 31 55 33" stroke="#0d0d0d" stroke-width="2" fill="none"/>
    <!-- Expression neutre/invisible -->
    <line x1="33" y1="52" x2="47" y2="52" stroke="#c0a880" stroke-width="1.5" stroke-linecap="round"/>
    <!-- Hoodie col haut discret -->
    <path d="M22 62 Q30 56 40 55 Q50 56 58 62" fill="#111" opacity="0.6"/>
  </svg>`,

  CYPHER: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#00101a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#e0c090"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#e0c090"/>
    <!-- Cheveux noirs coupé côté net -->
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#0d0500"/>
    <rect x="22" y="24" width="36" height="9" rx="3" fill="#0d0500"/>
    <path d="M22 28 Q22 34 26 36" fill="#0d0500"/>
    <!-- Lunettes fines titane -->
    <rect x="23" y="36" width="12" height="8" rx="2" fill="none" stroke="#aaa" stroke-width="1.5"/>
    <rect x="45" y="36" width="12" height="8" rx="2" fill="none" stroke="#aaa" stroke-width="1.5"/>
    <line x1="35" y1="40" x2="45" y2="40" stroke="#aaa" stroke-width="1.5"/>
    <!-- Yeux cyan vifs -->
    <ellipse cx="29" cy="40" rx="4" ry="3.5" fill="#00E5FF"/>
    <ellipse cx="51" cy="40" rx="4" ry="3.5" fill="#00E5FF"/>
    <circle cx="30" cy="39" r="1.2" fill="white"/>
    <circle cx="52" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils nets -->
    <rect x="24" y="32" width="11" height="3" rx="1.5" fill="#0d0500"/>
    <rect x="45" y="32" width="11" height="3" rx="1.5" fill="#0d0500"/>
    <!-- Sourire efficace -->
    <path d="M33 52 Q40 56 47 52" stroke="#b09060" stroke-width="2" fill="none" stroke-linecap="round"/>
    <!-- Montre sport au poignet (symbolisée) -->
    <rect x="12" y="50" width="8" height="5" rx="2" fill="#00E5FF" opacity="0.5"/>
  </svg>`,

  FORGE: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0800"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c07840"/>
    <ellipse cx="40" cy="42" rx="19" ry="20" fill="#c07840"/>
    <!-- Cheveux brun-gris courts -->
    <ellipse cx="40" cy="26" rx="19" ry="10" fill="#5a4030"/>
    <rect x="21" y="24" width="38" height="9" rx="3" fill="#5a4030"/>
    <!-- Mâchoire large d'artisan -->
    <path d="M21 50 Q21 62 40 65 Q59 62 59 50" fill="#c07840"/>
    <!-- Barbe mi-longue poivre-sel -->
    <ellipse cx="40" cy="58" rx="16" ry="7" fill="#6a5040" opacity="0.8"/>
    <ellipse cx="40" cy="56" rx="14" ry="5" fill="#8a6050" opacity="0.6"/>
    <!-- Petite cicatrice pouce gauche (symbolisée sur joue) -->
    <line x1="24" y1="48" x2="27" y2="51" stroke="#a05030" stroke-width="1.5"/>
    <!-- Yeux calmes marron -->
    <ellipse cx="31" cy="40" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3.5" fill="#FF6600"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3.5" fill="#FF6600"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils épais naturels -->
    <rect x="25" y="32" width="12" height="4" rx="2" fill="#3a2010"/>
    <rect x="43" y="32" width="12" height="4" rx="2" fill="#3a2010"/>
    <!-- Expression calme et posée -->
    <path d="M33 52 Q40 55 47 52" stroke="#8a5020" stroke-width="2" fill="none" stroke-linecap="round"/>
  </svg>`,

  ZEN: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a1a0a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4c0a0"/>
    <ellipse cx="40" cy="42" rx="17" ry="19" fill="#d4c0a0"/>
    <!-- Cheveux noirs lissés -->
    <ellipse cx="40" cy="27" rx="17" ry="9" fill="#0d0d0d"/>
    <rect x="23" y="25" width="34" height="8" rx="4" fill="#0d0d0d"/>
    <!-- Visage fin serein -->
    <!-- Yeux mi-clos zen -->
    <path d="M25 40 Q31 36 37 40" stroke="none" fill="white"/>
    <ellipse cx="31" cy="40" rx="5.5" ry="3" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="3" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="2" fill="#5D7B5D"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="2" fill="#5D7B5D"/>
    <!-- Paupières mi-closes -->
    <path d="M25 38 Q31 37 37 39" stroke="#0d0d0d" stroke-width="2" fill="none"/>
    <path d="M43 38 Q49 37 55 39" stroke="#0d0d0d" stroke-width="2" fill="none"/>
    <!-- Sourcils fins reposés -->
    <path d="M26 34 Q31 32 36 34" stroke="#0d0d0d" stroke-width="1.5" fill="none"/>
    <path d="M44 34 Q49 32 54 34" stroke="#0d0d0d" stroke-width="1.5" fill="none"/>
    <!-- Sourire subtil intérieur -->
    <path d="M35 52 Q40 54 45 52" stroke="#9a8060" stroke-width="1.5" fill="none" stroke-linecap="round"/>
    <!-- Nez fin -->
    <ellipse cx="40" cy="46" rx="2" ry="1.5" fill="#c0a880"/>
  </svg>`,

  ALADIN: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a001a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4a870"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#d4a870"/>
    <!-- Cheveux noirs avec pointes violettes dégradé -->
    <ellipse cx="40" cy="25" rx="19" ry="11" fill="#0d0d0d"/>
    <rect x="21" y="23" width="38" height="9" rx="4" fill="#0d0d0d"/>
    <!-- Pointes violettes -->
    <path d="M24 24 Q26 16 30 18" stroke="#7B2FBE" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M34 22 Q35 13 38 15" stroke="#7B2FBE" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M44 22 Q46 13 49 16" stroke="#7B2FBE" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M52 24 Q55 17 58 20" stroke="#7B2FBE" stroke-width="4" fill="none" stroke-linecap="round"/>
    <!-- AirPod oreille droite -->
    <circle cx="58" cy="42" r="4" fill="white"/>
    <circle cx="58" cy="42" r="2" fill="#ddd"/>
    <!-- iPad dans la main symbolisé -->
    <!-- Yeux vifs bridés légèrement -->
    <ellipse cx="31" cy="40" rx="5.5" ry="4" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="4" fill="white"/>
    <ellipse cx="31" cy="40" rx="3.5" ry="3" fill="#7B2FBE"/>
    <ellipse cx="49" cy="40" rx="3.5" ry="3" fill="#7B2FBE"/>
    <circle cx="32" cy="39" r="1.2" fill="white"/>
    <circle cx="50" cy="39" r="1.2" fill="white"/>
    <!-- Sourcils expressifs -->
    <path d="M26 34 Q31 31 36 34" stroke="#0d0d0d" stroke-width="2.5" fill="none"/>
    <path d="M44 34 Q49 31 54 34" stroke="#0d0d0d" stroke-width="2.5" fill="none"/>
    <!-- Grand sourire organisateur -->
    <path d="M31 52 Q40 59 49 52" stroke="#a07030" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M33 53 Q40 58 47 53 L47 55 Q40 60 33 55Z" fill="white" opacity="0.7"/>
  </svg>`,

  SLY: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a0a0a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4a870"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#d4a870"/>
    <!-- Cheveux brun-châtain mi-longs derrière oreilles -->
    <ellipse cx="40" cy="25" rx="19" ry="11" fill="#5a3010"/>
    <rect x="21" y="23" width="38" height="9" rx="4" fill="#5a3010"/>
    <rect x="21" y="28" width="6" height="18" rx="3" fill="#5a3010"/>
    <rect x="53" y="28" width="6" height="18" rx="3" fill="#5a3010"/>
    <!-- Chapeau fedora gris (signature) -->
    <ellipse cx="40" cy="22" rx="22" ry="5" fill="#888"/>
    <rect x="26" y="10" width="28" height="14" rx="4" fill="#999"/>
    <path d="M26 17 Q40 14 54 17" stroke="#777" stroke-width="1" fill="none"/>
    <!-- Yeux verts-noisette malins -->
    <ellipse cx="31" cy="41" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="49" cy="41" rx="5.5" ry="4.5" fill="white"/>
    <ellipse cx="32" cy="41" rx="3.5" ry="3.5" fill="#CC2200"/>
    <ellipse cx="50" cy="41" rx="3.5" ry="3.5" fill="#CC2200"/>
    <circle cx="33" cy="40" r="1.2" fill="white"/>
    <circle cx="51" cy="40" r="1.2" fill="white"/>
    <!-- Sourcils bien formés -->
    <path d="M26 35 Q31 32 36 35" stroke="#3a1a00" stroke-width="2.5" fill="none"/>
    <path d="M44 35 Q49 32 54 35" stroke="#3a1a00" stroke-width="2.5" fill="none"/>
    <!-- Sourire en coin — malicieux -->
    <path d="M33 52 Q40 55 48 51" stroke="#a07030" stroke-width="2" fill="none" stroke-linecap="round"/>
  </svg>`,

  BENTLEY: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#000a00"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#f0d0a8"/>
    <ellipse cx="40" cy="42" rx="19" ry="20" fill="#f0d0a8"/>
    <!-- Silhouette légèrement corpulente (joues rondes) -->
    <ellipse cx="40" cy="48" rx="22" ry="16" fill="#f0d0a8"/>
    <!-- Cheveux châtain-roux ondulés jamais coiffés -->
    <ellipse cx="40" cy="24" rx="20" ry="12" fill="#9B4D0F"/>
    <path d="M22 28 Q20 22 24 18 Q32 13 40 12 Q48 13 56 18 Q60 22 58 28" fill="#9B4D0F"/>
    <!-- Mèche rebelle front -->
    <path d="M34 20 Q37 28 38 25" stroke="#7a3a08" stroke-width="3" fill="none" stroke-linecap="round"/>
    <!-- Lunettes épaisses bleues -->
    <rect x="22" y="36" width="14" height="11" rx="4" fill="none" stroke="#1a6abf" stroke-width="3"/>
    <rect x="44" y="36" width="14" height="11" rx="4" fill="none" stroke="#1a6abf" stroke-width="3"/>
    <line x1="36" y1="41" x2="44" y2="41" stroke="#1a6abf" stroke-width="2.5"/>
    <!-- Yeux derrière lunettes -->
    <ellipse cx="29" cy="41" rx="4" ry="3.5" fill="#00FF41"/>
    <ellipse cx="51" cy="41" rx="4" ry="3.5" fill="#00FF41"/>
    <circle cx="30" cy="40" r="1.2" fill="white"/>
    <circle cx="52" cy="40" r="1.2" fill="white"/>
    <!-- Joues rondes qui rougissent facilement -->
    <circle cx="25" cy="48" r="5" fill="#ffb0a0" opacity="0.4"/>
    <circle cx="55" cy="48" r="5" fill="#ffb0a0" opacity="0.4"/>
    <!-- Sourire enthousiaste -->
    <path d="M30 52 Q40 59 50 52" stroke="#c09060" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M32 53 Q40 58 48 53 L48 55 Q40 60 32 55Z" fill="white" opacity="0.7"/>
  </svg>`,

  MURRAY: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0000"/>
    <rect x="33" y="54" width="14" height="12" rx="4" fill="#3d1500"/>
    <ellipse cx="40" cy="42" rx="20" ry="21" fill="#3d1500"/>
    <!-- Crâne rasé imposant -->
    <ellipse cx="40" cy="27" rx="20" ry="11" fill="#2a0d00"/>
    <!-- Carrure des épaules larges -->
    <path d="M15 65 Q20 54 40 52 Q60 54 65 65" fill="#3d1500"/>
    <!-- Yeux expressifs chaleureux -->
    <ellipse cx="31" cy="41" rx="6" ry="5.5" fill="white"/>
    <ellipse cx="49" cy="41" rx="6" ry="5.5" fill="white"/>
    <ellipse cx="31" cy="41" rx="4" ry="4" fill="#FF0000"/>
    <ellipse cx="49" cy="41" rx="4" ry="4" fill="#FF0000"/>
    <circle cx="32" cy="40" r="1.5" fill="white"/>
    <circle cx="50" cy="40" r="1.5" fill="white"/>
    <!-- Sourcils épais expressifs -->
    <rect x="24" y="32" width="14" height="5" rx="2.5" fill="#1a0500"/>
    <rect x="42" y="32" width="14" height="5" rx="2.5" fill="#1a0500"/>
    <!-- Grand sourire immense communicatif -->
    <path d="M27 52 Q40 62 53 52" stroke="#2a0d00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M29 53 Q40 61 51 53 L51 57 Q40 64 29 57Z" fill="white" opacity="0.85"/>
    <!-- Dent en or visible -->
    <rect x="38" y="55" width="4" height="4" rx="1" fill="#d4af37"/>
    <!-- Apple Watch symbolisée -->
    <rect x="11" y="50" width="9" height="7" rx="2" fill="#FF0000" opacity="0.7"/>
    <rect x="12" y="51" width="7" height="5" rx="1" fill="#111"/>
  </svg>`,

  BAGHEERA: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a1400"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8955a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8955a"/>
    <!-- Cheveux noirs légèrement frisés élégants -->
    <ellipse cx="40" cy="25" rx="19" ry="11" fill="#0d0500"/>
    <path d="M22 28 Q21 20 30 16 Q40 13 50 16 Q59 20 58 28" fill="#0d0500"/>
    <!-- Deux stylos dans poche (rouge et noir) -->
    <line x1="54" y1="50" x2="54" y2="64" stroke="#e00" stroke-width="2" stroke-linecap="round"/>
    <line x1="57" y1="50" x2="57" y2="64" stroke="#111" stroke-width="2" stroke-linecap="round"/>
    <!-- Yeux ambre vivaces -->
    <ellipse cx="31" cy="40" rx="5.5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5.5" ry="5" fill="white"/>
    <ellipse cx="31" cy="40" rx="4" ry="4" fill="#FFBF00"/>
    <ellipse cx="49" cy="40" rx="4" ry="4" fill="#FFBF00"/>
    <circle cx="32" cy="39" r="1.5" fill="white"/>
    <circle cx="50" cy="39" r="1.5" fill="white"/>
    <!-- Sourcils expressifs mobiles -->
    <path d="M26 33 Q31 30 36 33" stroke="#0d0500" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M44 33 Q49 30 54 33" stroke="#0d0500" stroke-width="3" fill="none" stroke-linecap="round"/>
    <!-- Mains expressives symbolisées -->
    <!-- Sourire orchestrateur -->
    <path d="M31 52 Q40 58 49 52" stroke="#9a6020" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M33 53 Q40 57 47 53 L47 55 Q40 59 33 55Z" fill="white" opacity="0.7"/>
  </svg>`,

  BALOO: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a001a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8905a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8905a"/>
    <!-- Dreadlocks mi-longs retenus vaguement -->
    <line x1="32" y1="25" x2="28" y2="8" stroke="#3d1a00" stroke-width="4.5" stroke-linecap="round"/>
    <line x1="36" y1="23" x2="33" y2="5" stroke="#3d1a00" stroke-width="4.5" stroke-linecap="round"/>
    <line x1="40" y1="22" x2="40" y2="5" stroke="#3d1a00" stroke-width="4" stroke-linecap="round"/>
    <line x1="44" y1="23" x2="47" y2="6" stroke="#3d1a00" stroke-width="4.5" stroke-linecap="round"/>
    <line x1="48" y1="25" x2="52" y2="9" stroke="#3d1a00" stroke-width="4" stroke-linecap="round"/>
    <ellipse cx="40" cy="27" rx="17" ry="9" fill="#3d1a00"/>
    <!-- Élastique ou crayon dans les dreads -->
    <circle cx="44" cy="23" r="3" fill="#6B21A8" opacity="0.8"/>
    <!-- Yeux dans un autre fuseau — dorés reflets -->
    <ellipse cx="31" cy="41" rx="6" ry="5" fill="white"/>
    <ellipse cx="49" cy="41" rx="6" ry="5" fill="white"/>
    <ellipse cx="31" cy="41" rx="4" ry="4" fill="#6B21A8"/>
    <ellipse cx="49" cy="41" rx="4" ry="4" fill="#6B21A8"/>
    <!-- Reflet doré dans les yeux -->
    <circle cx="32" cy="40" r="1.5" fill="#d4af37" opacity="0.8"/>
    <circle cx="50" cy="40" r="1.5" fill="#d4af37" opacity="0.8"/>
    <!-- Sourcils détendus naturels -->
    <path d="M25 34 Q31 32 37 34" stroke="#3d1a00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M43 34 Q49 32 55 34" stroke="#3d1a00" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <!-- Sourire lent qui arrive comme le soleil -->
    <path d="M30 52 Q40 60 50 52" stroke="#7a4a10" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M32 53 Q40 59 48 53 L48 56 Q40 62 32 56Z" fill="white" opacity="0.75"/>
    <!-- Dent en or molaire gauche -->
    <circle cx="36" cy="57" r="2" fill="#d4af37" opacity="0.7"/>
    <!-- Bracelets de fils aux poignets -->
    <line x1="12" y1="55" x2="20" y2="55" stroke="#6B21A8" stroke-width="2.5" stroke-linecap="round"/>
    <line x1="12" y1="58" x2="20" y2="58" stroke="#d4af37" stroke-width="2" stroke-linecap="round"/>
  </svg>`,

  // === 10 NOUVEAUX AGENTS (30→40) ===

  OUTREACH: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a2540"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#8d5524"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#8d5524"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#1a0a00"/>
    <rect x="22" y="24" width="36" height="6" rx="3" fill="#1a0a00"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#1F6FFF"/>
    <circle cx="49" cy="40" r="2.5" fill="#1F6FFF"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#7a4a10"/>
    <path d="M32 52 Q40 58 48 52" stroke="#5a3510" stroke-width="2" fill="none" stroke-linecap="round"/>
    <rect x="52" y="28" width="8" height="12" rx="2" fill="#1F6FFF" opacity="0.8"/>
    <line x1="56" y1="24" x2="56" y2="28" stroke="#1F6FFF" stroke-width="1.5"/>
    <circle cx="56" cy="23" r="2" fill="#1F6FFF"/>
  </svg>`,

  ANALYTICS: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a1628"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#f0c8a0"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#f0c8a0"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#2d1810"/>
    <rect x="22" y="24" width="36" height="6" rx="3" fill="#2d1810"/>
    <rect x="25" y="36" width="12" height="8" rx="4" fill="none" stroke="#00E5FF" stroke-width="1.5"/>
    <rect x="43" y="36" width="12" height="8" rx="4" fill="none" stroke="#00E5FF" stroke-width="1.5"/>
    <line x1="37" y1="40" x2="43" y2="40" stroke="#00E5FF" stroke-width="1.5"/>
    <circle cx="31" cy="40" r="2.5" fill="#0B0F14"/>
    <circle cx="49" cy="40" r="2.5" fill="#0B0F14"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#c8a080"/>
    <path d="M34 53 Q40 56 46 53" stroke="#a08060" stroke-width="1.5" fill="none"/>
  </svg>`,

  PARAGON: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a2010"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c68642"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c68642"/>
    <ellipse cx="40" cy="26" rx="17" ry="9" fill="#3d2510"/>
    <rect x="23" y="24" width="34" height="7" rx="3" fill="#3d2510"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#1EFF8E"/>
    <circle cx="49" cy="40" r="2.5" fill="#1EFF8E"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#a06830"/>
    <path d="M33 52 Q40 57 47 52" stroke="#804820" stroke-width="2" fill="none"/>
    <path d="M36 21 L40 16 L44 21" stroke="#1EFF8E" stroke-width="2" fill="none" stroke-linecap="round"/>
  </svg>`,

  ARCHITECT: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a1020"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#e0b090"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#e0b090"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#404040"/>
    <rect x="22" y="24" width="36" height="7" rx="3" fill="#404040"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#7A3CFF"/>
    <circle cx="49" cy="40" r="2.5" fill="#7A3CFF"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#c09070"/>
    <path d="M34 53 Q40 56 46 53" stroke="#a07050" stroke-width="1.5" fill="none"/>
    <rect x="26" y="36" width="28" height="0.8" fill="#7A3CFF" opacity="0.5"/>
    <line x1="40" y1="28" x2="40" y2="36" stroke="#7A3CFF" stroke-width="0.8" opacity="0.5"/>
  </svg>`,

  PROXY: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a1a2e"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#d4a574"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#d4a574"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#0d0700"/>
    <rect x="22" y="24" width="36" height="7" rx="3" fill="#0d0700"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#3A8DFF"/>
    <circle cx="49" cy="40" r="2.5" fill="#3A8DFF"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#b48554"/>
    <path d="M32 52 Q40 58 48 52" stroke="#946534" stroke-width="2" fill="none"/>
    <path d="M32 53 Q40 57 48 53" fill="white" opacity="0.8"/>
    <rect x="35" y="59" width="10" height="3" rx="1" fill="#3A8DFF"/>
  </svg>`,

  VECTOR: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a1828"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#f5d0a0"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#f5d0a0"/>
    <ellipse cx="40" cy="26" rx="17" ry="9" fill="#5a3520"/>
    <rect x="23" y="24" width="34" height="6" rx="3" fill="#5a3520"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#00B8CC"/>
    <circle cx="49" cy="40" r="2.5" fill="#00B8CC"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#d5b080"/>
    <path d="M34 53 Q40 56 46 53" stroke="#b59060" stroke-width="1.5" fill="none"/>
    <text x="40" y="20" text-anchor="middle" font-size="8" fill="#00E5FF" font-family="monospace">A文</text>
  </svg>`,

  CATALYST: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#1a0a10"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#b07040"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#b07040"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#c03020"/>
    <rect x="22" y="24" width="36" height="7" rx="3" fill="#c03020"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#FF6B35"/>
    <circle cx="49" cy="40" r="2.5" fill="#FF6B35"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#905020"/>
    <path d="M30 52 Q40 60 50 52" stroke="#704010" stroke-width="2.5" fill="none" stroke-linecap="round"/>
    <path d="M32 53 Q40 59 48 53" fill="white" opacity="0.7"/>
    <circle cx="56" cy="30" r="4" fill="#FF6B35" opacity="0.6"/>
    <circle cx="58" cy="28" r="2" fill="#FF9A3C" opacity="0.8"/>
  </svg>`,

  MIMIC: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0d0d1a"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#e8c8a0"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#e8c8a0"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#202030"/>
    <rect x="22" y="24" width="36" height="7" rx="3" fill="#202030"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#B18CFF"/>
    <circle cx="49" cy="40" r="2.5" fill="#B18CFF"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#c8a880"/>
    <path d="M34 52 Q40 55 46 52" stroke="#a88860" stroke-width="1.5" fill="none"/>
    <rect x="24" y="36" width="8" height="8" rx="4" fill="none" stroke="#B18CFF" stroke-width="1" stroke-dasharray="2 2"/>
    <rect x="48" y="36" width="8" height="8" rx="4" fill="none" stroke="#B18CFF" stroke-width="1" stroke-dasharray="2 2"/>
  </svg>`,

  KEEPER: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a1a20"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#a0704a"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#a0704a"/>
    <ellipse cx="40" cy="26" rx="17" ry="9" fill="#1a0800"/>
    <rect x="23" y="24" width="34" height="7" rx="3" fill="#1a0800"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#3A8DFF"/>
    <circle cx="49" cy="40" r="2.5" fill="#3A8DFF"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#80502a"/>
    <path d="M33 52 Q40 57 47 52" stroke="#60400a" stroke-width="2" fill="none"/>
    <path d="M30 20 L40 14 L50 20 L50 26 L30 26Z" fill="none" stroke="#3A8DFF" stroke-width="1.5"/>
    <circle cx="40" cy="22" r="2" fill="#3A8DFF"/>
  </svg>`,

  NEXUS: `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <circle cx="40" cy="40" r="38" fill="#0a0a1e"/>
    <rect x="33" y="54" width="14" height="10" rx="4" fill="#c8a070"/>
    <ellipse cx="40" cy="42" rx="18" ry="20" fill="#c8a070"/>
    <ellipse cx="40" cy="26" rx="18" ry="10" fill="#0a0020"/>
    <rect x="22" y="24" width="36" height="7" rx="3" fill="#0a0020"/>
    <ellipse cx="31" cy="40" rx="5" ry="5" fill="white"/>
    <ellipse cx="49" cy="40" rx="5" ry="5" fill="white"/>
    <circle cx="31" cy="40" r="2.5" fill="#7A3CFF"/>
    <circle cx="49" cy="40" r="2.5" fill="#7A3CFF"/>
    <ellipse cx="40" cy="48" rx="3" ry="2" fill="#a88050"/>
    <path d="M33 52 Q40 57 47 52" stroke="#886030" stroke-width="2" fill="none"/>
    <line x1="25" y1="20" x2="40" y2="15" stroke="#7A3CFF" stroke-width="1" opacity="0.6"/>
    <line x1="55" y1="20" x2="40" y2="15" stroke="#1F6FFF" stroke-width="1" opacity="0.6"/>
    <line x1="25" y1="20" x2="55" y2="20" stroke="#00E5FF" stroke-width="1" opacity="0.4"/>
    <circle cx="25" cy="20" r="2.5" fill="#7A3CFF"/>
    <circle cx="55" cy="20" r="2.5" fill="#1F6FFF"/>
    <circle cx="40" cy="15" r="2.5" fill="#00E5FF"/>
  </svg>`

};
