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
  UNIQUE(published,url) -- 公開日時とURLの両方が被ると同一とみなす
);
insert into news(published, url) values('0','A');
insert into news(published, url) values('0','B');
insert or fail into news(published, url) values('0','A');
insert into news(published, url) values('1','A');
insert into news(published, url) values('1','B');
'''
try: cur.executescript(sql)
except sqlite3.IntegrityError: # おそらく制約違反
    import traceback
    traceback.print_exc()
except: # それ以外
    import traceback
    traceback.print_exc()
    self.conn.rollback() # ロールバックする
finally: print(cur.execute('select count(*) from news;').fetchone()[0])

