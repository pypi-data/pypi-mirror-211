from src import enedis_tic
from src.enedis_tic import link_layer
from collections import namedtuple
import json
import os


with open(os.path.join(enedis_tic.__path__[0], 'infos.json'), 'r') as f:
    infos = json.loads(f.read())
with open(os.path.join(enedis_tic.__path__[0], 'euridis.json'), 'r') as f:
    euridis = json.loads(f.read())


async def tic(port, mode, sep):
    async for frame in link_layer.frame_iterator(port, mode, sep):
        yield FrameParser(frame).to_dict()


def parse_frame(frame):
    return FrameParser(frame).to_dict()


Measure = namedtuple('Measure', ('value', 'unit'))


class FrameParser:
    def __init__(self, frame):
        self.frame = frame

    def to_dict(self):
        res = dict()
        for key, value in self.frame.items():
            try:
                res.update(getattr(self, f'_parse_{key.lower()}')(value))
            except AttributeError:
                res.update(self._info(key, value))
        return res

    @staticmethod
    def _info(key, value):
        try:
            info = infos[key]
            try:
                unit = info['unit']
                return {info['name']: Measure(int(value), unit)}
            except KeyError:
                return {info['name']: value}
        except KeyError:
            return {key: value}

    @staticmethod
    def _parse_adsc(value):
        datas = dict()
        datas['Adresse secondaire du compteur'] = value
        datas['Constructeur'] = euridis['constructeurs'].get(value[0:2], None)
        datas['Appareil'] = euridis['appareils'].get(value[2:4], None)
        try:
            datas['Année de fabrication'] = 2000 + int(value[4:6])
        except ValueError:
            pass
        datas['Numéro de série'] = value[6:]
        return datas

    @staticmethod
    def _parse_optarif(value):
        if value.startswith('BBR'):
            option = 'Tempo'
        else:
            option = {
                'BASE': 'Base',
                'HC..': 'Heures Creuses',
                'EJP.': 'EJP'
            }.get(value, value)
        return {'Option tarifaire choisie': option}

    @staticmethod
    def _parse_stge(value):
        value = int(value, base=16)

        return {
            'Contact sec': ['fermé', 'ouvert'][get_bit_int(value, index=0)],
            'Organe de coupure': ['fermé', 'ouvert sur surpuissance', 'ouvert sur surtension', 'ouvert sur délestage', 'ouvert sur ordre CPL ou Euridis', 'ouvert sur une surchauffe avec une valeur du courant supérieure au courant de commutation maximal', 'ouvert sur une surchauffe avec une valeur de courant inférieure au courant de commutation maximal'][get_bit_int(value, index=1, length=3)],
            'État du cache-bornes distributeur': ['fermé', 'ouvert'][get_bit_int(value, index=4)],
            'Surtension sur une des phases': ['pas de surtension', 'surtension'][get_bit_int(value, index=6)],
            'Dépassement de la puissance de référence': ['pas de dépassement', 'dépassement en cours'][get_bit_int(value, index=7)],
            'Fonctionnement producteur/consommateur': ['consommateur', 'producteur'][get_bit_int(value, index=8)],
            'Sens de l’énergie active': ['énergie active positive', 'énergie active négative'][get_bit_int(value, index=9)],
            'Tarif en cours sur le contrat fourniture': 'énergie ventilée sur Index {}'.format(get_bit_int(value, index=10, length=3) + 1),
            'Tarif en cours sur le contrat distributeur': 'énergie ventilée sur Index {}'.format(get_bit_int(value, index=14, length=2) + 1),
            'Mode dégradée de l’horloge (perte de l’horodate de l’horloge interne)': ['horloge correcte', 'horloge en mode dégradée'][get_bit_int(value, index=16)],
            'État de la sortie télé-information': ['mode historique', 'mode standard'][get_bit_int(value, index=17)],
            'État de la sortie communication Euridis': ['désactivée', 'activée sans sécurité', '', 'activée avec sécurité'][get_bit_int(value, index=19, length=2)],
            'Statut du CPL':  ['New/Unlock', 'New/Lock', 'Registered'][get_bit_int(value, index=21, length=2)],
            'Synchronisation CPL': ['compteur non synchronisé', 'compteur synchronisé'][get_bit_int(value, index=23)],
            'Couleur du jour pour le contrat historique tempo': ['Pas d‘annonce', 'Bleu', 'Blanc', 'Rouge'][get_bit_int(value, index=24, length=2)],
            'Couleur du lendemain pour le contrat historique tempo': ['Pas d‘annonce', 'Bleu', 'Blanc', 'Rouge'][get_bit_int(value, index=26, length=2)],
            'Préavis pointes mobiles': ['pas de préavis en cours', 'préavis PM1 en cours', 'préavis PM2 en cours', 'préavis PM3 en cours'][get_bit_int(value, index=28, length=2)],
            'Pointe mobile (PM)': ['Pas de pointe mobile', 'PM 1 en cours', 'PM 2 en cours', 'PM 3 en cours'][get_bit_int(value, index=30, length=2)]
        }

    @staticmethod
    def _parse_relais(value):
        value = int(value, base=10)
        return {'Relai {}'.format(i + 1): ['ouvert', 'fermé'][get_bit_int(value, index=i)] for i in range(8)}


def get_bit_int(val, index, length=1):
    return int((val >> index) & ((2**length)-1))
