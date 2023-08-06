# TP Importer

This package is used for importing our main Titelplanung Excel files;
<br>
as this data is used in different systems this package provides adapters to use the imported data within different products
<br>
## Usage
Usage Example (Transaktional - Feature):
```
def import_tp_data_for_mam():
    """
    importiert TP-Daten mit den fürs MAM genutzten Keys
    """
    tp_path = "G:\Listen\TPDD aktuell absolutiert.xlsm"
    tp_data = TP_Importer().get_tp_data_from_file(tp_path)
    tp_data_mam = Adapter_For_MAM().transform(tp_data)
    for title in tp_data_mam:
        # do something with title


if __name__ == '__main__':
    tp_data_mam = import_tp_data_for_mam()
```

Usage Example for TVTP Transaktional:

```
def _get_data(self) -> dict:
    """
    diese Methode liest die Daten aus der TV Titelplanung ein
    :return: Dict (one entry per series with the series-Basis-VendorID as key) - die Daten zu den Staffeln
        kann man als Liste von Dicts unter dem Key "seasons" aufrufen
        (auch wieder als Dict mit Key = Season-Basis-VID),
        die zu den Episoden sind im Staffel-Dict als Liste von Dicts unter dem Key "episodes" zu finden
        (auch wieder als Dict mit Key = Episode-Basis-VID)
    """
    filepath = "G:\Listen\TV Titelplanung DD_absolutiert_v2.xlsm"
    tp_data = TVTP_Importer(
        valid_statuses=(
            "ok",
            "change",
            "new",
            "alt/keine Rechte",
            "canceled",
            "INDIZIERT",
            "no avail",
            "Rights expired",
            "ausgelaufen",
        )
    ).get_tp_data_from_file(filepath)
    return tp_data


tp_data = self._get_date()
for vendor_id, series in tqdm(tp_data.items()):
    # do something for series
    for vendor_id_season, season in series.get('seasons').items():
        # do something for seasons
        for vendor_id_episode, episode in season.get('episodes').items():
            # do something for episodes
```

Usage Example for Channels (Feature):
```
channel_tp_data_feature = dict()
importer = TP_Importer_Channels(
        valid_statuses=(("ok", "change", "new"))
    )
path = 'G:\Listen\Titelplanung Channels aktuell_absolutiert_new.xlsm'
tp_data = importer.get_tp_data_from_file(path)
print(tp_data.keys())
    

for channel_type, channel_titles in tp_data.items():
    # durch alle Channels iterieren
    for title in tqdm(channel_titles):
        # durch Titel in jeweiligem Channel iterieren
```

Usage Example for Channels (TV):
```
channel_tp_data_feature = dict()
importer = TVTP_Importer_Channels(
        valid_statuses=(("ok", "change", "new"))
    )
path = 'G:\Listen\Titelplanung Channels aktuell_absolutiert_new.xlsm'
tp_data = importer.get_tp_data_from_file(path)
print(tp_data.keys())

    

for channel_type, channel_titles in tp_data.items():
    # durch alle Channels iterieren
    for vendor_id, series in tqdm(channel_titles.items()):
        # do something for series
        for vendor_id_season, season in series.get('seasons').items():
            # do something for seasons
            for vendor_id_episode, episode in season.get('episodes').items():
                # do something for episodes
```