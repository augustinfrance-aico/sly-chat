const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const TYPES = {html:'text/html',js:'application/javascript',css:'text/css',webp:'image/webp',avif:'image/avif',png:'image/png',jpg:'image/jpeg',json:'application/json',glb:'model/gltf-binary',mp3:'audio/mpeg'};

// ── Clés API — JAMAIS dans le frontend
const GROQ_KEY  = process.env.GROQ_KEY  || '';
const FISH_KEY  = process.env.FISH_KEY  || '';
const GEMINI_KEY = process.env.GEMINI_KEY || '';

function readBody(req) {
    return new Promise((resolve, reject) => {
        let body = '';
        req.on('data', d => { body += d; if (body.length > 512000) req.destroy(); });
        req.on('end', () => resolve(body));
        req.on('error', reject);
    });
}

function corsHeaders() {
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    };
}

http.createServer(async (req, res) => {

    // CORS preflight
    if (req.method === 'OPTIONS') {
        res.writeHead(204, corsHeaders());
        res.end();
        return;
    }

    // ── PROXY GROQ (/proxy/chat) ─────────────────────────────────────
    if (req.url === '/proxy/chat' && req.method === 'POST') {
        if (!GROQ_KEY) { res.writeHead(503, corsHeaders()); res.end(JSON.stringify({error:'GROQ_KEY not configured on server'})); return; }
        const body = await readBody(req);
        const proxyReq = https.request({
            hostname: 'api.groq.com',
            path: '/openai/v1/chat/completions',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + GROQ_KEY,
                'Content-Length': Buffer.byteLength(body)
            }
        }, proxyRes => {
            res.writeHead(proxyRes.statusCode, { ...corsHeaders(), 'Content-Type': proxyRes.headers['content-type'] || 'application/json' });
            proxyRes.pipe(res);
        });
        proxyReq.on('error', e => { res.writeHead(502, corsHeaders()); res.end(JSON.stringify({error: e.message})); });
        proxyReq.write(body);
        proxyReq.end();
        return;
    }

    // ── PROXY GROQ MODELS (/proxy/models) ────────────────────────────
    if (req.url === '/proxy/models' && req.method === 'GET') {
        if (!GROQ_KEY) { res.writeHead(503, corsHeaders()); res.end(JSON.stringify({error:'GROQ_KEY not configured'})); return; }
        const proxyReq = https.request({
            hostname: 'api.groq.com',
            path: '/openai/v1/models',
            method: 'GET',
            headers: { 'Authorization': 'Bearer ' + GROQ_KEY }
        }, proxyRes => {
            res.writeHead(proxyRes.statusCode, { ...corsHeaders(), 'Content-Type': 'application/json' });
            proxyRes.pipe(res);
        });
        proxyReq.on('error', e => { res.writeHead(502, corsHeaders()); res.end(JSON.stringify({error: e.message})); });
        proxyReq.end();
        return;
    }

    // ── PROXY GEMINI (/proxy/gemini) ─────────────────────────────────
    if (req.url.startsWith('/proxy/gemini') && req.method === 'POST') {
        if (!GEMINI_KEY) { res.writeHead(503, corsHeaders()); res.end(JSON.stringify({error:'GEMINI_KEY not configured on server'})); return; }
        const body = await readBody(req);
        // Extraire le modèle depuis ?model=gemini-2.0-flash
        const urlObj = new URL(req.url, 'http://localhost');
        const model = urlObj.searchParams.get('model') || 'gemini-2.0-flash';
        const geminiPath = `/v1beta/models/${model}:generateContent?key=${GEMINI_KEY}`;
        const proxyReq = https.request({
            hostname: 'generativelanguage.googleapis.com',
            path: geminiPath,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body)
            }
        }, proxyRes => {
            res.writeHead(proxyRes.statusCode, { ...corsHeaders(), 'Content-Type': proxyRes.headers['content-type'] || 'application/json' });
            proxyRes.pipe(res);
        });
        proxyReq.on('error', e => { res.writeHead(502, corsHeaders()); res.end(JSON.stringify({error: e.message})); });
        proxyReq.write(body);
        proxyReq.end();
        return;
    }

    // ── PROXY TTS FishAudio (/proxy/tts) ─────────────────────────────
    if (req.url === '/proxy/tts' && req.method === 'POST') {
        if (!FISH_KEY) { res.writeHead(503, corsHeaders()); res.end(JSON.stringify({error:'FISH_KEY not configured on server'})); return; }
        const body = await readBody(req);
        const proxyReq = https.request({
            hostname: 'api.fish.audio',
            path: '/v1/tts',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + FISH_KEY,
                'Content-Length': Buffer.byteLength(body)
            }
        }, proxyRes => {
            res.writeHead(proxyRes.statusCode, { ...corsHeaders(), 'Content-Type': proxyRes.headers['content-type'] || 'audio/mpeg' });
            proxyRes.pipe(res);
        });
        proxyReq.on('error', e => { res.writeHead(502, corsHeaders()); res.end(JSON.stringify({error: e.message})); });
        proxyReq.write(body);
        proxyReq.end();
        return;
    }

    // ── Fichiers statiques ────────────────────────────────────────────
    const url = decodeURIComponent(req.url === '/' ? '/index.html' : req.url);
    const f = path.join(__dirname, url.split('?')[0]);
    if (!fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); res.end('Not found'); return; }
    const ext = path.extname(f).slice(1);
    res.writeHead(200, {'Content-Type': TYPES[ext] || 'application/octet-stream'});
    fs.createReadStream(f).pipe(res);

}).listen(process.env.PORT || 3000, () => console.log(`SLY-CHAT running at http://localhost:${process.env.PORT || 3000}`));
