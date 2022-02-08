import random

#--------ハイパーパラメータ-------#
POPULATION_SIZE = 10 #生成する個体数
GTYPE_LENGTH = 10 #遺伝子長
GENERATION = 10 #実行世代数
MIN_X = -5.12 #探索範囲の最小値
MAX_X = 5.12  #探索範囲の最大値
ELITE_INDIV = 2 #エンリート順位 偶数
MUTATION_RATE = 0.3 #突然変異率
ERROR = 99
CROSS_POINT = 5

# GAの個体クラス
class Individual(object):
    def __init__(self, gtype, ptype=0, fitness=0, rank=0, pair=0):
        self.gtype = gtype #遺伝子
        self.ptype = ptype #遺伝子の実数表現
        self.fitness = fitness #適応度
        self.rank = rank #遺伝子の順位
        self.pair = pair #交差相手となる遺伝子のインデックス
    def __lt__(self, other): #特殊メソッド 比較　ソート時に使用
        # self > other
        return self.fitness > other.fitness

# 目的関数 y=x^2
def object_function(x):
    #目的変数 同時に桁丸め
    y = round(x ** 2, 2)
    return y

# 初期集団生成
def initialization(population):
    for i in range(POPULATION_SIZE):
        tmp = []
        for j in range(GTYPE_LENGTH):
            tmp.append(random.randint(0,1))
        population.append(Individual(tmp))
    return population

# 評価
def evaluation(population):
    #ptypeの計算
    for individual in population:
        #基数変換
        x = radix_trans(individual.gtype)
        #探索範囲へ正規化
        norm_x = normalization(x)
        #目的関数へ入力
        individual.ptype = norm_x
    #適応度の計算
    for individual in population:
        y = object_function(individual.ptype)  #y求める
        individual.fitness = fitness(y, 'max') #最大化
    # 降順にソートして順位づけ
    population = sorted(population)
    for i,individual in enumerate(population):
        individual.rank = i
    return population

#基数変換
def radix_trans(gtype):
    x=0
    #基数変換 2進数10進数
    for i,j in enumerate(gtype):
        x += j * (2**i)
    return x

#正規化
def normalization(x):
    #正規化
    x = MIN_X + ((MAX_X-MIN_X)/(2**GTYPE_LENGTH)) * x
    x = round(x, 2)
    return x

#適応度の計算
def fitness(ptype, str):
    __dict__ = {
        'min' : ptype, #最小化問題として定義
        'max' : 1 / abs(1+ptype) #最大化問題として定義
    }
    fitness = round(__dict__[str],2)
    return fitness

# 選択
def selection(population):
    #エリート保存と対選択
    select_rank = ELITE_INDIV + POPULATION_SIZE - 1 #対決定変数
    for i,individual in enumerate(population):
        if(i < ELITE_INDIV):
            individual.pair = ERROR #番兵
        else:
            individual.pair = select_rank - individual.rank
    return population

# 交叉
def cross_over(population):
    #一点交差
    for i, individual in enumerate(population):
        #エリート選択部分は無視　かつ　交叉相手との交換も無視
        if(ELITE_INDIV <= i and i < (POPULATION_SIZE-ELITE_INDIV)/2 + ELITE_INDIV):
            #上位親の上位5ビットを保存
            tmp1 = individual.gtype[CROSS_POINT:GTYPE_LENGTH]
            #下位親の上位5ビットを保存
            tmp2 = population[individual.pair].gtype[CROSS_POINT:GTYPE_LENGTH]
            #上位親の上位5ビットに下位親の上位5ビットをコピー
            individual.gtype[CROSS_POINT:GTYPE_LENGTH] = tmp2
            #下位親の上位5ビットに上位親の上位5ビットをコピー
            population[individual.pair].gtype[CROSS_POINT:GTYPE_LENGTH] = tmp1
    return population

# 突然変異
def mutation(population):
    #ランダムで個体決定
    for i in range(int(POPULATION_SIZE*MUTATION_RATE)):
        #個体のインデックスを決定
        x = random.randint(0, POPULATION_SIZE-1)
        #遺伝子の変曲点を決定
        y = random.randint(0, GTYPE_LENGTH-1)
        #0を1に変更 1を0に変更
        if(population[x].gtype[y] == 0):
            population[x].gtype[y] = 1
        else:
            population[x].gtype[y] = 0
    return population

#遺伝子情報の表示
def summary(i, population):
    print('----------------------- GENERATION ' + str(i+1) + ' -------------------------')
    print('            GTYPE', '             PTYPE', 'FITNESS', 'RANK', 'PAIR', sep='   ')
    for individual in population:
        print(individual.gtype, individual.ptype, individual.fitness, individual.rank,individual.pair, sep='     ')

def main():
    population = [] #母集団
    #初期集団生成
    population = initialization(population)
    #世代処理実行
    for i in range(GENERATION):
        #評価
        population = evaluation(population)
        #選択
        population = selection(population)
        #交叉
        population = cross_over(population)
        #突然変異
        population = mutation(population)
        #遺伝子情報の表示
        summary(i, population)
    return 0


if __name__ == '__main__':
    main()
