import random
import requests

def get_random_quote():
    """Get a random quote from zenquotes.io"""
    quote = requests.get('https://zenquotes.io/api/random')
    return quote.json()[0]['q']

def generate_meme(top_text: str, bottom_text: str):
    """Generate a meme from apimeme.com"""
    memes = [
        "10-Guy",
        "Advice-Dog",
        "Actual-Advice-Mallard",
        "Ancient-Aliens",
        "Albert-Cagestein",
        "Bad-Joke-Eel",
        "1990s-First-World-Problems",
        "American-Chopper-Argument",
        "Back-In-My-Day",
        "Awkward-Moment-Sealion",
        "Castaway-Fire"
    ]

    random_meme = random.choice(memes)
    url = f"https://apimeme.com/meme?meme={random_meme}&top={top_text}&bottom={bottom_text}"
    meme = requests.get(url)
    return meme.content

def save_meme(meme: bytes):
    """Save the meme to a file"""
    with open('meme.jpg', 'wb') as f:
        f.write(meme)

def generate_meme_headings(quote: str) -> tuple[str, str]:
    """Generate the top and bottom text for the meme, splitting the quote in half word-wise"""
    words = quote.split()
    half = len(words) // 2
    top_text = ' '.join(words[:half])
    bottom_text = ' '.join(words[half:])

    return top_text, bottom_text

def create_meme():
    """Create a meme from a random quote"""
    quote = get_random_quote()
    top_text, bottom_text = generate_meme_headings(quote)
    meme = generate_meme(top_text, bottom_text)
    save_meme(meme)

if __name__ == "__main__":
    create_meme()