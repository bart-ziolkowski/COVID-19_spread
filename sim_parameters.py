TRASITION_PROBS = {
    'less_5':
    {
        'H':{'H':0.9, 'I':0.1}, 
        'I':{'I':0, 'S':0.5, 'M':0.5}, 
        'S':{'S':0, 'D':0.01, 'M':0.99}, 
        'D':{'D':1}, 
        'M':{'M':0, 'H':1}
    },
    '5_to_14':
    {
        'H':{'H':0.9, 'I':0.1}, 
        'I':{'I':0, 'S':0.5, 'M':0.5}, 
        'S':{'S':0, 'D':0.01, 'M':0.99}, 
        'D':{'D':1}, 
        'M':{'M':0, 'H':1}
    },
    '15_to_24':
    {
        'H':{'H':0.7, 'I':0.3}, 
        'I':{'I':0, 'S':0.5, 'M':0.5}, 
        'S':{'S':0, 'D':0.05, 'M':0.95}, 
        'D':{'D':1}, 
        'M':{'M':0, 'H':1}
    },
    '25_to_64':
    {
        'H':{'H':0.7, 'I':0.3}, 
        'I':{'I':0, 'S':0.5, 'M':0.5}, 
        'S':{'S':0, 'D':0.2, 'M':0.8}, 
        'D':{'D':1}, 
        'M':{'M':0, 'H':1}
    },
    'over_65':
    {
        'H':{'H':0.7, 'I':0.3}, 
        'I':{'I':0, 'S':0.5, 'M':0.5}, 
        'S':{'S':0, 'D':0.4, 'M':0.6}, 
        'D':{'D':1}, 
        'M':{'M':0, 'H':1}
    }
}

HOLDING_TIMES = {
    'less_5': {'H':0, 'I':4, 'S':14, 'D':0, 'M':120},
    '5_to_14': {'H':0, 'I':4, 'S':14, 'D':0, 'M':120},
    '15_to_24': {'H':0, 'I':4, 'S':14, 'D':0, 'M':120},
    '25_to_64': {'H':0, 'I':4, 'S':14, 'D':0, 'M':120},
    'over_65': {'H':0, 'I':4, 'S':14, 'D':0, 'M':120}
}
