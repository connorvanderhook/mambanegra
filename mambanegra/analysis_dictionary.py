import binascii

ANALYSIS_DICT = {
    # Current Production ('tademo.trueanthem.com/this/is/your/article/speaking-1')
    0: {"id": "ranked.current",
        "f": lambda x, y, z, v, u: x+y,
        "l": "Current Production",
        "t": "token(host, path)"},
    # Reversed PageID ('1-gnikaeps/elcitra/ruoy/si/siht/moc.mehtnaeurt.omedat')
    1: {"id": "ranked.uno",
        "f": lambda x, y, z, v, u: x+y[::-1],
        "l": "Reversed PageID",
        "t": "token(key)"},
    # CRC32 of PageID: ('2224592772')
    2: {"id": "ranked.dos",
        "f": lambda x, y, z, v, u: str(binascii.crc32(bytes(x+y, 'UTF-8')) & 0xffffffff),
        "l": "CRC32 of PageID",
        "t": "token(key, host)"},
    # Path + Host ('/this/is/your/article/speaking-1tademo.trueanthem.com')
    3: {"id": "ranked.tres",
        "f": lambda x, y, z, v, u: y+x,
        "l": "Path + Host",
        "t": "token(path, host)"},
    # CRC32(Path) + Host ('2894818572tademo.trueanthem.com')
    4: {"id": "ranked.cuatro",
        "f": lambda x, y, z, v, u: str(binascii.crc32(bytes(y, 'UTF-8')) & 0xffffffff)+x,
        "l": "CRC32(Path) + Host",
        "t": "token(key)"},
    5: {"id": "ranked.cinco",
        "f": lambda x, y, z, v, u: u,
        "l": "UUID",
        "t": "token(uuid)"},
    6: {"id": "ranked.seis",
        "f": lambda x, y, z, v, u: z+x,
        "l": "YYYY-MM-DD + Host",
        "t": "token(day, host)"},
    7: {"id": "ranked.siete",
        "f": lambda x, y, z, v, u: z+x+y,
        "l": "YYYY-MM-DD + Host + Path",
        "t": "token(day, host, path)"},
    8: {"id": "ranked.ocho",
        "f": lambda x, y, z, v, u: v+x,
        "l": "YYYY-MM + Host",
        "t": "token(month, host)"},
}