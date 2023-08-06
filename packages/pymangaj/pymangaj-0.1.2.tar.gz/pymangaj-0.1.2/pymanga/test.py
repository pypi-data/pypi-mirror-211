from pymanga import pymanga, Sources

# Test example
manga_name = "Naruto"
chapter = 699

# Search for the manga using both sources
if __name__ == '__main__':
    manga_pages = pymanga.search(manga_name, chapter, sources=[Sources.MANGA_LIVRE])
    # Print the result
    print(manga_pages)