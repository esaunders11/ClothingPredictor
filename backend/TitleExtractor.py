import re

class TitleExtractor:
    with open("backend/brands.txt", "r", encoding="utf-8") as file:
        brands = [line.strip() for line in file.readlines() if line.strip()]
    brand_lookup = {brand.lower(): brand for brand in brands}
    sorted_brand_keys = sorted(brand_lookup.keys(), key=lambda x: len(x.split()), reverse=True)

    category_keywords = {
        "Jacket": ["jacket", "parka", "anorak"],
        "Shirt": ["shirt", "button-up", "flannel", "tee"],
        "Pants": ["pants", "jeans", "trousers", "slacks"],
        "Hoodie": ["hoodie", "pullover", "sweatshirt"]
    }

    sub_category_keywords = {
        "Windbreaker": ["windbreaker"],
        "Denim": ["denim", "jean"],
        "Puffer": ["puffer", "down jacket"],
        "Band": ["band", "tour"],
        "Graphic": ["graphic", "print"]
    }

    def extract_fields(self, title):
        return {
            "brand": self.extract_brand(title),
            "category": self.match_keywords(title, self.category_keywords),
            "sub_category": self.match_keywords(title, self.sub_category_keywords),
            "size": self.extract_size(title)
        }

    def extract_brand(self, title):
        title_clean = re.sub(r"[^\w\s]", "", title).lower()
        title_words = title_clean.split()

        for n in range(4, 0, -1):
            for i in range(len(title_words) - n + 1):
                phrase = " ".join(title_words[i:i+n])
                if phrase in self.brand_lookup:
                    return self.brand_lookup[phrase]
        return "Unknown"
    
    def match_keywords(self, title, keyword_map):
        title = title.lower()
        for label, keywords in keyword_map.items():
            for word in keywords:
                if word in title:
                    return label
        return "Unknown"
    
    def extract_size(self, title):
        title = title.lower()

        full_words = {
            "extra small": "XS",
            "small": "S",
            "medium": "M",
            "large": "L",
            "extra large": "XL",
            "xxl": "XXL"
        }

        for word, code in full_words.items():
            if word in title:
                return code
        
        match = re.search(r"\b(XXL|XL|XS|S|M|L)\b", title.upper())
        if match:
            return match.group().upper()
        
        match = re.search(r"\b\d{1,2}x\d{1,2}\b|\b\d{1,2}\b", title)
        if match:
            return match.group()
        
        return "Unknown"
