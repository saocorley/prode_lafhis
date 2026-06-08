import sys
import requests
from lxml import html

def fetch_response(l, v):
    res = requests.get(f'https://301060.exactas.uba.ar/es/one-vs-one/{l}{v}.htm')
    res.raise_for_status()
    return res.text

def get_percentages(src):
    h = html.fromstring(src)
    texts = h.xpath("//td[contains(@class,'valor')]/text()")
    return [int(t[:-1]) for t in texts]

def map_percentages_to_results(percentages):
    ret = {}
    for i in range(6):
        for j in range(6):
            ret[(i, j)] = percentages[6*i + j]
    return ret

def best_result(results):
    return max(results, key=lambda k: results[k])

# percentages = get_percentages(fetch_response(local, visitante))
# print(best_result(map_percentages_to_results(percentages)))

def levenshtein_distance(s1, s2):
    s1 = s1.lower()
    s2 = s2.lower()
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(n+1)] for _ in range(m+1)]

    # Initialize base cases
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j

    # Fill the matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # deletion
                dp[i][j-1] + 1,      # insertion
                dp[i-1][j-1] + cost  # substitution
            )

    # Print the matrix
    for i in range(m+1):
        row = [s1[i-1] if i > 0 else " "]
        for j in range(n+1):
            row.append(str(dp[i][j]))

    return dp[m][n]

mapping = {"estados unidos": "USA", "united states": "USA", "paises bajos": "NED", "alemania": "GER", "holanda": "NED", "corea del sur": "KOR", "corea": "KOR", "escocia": "SCO", "turquia": "TUR", "costa de marfil": "CIV", "arabia saudita": "KSA", "noruega": "NOR", "canada": "CAN", "brazil": "BRA", "czech republic": "CZE", "usa": "USA", "scotland": "SCO", "france": "FRA", "ivory coast": "CIV", "argentina": "ARG", "norway": "NOR", "ecuador": "ECU", "ghana": "GHA", "saudi arabia": "KSA", "australia": "AUS", "iran": "IRN", "algeria": "ALG", "korea republic": "KOR", "austria": "AUT", "germany": "GER", "bosnia and herzegovina": "BIH", "belgium": "BEL", "haiti": "HAI", "iraq": "IRQ", "spain": "ESP", "netherlands": "NED", "turkey": "TUR", "morocco": "MAR", "sweden": "SWE", "uruguay": "URU", "croatia": "CRO", "switzerland": "SUI", "new zealand": "NZL", "inglaterra": "ENG", "england": "ENG", "portugal": "POR", "south africa": "RSA", "tunisia": "TUN", "mexico": "MEX", "egypt": "EGY", "senegal": "SEN", "colombia": "COL", "paraguay": "PAR", "japan": "JPN", "jordania": "JOR", "qatar": "QAT", "uzbekistan": "UZB", "panama": "PAN", "cabo verde": "CPV", "congo": "COD", "curazao": "CUW", "dr congo": "COD", "rd congo": "COD"}

def normalize(team):
    return min(mapping.keys(), key=lambda t: levenshtein_distance(t, team))

def predict(partido):
    l = mapping[normalize(partido['local'])]
    v = mapping[normalize(partido['visitante'])]
    print(f'{l} vs {v}')
    percentages = get_percentages(fetch_response(l, v))
    goals_l, goals_v = best_result(map_percentages_to_results(percentages))
    return {"local": goals_l, "visitante": goals_v}

# print(predict({
#     "id":        "GC1",                          # identificador único del partido
#     "ronda":     "Fase de Grupos - Grupo C - Fecha 1",
#     "fecha":     "2026-06-15",
#     "hora":      "18:00",
#     "local":     sys.argv[1],
#     "visitante": sys.argv[2],
#     "sede":      "MetLife Stadium, Nueva Jersey",
# }))
