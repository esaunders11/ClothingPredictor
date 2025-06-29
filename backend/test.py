from TitleExtractor import TitleExtractor

title_extractor = TitleExtractor()

title = "Ancient Greek Sandals Half off sale"
brand = title_extractor.extract_brand(title)
size = title_extractor.extract_size("Size: L")
print(brand, size)