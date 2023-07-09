RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

shops = {
        "komputronik": ".leading-8.text-3xl",
        "x-kom": ".sc-n4n86h-1.hYfBFq",
        "morele": ".product-price",
        "proline": "b.cena_b>span",
        "eurortvagd": "",
        "mediaexpert": ""
    }

def printScraping(i, l):
    print(f"\rScraping: {'#' * i + '-' * (l - i)} {GREEN}{str(i * 100 // l)}%{RESET}",
          end='')

def printValue(key, value):
    print(f"Best price of {BLUE}{key} {RED}{value[0]}{RESET} is in {GREEN}{value[1]}{RESET}: {GREEN}{value[2]:.2f} zł{RESET}.")

def saveFile(parts):
    with open('list', 'w', encoding='utf-8') as f:
        current = ''
        total_sum = 0
        total = 0
        for key in sorted(parts, key=lambda _: parts[_][1]):
            if parts[key][1] != current:
                if total_sum != 0:
                    f.write(f"\t----Total in {current}: {total_sum:.2f} zł\n\n")
                    total_sum = 0
                current = parts[key][1]
                f.write(current + ':\n')
            total_sum += parts[key][2]
            total += parts[key][2]
            f.write("\t" + parts[key][0] + " - " + f"{parts[key][2]:.2f} zł" + "\n")
        f.write(f"\t----Total in {current}: {total_sum:.2f} zł\n\n")
        f.write(f"The total price of the whole setup is {total:.2f} zł.")