import asyncio
import genanki
from googletrans import Translator
import nltk
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import word_tokenize

# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')

def main(text_file_path):
    # Initialize the French stemmer
    stemmer = FrenchStemmer()

    # Read the content of the file
    with open(text_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Tokenize the text into words
    words = [word for word in word_tokenize(text, language='french') if any(char.isalpha() for char in word)]

    # Stem each word
    stemmed_words = [stemmer.stem(word) for word in words]

    # Create a sorted set of the words by first occurrence
    sorted_unique_words = sorted(set(stemmed_words), key=stemmed_words.index)

    asyncio.run(dump_to_flashcards(text_file_path, sorted_unique_words))


async def dump_to_flashcards(deck_filepath, words):
    # Initialize the Google Translate API
    translator = Translator()

    # Create a new Anki deck
    deck = genanki.Deck(
        name='French Flashcards',
        deck_id=717171711
    )

    # Create a model for the cards
    model = genanki.Model(
        717171713,
        name='Simple Model',
        fields=[
            {'name': 'French'},
            {'name': 'English'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{French}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{English}}'
            }
        ]
    )
    for word in words:
        translation = (await translator.translate(word, src='fr', dest='en')).text
        note = genanki.Note(
            model=model,
            fields=[word, translation]
        )
        deck.add_note(note)

    # Save the deck to a file
    genanki.Package(deck).write_to_file(f'out/{deck_filepath}.apkg')

if __name__ == '__main__':
    import sys
    main(sys.argv[1])