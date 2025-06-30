import re

class TitleExtractor:

    def normalize_text(self, text):
        return re.sub(r"[^\w\s]", "", text).lower().strip()

    def __init__(self):
        with open("backend/data/brands.txt", "r", encoding="utf-8") as f:
            raw_brands = [line.strip() for line in f.readlines()]
        self.brand_lookup = {self.normalize_text(brand): brand for brand in raw_brands}
        self.sorted_brand_keys = sorted(self.brand_lookup.keys(), key=lambda x: len(x.split()), reverse=True)

    category_keywords = {
        "Jacket": ["jacket", "parka", "anorak", "bomber", "blazer", "windbreaker", "coat", "overcoat", "trench"],
        "Hoodie": ["hoodie", "pullover", "sweatshirt"],
        "Shirt": ["shirt", "button-up", "button down", "flannel", "oxford", "tee", "t-shirt", "polo"],
        "Pants": ["pants", "jeans", "trousers", "slacks", "chinos", "joggers", "sweatpants", "track pants"],
        "Shorts": ["shorts", "cargo shorts", "denim shorts", "bike shorts", "gym shorts"],
        "Dress": ["dress", "gown", "maxi dress", "midi dress", "mini dress", "sundress"],
        "Skirt": ["skirt", "mini skirt", "midi skirt", "maxi skirt", "tennis skirt", "pleated skirt"],
        "Sweater": ["sweater", "knit", "cardigan", "crewneck", "jumper", "turtleneck"],
        "Top": ["top", "tank top", "tube top", "crop top", "camisole", "blouse"],
        "Shoes": ["shoes", "sneakers", "boots", "loafers", "heels", "sandals", "slides"],
        "Outerwear": ["coat", "trench", "overcoat", "peacoat", "raincoat"],
        "Activewear": ["activewear", "leggings", "sports bra", "gym", "athletic"],
        "Loungewear": ["loungewear", "pajamas", "pj", "sleepwear", "robe"],
        "Set": ["set", "matching set", "co-ord", "tracksuit"],
        "Accessories": ["hat", "cap", "beanie", "belt", "bag", "purse", "scarf", "gloves"],
    }

    sub_category_keywords = {
        "Windbreaker": ["windbreaker", "wind breaker"],
        "Denim": ["denim", "jean", "jeans"],
        "Puffer": ["puffer", "down jacket", "quilted", "bubble"],
        "Band": ["band", "tour", "concert", "rock", "metal"],
        "Graphic": ["graphic", "print", "screenprint", "design", "illustration"],
        "Varsity": ["varsity", "letterman"],
        "Track": ["track jacket", "track pants", "tracksuit", "jogger"],
        "Cropped": ["cropped", "crop top", "short length"],
        "Oversized": ["oversized", "baggy", "loose fit"],
        "Athletic": ["athletic", "sportswear", "training", "performance"],
        "Plaid": ["plaid", "checkered", "flannel"],
        "Vintage": ["vintage", "retro", "y2k", "90s", "80s"],
        "Corduroy": ["corduroy", "cords"],
        "Leather": ["leather", "faux leather", "pleather"],
        "Fleece": ["fleece", "sherpa", "polar fleece"],
        "Utility": ["utility", "cargo", "military", "field", "tactical"],
        "Striped": ["striped", "stripes", "pinstripe"],
        "Floral": ["floral", "flowers", "botanical"],
        "Hooded": ["hooded", "hoodie", "with hood"],
        "Sleeveless": ["sleeveless", "tank", "muscle tee"],
        "Button-Up": ["button-up", "button down", "oxford"],
        "Crewneck": ["crewneck", "crew neck"],
        "V-Neck": ["v-neck", "v neck"],
        "Pullover": ["pullover", "pull over"],
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
        title_clean = re.sub(r"[^\w\s]", "", title.lower()) 

        for label, keywords in keyword_map.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, title_clean):
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
        
        match = re.search(r"\b(\d{1,2})(?:x\d{1,2})?\b", title)
        if match:
            num = int(match.group(1))
            if num <= 28:
                return "XS"
            elif 29 <= num <= 30:
                return "S"
            elif 31 <= num <= 32:
                return "M"
            elif 33 <= num <= 34:
                return "L"
            elif 35 <= num <= 36:
                return "XL"
            else:
                return "XXL"
            
        return "Unknown"
