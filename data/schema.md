# Wedding Data Schema — `wedding.yaml`

Tento dokument popisuje strukturu datového souboru `data/wedding.yaml`.
Všechny texty a údaje webu se upravují **výhradně v YAML souboru** — HTML šablona se automaticky přegeneruje.

---

## Hlavní sekce

| Klíč | Typ | Popis |
|---|---|---|
| `couple` | objekt | Jména páru (`name_a`, `name_b`, `full_name_a`, `full_name_b`) |
| `wedding` | objekt | Datum, čas, datetime (ISO 8601 pro `.ics`), locale |
| `venue` | objekt | Název místa, popis, odkazy na mapy (Google Maps, Mapy.cz) |
| `parking` | objekt | Popis parkování, odkazy na mapy |
| `transport` | objekt | Informace o dopravě |
| `schedule` | seznam | Harmonogram dne — každá položka má `time`, `title`, `description`, `icon` |
| `accommodation` | objekt | Popis ubytování + `assignments` (seznam přiřazení hostů k pokojům) |
| `dress_code` | objekt | Styl, popis, upozornění na terén |
| `colors` | objekt | HEX kódy barevné palety (`primary`, `secondary`, `accent`, `background`, `text`, `text_light`) |
| `gifts` | objekt | Typ daru (`monetary`/`registry`/`none`), popis, volitelně `registry_url` |
| `children` | objekt | `allowed` (bool), `note` (text) |
| `pets` | objekt | `allowed_with_consultation` (bool), `note` (text) |
| `contacts` | seznam | Kontakty na den D — každý má `name`, `phone`, `role` |
| `privacy` | objekt | Metoda ochrany (`unlisted`/`password`/`encrypted`), `robots_noindex` (bool) |
| `site` | objekt | Doména, `base_url`, `title`, `meta_description` |

---

## Harmonogram (`schedule`)

Každá položka v seznamu:

```yaml
- time: "13:00"           # Čas ve formátu HH:MM
  title: "Svatební obřad"  # Název události
  description: ""           # Volitelný popis
  icon: "ceremony"          # Ikona: ceremony | drinks | camera | dinner | cake | dance | party | sparkler
```

---

## Ubytování (`accommodation.assignments`)

Každá položka:

```yaml
- place: "Pokoj 1"          # Název místa/pokoje
  type: "pokoj"              # Typ: stan | auto | apartmán | pokoj | tp | místnost
  guests: ["Jméno1", "Jméno2"]  # Seznam hostů
```

---

## Barevná paleta (`colors`)

Všechny barvy jsou HEX kódy. Pro změnu palety stačí přepsat hodnoty:

```yaml
colors:
  primary:    "#4A7C59"   # Hlavní barva (zelená)
  secondary:  "#E8B931"   # Sekundární barva (žlutá)
  accent:     "#3B7CB8"   # Akcentová barva (modrá)
  background: "#FDF8F0"   # Pozadí stránky
  text:       "#2C2C2C"   # Barva textu
  text_light: "#FFFFFF"   # Bílý text
```

---

## Kontakty (`contacts`)

```yaml
- name: "Jméno"
  phone: "+420 123 456 789"
  role: "Svědek"            # Svědek | Svědkyně | Koordinátor | ...
```
