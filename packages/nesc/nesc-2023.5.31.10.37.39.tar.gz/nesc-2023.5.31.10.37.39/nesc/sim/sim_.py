#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : sim_app
# @Time         : 2021/9/1 下午2:45
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  :

from shutil import copyfile

from meutils.pipe import *
from meutils.log_utils import logger4wecom
from meutils.decorators.catch import wecom_catch, wecom_hook

from bertzoo.simbert2vec import Simbert2vec
from gensim.models import KeyedVectors

tqdm.pandas()


def get_vector_cache():
    p = Path('vecs.cache')  # p.read_text() windows有编码问题

    w2v = {}
    if p.is_file():
        copyfile(p, f"{p}.bak.{time.time()}")  # 备份词向量
        with open(p, encoding='utf8') as f:
            for r in f:
                r = r.split()
                w2v[r[0]] = np.array(r[1:], float)

    return w2v


def main(target, file, topn=10, batch_size=512, model_home='chinese_roformer-sim-char-ft_L-6_H-384_A-6'):
    logger.info(f"输入路径：{file}")

    s2v = Simbert2vec(model_home)
    w2v = get_vector_cache()

    @lru_cache()
    def text2vec(text='年收入'):
        return w2v.get(text, s2v.encoder([text], output_dim=None)[0])

    logger.info("向量化")
    df = (
        pd.read_csv(file, names=['s'])
            .drop_duplicates()
            .assign(s=lambda df: df.s.astype(str).str.replace(' ', ''))
    )

    df1 = df[df.s.isin(w2v)]
    if len(df1):
        df1 = pd.concat([df1[['s']], pd.DataFrame(np.row_stack(df1.s.map(lambda w: w2v.get(w))))], 1)

    df2 = df[~df.s.isin(w2v)]
    if len(df2):

        vs = []
        for texts in tqdm(df2.s.tolist() | xgroup(batch_size), '向量化'):
            _ = s2v.encoder(texts, output_dim=None)
            vs.append(_)
        df2 = pd.concat([df2[['s']], pd.DataFrame(np.row_stack(vs))], 1)

    pd.concat([df1, df2]).to_csv('vecs.txt', ' ', index=False, header=False)

    model = KeyedVectors.load_word2vec_format('vecs.txt', no_header=True)

    # 添加不在cache向量方便以后加速
    df2.to_csv('vecs.cache', ' ', index=False, header=False, mode='a')
    logger.info(f"Cache {len(df2)} 个向量")

    if Path(target).is_file():
        target = Path(target).read_text(encoding='utf8').strip().split('\n')
    else:
        target = [target]

    df_rsts = []
    for idx, t in tqdm(enumerate(target), desc="向量匹配"):
        r2s = model.similar_by_vector(text2vec(t), topn=topn)
        df_rst = pd.DataFrame(r2s, columns=['recall', 'score'])
        df_rst.insert(0, 'target', t)
        df_rsts.append(df_rst)

        if idx == 0:
            df_rst.columns = ['target', 'recall', 'score']
            tb = Besttable.draw_df(df_rst)
            logger.info("首句匹配结果")
            time.sleep(0.3)
            print(tb)

    opath = Path(file).parent / 'recall.tsv'
    (
        pd.concat(df_rsts, ignore_index=True)
            .to_csv(opath, '\t', index=False, header=False)
    )
    logger.info(f"输出路径：{opath}")
