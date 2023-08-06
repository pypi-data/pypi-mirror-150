#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .LiteCollection import LiteCollection
from .loader import load, dump


def hashable(obj) -> bool:
    ''' boolean check for hashable inputs '''
    try:
        hash(obj)
    except:
        return False
    else:
        return True

class LiteDict(LiteCollection):
    ''' python dict but backed by a sqlite database '''
    schema = [
        '''
            CREATE TABLE IF NOT EXISTS kv_store(
                key TEXT UNIQUE ON CONFLICT REPLACE,
                value TEXT,
                CHECK(json_valid(value))
            )
        '''
    ]
    _default_db_path = LiteCollection._default_db_path
    
    def __init__(self, db_path=_default_db_path, *dict_args, **dict_kwargs):
        if not isinstance(db_path, str):
            # db_path is being used as a traditional arg for dict()
            dict_args = db_path, *dict_args
            db_path = LiteDict._default_db_path
        # ensure db_path is a string now
        assert isinstance(db_path, str), db_path
        # assemble the backend
        LiteCollection.__init__(
            self,
            LiteDict.schema,
            db_path=db_path
        )
        # load in any data passed to the constructor
        if dict_args or dict_kwargs:
            # if other args exist, the user probably wants
            # the normal dict() constructor behavior
            self.update(
                dict(
                    *dict_args,
                    **dict_kwargs
                )
            )
            
    def __setitem__(self, key, value):
        assert hashable(key), f'unhashable input {key}'
        list(self._cursor.execute(
            '''
                INSERT INTO kv_store(key, value) VALUES (?, ?)
            ''',
            [dump(key), dump(value)]
        ))
        if self._autocommit:
            self.commit()
        
    def __contains__(self, key):
        assert hashable(key), f'unhashable input {key}'
        count, = self._cursor.execute(
            '''
                SELECT count(key) FROM kv_store WHERE key=? LIMIT 1
            ''',
            [dump(key)]
        ).fetchone()
        return count == 1
        
    def __getitem__(self, key):
        assert hashable(key), f'unhashable input {key}'
        query = self._cursor.execute(
            '''
                SELECT value FROM kv_store WHERE key=? LIMIT 1
            ''',
            [dump(key)]
        )
        for value, in query:
            return load(value)
        raise KeyError(f'couldnt find key {repr(key)}')
    
    def __delitem__(self, key):
        assert hashable(key), f'unhashable input {key}'
        list(self._cursor.execute(
            'delete from kv_store where key=?',
            [dump(key)]
        ))
        if self._autocommit:
            self.commit()
        
    def __iter__(self):
        query = self._cursor.execute(
            '''
                SELECT key FROM kv_store
            '''
        )
        for key, in query:
            yield load(key)
    
    def __len__(self):
        query = self._cursor.execute('''
            select count(key) from kv_store
        ''')
        for cnt, in query:
            return cnt
            
    def __str__(self):
        return str(dict(self.items()))
        
    def __repr__(self):
        return repr(dict(self.items()))
        
    def update(self, update_dict):
        assert isinstance(update_dict, dict), update_dict
        for k,v in update_dict.items():
            self[k] = v
            
    
    def iter_values(self):
        query = self._cursor.execute(
            '''
                SELECT value FROM kv_store
            '''
        )
        for value, in query:
            yield load(value)
    
    def iter_items(self):
        query = self._cursor.execute(
            '''
                SELECT key, value FROM kv_store
            '''
        )
        for key, value in query:
            yield load(key), load(value)
    
    def keys(self):
        return list(self)
        
    def values(self):
        return list(self.iter_values())
    
    def items(self):
        return list(self.iter_items())
