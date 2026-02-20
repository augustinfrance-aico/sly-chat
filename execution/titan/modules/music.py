"""
TITAN Music Module v2
Discover music you'll love based on your tastes. AI-powered recommendations.
Spotify/YouTube links, artist discovery, genre exploration.
"""

import random
import requests

from ..ai_client import chat as ai_chat


class TitanMusic:
    """Ton DJ personnel qui te connaît par coeur."""

    PLAYLISTS = {
        "focus": {
            "genres": ["Lo-fi Hip Hop", "Ambient", "Classical Piano", "Post-Rock", "Chillhop"],
            "artists": ["Nujabes", "Bonobo", "Tycho", "Boards of Canada", "Emancipator"],
            "spotify": "https://open.spotify.com/search/focus%20music",
        },
        "workout": {
            "genres": ["EDM", "Hip-Hop", "Drum & Bass", "Rock", "Trap"],
            "artists": ["Eminem", "Run The Jewels", "Pendulum", "Rage Against The Machine"],
            "spotify": "https://open.spotify.com/search/workout%20playlist",
        },
        "chill": {
            "genres": ["Jazz", "Bossa Nova", "Soul", "R&B", "Indie Folk"],
            "artists": ["Norah Jones", "Jack Johnson", "Bon Iver", "Khruangbin", "Tom Misch"],
            "spotify": "https://open.spotify.com/search/chill%20vibes",
        },
        "coding": {
            "genres": ["Synthwave", "Cyberpunk", "Trance", "Minimal Techno", "Lo-fi Beats"],
            "artists": ["Kavinsky", "Perturbator", "Carpenter Brut", "Deadmau5", "Aphex Twin"],
            "spotify": "https://open.spotify.com/search/coding%20music",
        },
        "party": {
            "genres": ["Pop", "Dance", "Reggaeton", "House", "Funk"],
            "artists": ["Dua Lipa", "Bad Bunny", "Disclosure", "Calvin Harris", "Daft Punk"],
            "spotify": "https://open.spotify.com/search/party%20hits",
        },
        "sleep": {
            "genres": ["Ambient Sleep", "Rain Sounds", "Piano Doux", "Nature Sounds"],
            "artists": ["Max Richter", "Ólafur Arnalds", "Nils Frahm", "Brian Eno"],
            "spotify": "https://open.spotify.com/search/sleep%20sounds",
        },
        "motivation": {
            "genres": ["Epic Orchestral", "Movie Soundtracks", "Power Metal", "Hip-Hop"],
            "artists": ["Hans Zimmer", "Two Steps from Hell", "Eminem", "Kendrick Lamar"],
            "spotify": "https://open.spotify.com/search/motivation%20epic",
        },
        "road_trip": {
            "genres": ["Classic Rock", "Indie", "Pop Rock", "Country Rock"],
            "artists": ["Fleetwood Mac", "Eagles", "Arctic Monkeys", "Tame Impala"],
            "spotify": "https://open.spotify.com/search/road%20trip",
        },
        "french": {
            "genres": ["French Rap", "French Pop", "Chanson", "French Touch"],
            "artists": ["PNL", "Stromae", "Daft Punk", "Angèle", "Orelsan", "Nekfeu", "SCH"],
            "spotify": "https://open.spotify.com/search/french%20music",
        },
        "romantic": {
            "genres": ["Neo-Soul", "R&B", "Jazz Vocals", "Soft Rock"],
            "artists": ["Frank Ocean", "Daniel Caesar", "Sade", "The Weeknd", "SZA"],
            "spotify": "https://open.spotify.com/search/romantic%20playlist",
        },
        "sport": {
            "genres": ["Trap", "EDM", "Dubstep", "Drum & Bass", "Grime"],
            "artists": ["Skrillex", "Travis Scott", "DMX", "Meek Mill", "Stormzy"],
            "spotify": "https://open.spotify.com/search/sport%20workout%20beast%20mode",
        },
    }

    ICONIC_ALBUMS = [
        ("Dark Side of the Moon", "Pink Floyd", "1973", "Progressive Rock"),
        ("Thriller", "Michael Jackson", "1982", "Pop"),
        ("OK Computer", "Radiohead", "1997", "Alt Rock"),
        ("To Pimp a Butterfly", "Kendrick Lamar", "2015", "Hip-Hop"),
        ("Random Access Memories", "Daft Punk", "2013", "Electronic"),
        ("Abbey Road", "The Beatles", "1969", "Rock"),
        ("Discovery", "Daft Punk", "2001", "French Touch"),
        ("Back to Black", "Amy Winehouse", "2006", "Soul"),
        ("Rumours", "Fleetwood Mac", "1977", "Rock"),
        ("Channel Orange", "Frank Ocean", "2012", "R&B"),
        ("DAMN.", "Kendrick Lamar", "2017", "Hip-Hop"),
        ("In Rainbows", "Radiohead", "2007", "Alt Rock"),
        ("Blonde", "Frank Ocean", "2016", "R&B"),
        ("Igor", "Tyler The Creator", "2019", "Neo-Soul"),
        ("After Hours", "The Weeknd", "2020", "Synth-Pop"),
        ("Les derniers salopards", "PNL", "2015", "French Rap"),
        ("Multitude", "Stromae", "2022", "French Pop"),
        ("Civilisation", "Orelsan", "2021", "French Rap"),
        ("JVLIVS", "SCH", "2019", "French Rap"),
        ("Kid A", "Radiohead", "2000", "Experimental"),
    ]

    # Taste profiles for AI matching
    TASTE_PROFILES = {
        "rap_fr": {"artists": ["PNL", "Nekfeu", "Orelsan", "SCH", "Damso", "Ninho", "PLK", "Gazo", "SDM"], "vibe": "rap français"},
        "rap_us": {"artists": ["Kendrick", "Drake", "Travis Scott", "J. Cole", "Tyler", "21 Savage"], "vibe": "rap US"},
        "rock": {"artists": ["Arctic Monkeys", "Radiohead", "Tame Impala", "The Strokes", "Muse"], "vibe": "rock/indie"},
        "electro": {"artists": ["Daft Punk", "Kavinsky", "Flume", "ODESZA", "Disclosure", "Fred Again"], "vibe": "electro"},
        "rnb": {"artists": ["Frank Ocean", "The Weeknd", "SZA", "Daniel Caesar", "Jorja Smith"], "vibe": "R&B/Soul"},
        "classique": {"artists": ["Chopin", "Debussy", "Beethoven", "Bach", "Ravel"], "vibe": "classique"},
    }

    def __init__(self):
        pass

    def playlist(self, mood: str = "focus") -> str:
        """Get a playlist recommendation with Spotify links."""
        mood_key = mood.lower().strip()
        if mood_key in self.PLAYLISTS:
            data = self.PLAYLISTS[mood_key]
        else:
            mood_key = random.choice(list(self.PLAYLISTS.keys()))
            data = self.PLAYLISTS[mood_key]

        lines = [f"🎵 PLAYLIST: {mood_key.upper()}\n"]
        lines.append("Genres:")
        for g in data["genres"]:
            lines.append(f"  🎶 {g}")
        lines.append("\nArtistes recommandés:")
        for a in data["artists"]:
            lines.append(f"  🎤 {a}")

        lines.append(f"\n🔗 Spotify: {data['spotify']}")
        lines.append(f"🔗 YouTube: https://www.youtube.com/results?search_query={mood_key.replace(' ', '+')}+playlist")

        lines.append(f"\nMoods dispo: {', '.join(self.PLAYLISTS.keys())}")
        return "\n".join(lines)

    def album_reco(self) -> str:
        """Recommend a classic album."""
        album, artist, year, genre = random.choice(self.ICONIC_ALBUMS)
        spotify_link = f"https://open.spotify.com/search/{(album + ' ' + artist).replace(' ', '%20')}"
        return (
            f"💿 ALBUM À ÉCOUTER\n\n"
            f"🎵 {album}\n"
            f"🎤 {artist} ({year})\n"
            f"🎶 Genre: {genre}\n\n"
            f"🔗 Spotify: {spotify_link}"
        )

    def artist_search(self, name: str) -> str:
        """Search for an artist on MusicBrainz."""
        try:
            resp = requests.get(
                f"https://musicbrainz.org/ws/2/artist/?query={name}&fmt=json&limit=3",
                headers={"User-Agent": "TitanBot/1.0"},
                timeout=10,
            )
            data = resp.json()
            artists = data.get("artists", [])

            if not artists:
                return f"Artiste '{name}' non trouvé."

            lines = [f"🎤 ARTISTE: {name}\n"]
            for a in artists[:3]:
                aname = a.get("name", "?")
                country = a.get("country", "?")
                genre = a.get("disambiguation", "")
                score = a.get("score", 0)
                spotify = f"https://open.spotify.com/search/{aname.replace(' ', '%20')}"
                lines.append(f"  🎵 {aname} ({country}) — {genre}")
                lines.append(f"     🔗 {spotify}")

            return "\n".join(lines)
        except Exception as e:
            return f"Erreur: {e}"

    def song_of_day(self) -> str:
        """Random song recommendation with links."""
        songs = [
            ("Bohemian Rhapsody", "Queen", "Rock"),
            ("Billie Jean", "Michael Jackson", "Pop"),
            ("Smells Like Teen Spirit", "Nirvana", "Grunge"),
            ("Get Lucky", "Daft Punk", "French Touch"),
            ("Lose Yourself", "Eminem", "Hip-Hop"),
            ("Blinding Lights", "The Weeknd", "Synth-Pop"),
            ("Nikes", "Frank Ocean", "R&B"),
            ("Pyramids", "Frank Ocean", "R&B"),
            ("Runaway", "Kanye West", "Hip-Hop"),
            ("Le monde ou rien", "PNL", "Rap FR"),
            ("Papaoutai", "Stromae", "French Pop"),
            ("La Pluie", "Orelsan ft. Stromae", "Rap FR"),
            ("Formidable", "Stromae", "French Pop"),
            ("A.U.D.D.", "SCH", "Rap FR"),
            ("Money Trees", "Kendrick Lamar", "Hip-Hop"),
        ]
        song, artist, genre = random.choice(songs)
        spotify = f"https://open.spotify.com/search/{(song + ' ' + artist).replace(' ', '%20')}"
        yt = f"https://www.youtube.com/results?search_query={(song + ' ' + artist).replace(' ', '+')}"
        return (
            f"🎵 CHANSON DU JOUR\n\n"
            f"🎶 {song}\n🎤 {artist}\n🏷️ {genre}\n\n"
            f"🔗 Spotify: {spotify}\n"
            f"🔗 YouTube: {yt}"
        )

    def genres(self) -> str:
        """List available mood playlists."""
        lines = ["🎵 MOODS DISPONIBLES\n"]
        for mood, data in self.PLAYLISTS.items():
            artists_str = ", ".join(data["artists"][:3])
            lines.append(f"  🎶 {mood}: {artists_str}...")
        lines.append(f"\n/playlist <mood> pour écouter")
        return "\n".join(lines)

    async def discover(self, tastes: str) -> str:
        """AI-powered music discovery based on user tastes."""
        return ai_chat("Expert assistant.", f"""En tant qu'expert musical avec une connaissance encyclopédique de TOUS les genres, recommande de la musique basée sur ces goûts: "{tastes}" """, 1500)

    async def similar_to(self, artist: str) -> str:
        """Find artists similar to a given one."""
        return ai_chat("Expert assistant.", f"""Quels artistes sont similaires à "{artist}" ?""", 1000)

    def top_albums(self, genre: str = "all") -> str:
        """Top albums by genre."""
        genre_key = genre.lower().strip()

        # Filter albums by genre if specified
        if genre_key == "all":
            albums = self.ICONIC_ALBUMS
            title = "TOP ALBUMS TOUS GENRES"
        else:
            albums = [a for a in self.ICONIC_ALBUMS if genre_key in a[3].lower()]
            if not albums:
                albums = self.ICONIC_ALBUMS
            title = f"TOP ALBUMS {genre_key.upper()}"

        lines = [f"💿 {title}\n"]
        for i, (album, artist, year, genre_name) in enumerate(albums[:10], 1):
            spotify = f"https://open.spotify.com/search/{(album + ' ' + artist).replace(' ', '%20')}"
            lines.append(f"  {i}. {album} — {artist} ({year})")
            lines.append(f"     🎶 {genre_name} | 🔗 {spotify}")

        return "\n".join(lines)

    def new_releases_links(self) -> str:
        """Links to find new music releases."""
        lines = ["🆕 NOUVELLES SORTIES\n"]
        lines.append("Où trouver de la nouvelle musique:\n")

        sources = [
            ("Spotify New Releases", "https://open.spotify.com/search/new%20releases"),
            ("Pitchfork Reviews", "https://pitchfork.com/reviews/albums/"),
            ("Album of the Year", "https://www.albumoftheyear.org/"),
            ("Rate Your Music", "https://rateyourmusic.com/charts/top/album/2025/"),
            ("Stereogum", "https://www.stereogum.com/"),
            ("HypeMachine", "https://hypem.com/popular"),
        ]

        for name, url in sources:
            lines.append(f"  🔗 {name}: {url}")

        return "\n".join(lines)
