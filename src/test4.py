import sqlite3
conn = sqlite3.connect(':memory:')
cur = conn.cursor()
sql = '''
create table if not exists news(
  id         integer primary key,
  published  text,
  url        text,
  title      text,
  body       text,  -- URL先から本文だけを抽出したプレーンテキスト
  CONSTRAINT cstr_unique UNIQUE(published,url) -- 公開日時とURLの両方が被ると同一とみなす
);
insert into news(published, url) values('0','A');
insert into news(published, url) values('0','B');
insert or fail into news(published, url) values('0','A');
insert into news(published, url) values('1','A');
insert into news(published, url) values('1','B');
'''
try: cur.executescript(sql)
except sqlite3.IntegrityError as err_sql_integ: # おそらく制約違反
    import traceback
    import sys
    msg = str(err_sql_integ.with_traceback(sys.exc_info()[2]))
    traceback.print_exc()
    print(cur.execute('select * from sqlite_master;').fetchall())
    print(cur.execute("select * from pragma_index_xinfo('news');").fetchall())
    print(cur.execute("select * from pragma_index_xinfo('cstr_unique');").fetchall())
    print(cur.execute("select * from pragma_table_info('news');").fetchall())

    if 'UNIQUE' in msg and 'published' in msg and 'url' in msg: pass
    else: self.conn.rollback() # ロールバックする
except: # それ以外
    import traceback
    traceback.print_exc()
    self.conn.rollback() # ロールバックする
finally: print(cur.execute('select count(*) from news;').fetchone()[0])

