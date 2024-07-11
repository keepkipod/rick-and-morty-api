import requests
import csv

def get_characters(url):
    characters = []
    while url:
        response = requests.get(url)
        data = response.json()
        characters.extend(data['results'])
        url = data['info']['next']
    return characters

def filter_characters(characters):
    return [
        {
            'name': char['name'],
            'location': char['location']['name'],
            'image': char['image']
        }
        for char in characters
        if char['species'] == 'Human' and 
           char['status'] == 'Alive' and 
           char['origin']['name'].startswith('Earth')
    ]

def write_to_csv(characters, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Location', 'Image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for char in characters:
            writer.writerow({
                'Name': char['name'],
                'Location': char['location'],
                'Image': char['image']
            })

def main():
    base_url = 'https://rickandmortyapi.com/api/character'
    all_characters = get_characters(base_url)
    filtered_characters = filter_characters(all_characters)
    write_to_csv(filtered_characters, 'rick_and_morty_characters.csv')
    print(f"CSV file created with {len(filtered_characters)} characters.")

if __name__ == '__main__':
    main()