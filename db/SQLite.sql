-- SQLite
SELECT hash, title, size, category, createtime, task_finished, save_path, added_time, hash_v2, torrent_format
FROM MyShares;

SELECT DISTINCT task_finished,save_path FROM MyShares;

delete from MyShares where 1 = 1;