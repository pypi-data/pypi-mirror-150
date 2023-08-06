
def keyword_map(kw: str) -> str:
    amap = {
        'buildings burning': 'burn building',
        'buildings on fire': 'burn building',
        'burning buildings': 'burn building',
        'emergency plan': 'emergency',
        'emergency services': 'emergency',
        'fire': 'burn building',
        'nuclear reactor': 'nuclear',
        'nuclear disaster': 'nuclear',
        'radiation emergency': 'nuclear',
        'mass murder': 'massacre',
        'mass murderer': 'massacre',
        'wild fires': 'wildfire'
    }

