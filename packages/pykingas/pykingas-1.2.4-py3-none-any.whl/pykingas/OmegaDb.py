'''
class to Interface between json <=> python dict<tuple<int, int, int, int>, float> <=> cpp map<OmegaPoint, double>
json file contains omega integrals computed for a mie-potential without BH-diameters.

Note:
    The database will only contain a mixture once. That is: AR,HE and HE,AR is the same entry. Internal functions
    ensure that the correct values are returned. So if OmegaDb is initialized with (HE,AR) and (AR,HE) is found in the
    database, the components will be inverted.
'''

import json, os

DB_PATH = os.path.dirname(__file__) + '/omega_db.json'

class OmegaDb:
    '''
    self._db mirrors the database entry for the current mixture. If the mixture is either 'X,Y' or 'Y,X',
    self._db will be the dict corresponding exactly to the entry found in the database file
    '''
    def __init__(self, comps):
        self.__true_comps = comps # This is the mixture for which entries will be returned
        self._db_comps = comps # Is the key to the current database entry (may be flipped). __true_comps is 'AR,HE', _db_comps may be 'HE,AR'
        self._flipped_comps = False
        self._db = {} # Will contain k, v pairs with k corresponding to the key being used by the database

        with open(DB_PATH, 'r') as file:
            db = json.load(file)
            c1, c2 = self._db_comps.split(',')
            if self._db_comps in db.keys():
                comp_db = db[self._db_comps]
            elif ','.join((c2, c1)) in db.keys():
                self._db_comps = ','.join((c2, c1))
                self._flipped_comps = True
                comp_db = db[self._db_comps]
            else:
                comp_db = {}

        for k, v in comp_db.items():
            self._db[k] = v

        self._updated = False # Keep track of whether new computations have been entered into the database

    def get_db_key(self, op_key):
        # Take key as an OmegaPoint (used on cpp-side), return database key as a str.
        # If components are flipped, flip the key before returning
        # The return value is the correct database key.
        db_key = (op_key.ij, op_key.l, op_key.r, op_key.T_dK)
        if self._flipped_comps is True:
            if db_key[0] == 1:
                db_key = (2, db_key[1], db_key[2], db_key[3])
            elif db_key[0] == 2:
                db_key = (1, db_key[1], db_key[2], db_key[3])
            return str(db_key)

        return str(db_key)

    def get_return_key(self, db_key):
        # Take database key as a string, return tuple.
        # If components are flipped, flip the key before returning
        # The return value is the key corresponding to the mixture self.__true_comps
        key = tuple(int(i) for i in db_key.strip('()').split(','))
        if self._flipped_comps is True:
            if key[0] == 1:
                key = (2, key[1], key[2], key[3])
            elif key[0] == 2:
                key = (1, key[1], key[2], key[3])
            return key

        return key

    def db_to_vectors(self):
        # Return a (N, 4) and a (N, ) list of points and corresponding values
        pairs = [[self.get_return_key(db_k), v] for db_k, v in self._db.items()]
        vals = [p[1] for p in pairs]
        points = [[i for i in p[0]] for p in pairs] # (ij, l, r, T_dK)
        return points, vals

    def update(self, map):
        # map is the KineticGas.omega_map<OmegaPoint, double>
        for k, v in map.items():
            self._db[self.get_db_key(k)] = v
        self._updated = True

    def pull_update_from_db(self):
        with open(DB_PATH, 'r') as file:
            db = json.load(file)
            try:
                comp_db = db[self._db_comps]
            except KeyError:
                comp_db = {}
        for k, v in comp_db.items():
            self._db[k] = v

    def dump(self):
        if self._updated is True: # Only touch db if this instance has been updated
            self.pull_update_from_db() # Pull before pushing (in case another instance has written new computations to the database)
            with open(DB_PATH, 'r') as file:
                full_db = json.load(file)

            for k, v in self._db.items():
                if self._db_comps in full_db.keys():
                    full_db[self._db_comps][k] = v
                else:
                    full_db[self._db_comps] = {k : v}

            with open(DB_PATH, 'w') as file:
                json.dump(full_db, file, indent=6)

    def table(self, thing):
        return str(thing) + ' '*(25 - len(str(thing)))

    def __repr__(self):
        r = 'Omega values for mixture ' + self.__true_comps + ', using database entry for ' + self._db_comps + '\n'
        r += self.table('Database key') + self.table('Return key') + '\t\t Value\n\n'
        for k, v in self._db.items():
            r += self.table(k) + self.table(self.get_return_key(k)) + '\t'+ str(v) + '\n'

        return r