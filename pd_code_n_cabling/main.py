from de_r1 import de_r1

# 检查 pd_code 是否合法
# 不考虑平面图条件
def arc_index_checker(pd_code) -> bool:
    dic = {}
    for item in pd_code:
        if type(item) not in [list, tuple]:
            return False
        if len(item) != 4:
            return False
        for arc_index in item: # 检查弧线编号是否各出现两次
            if dic.get(arc_index) is None:
                dic[arc_index] = 0
            dic[arc_index] += 1
    for val in dic:
        if dic[val] != 2:
            return False
    return True

# 获得后继（默认后继 +1，特殊处理最大值位置）
def get_nxt_arc_number(b, blk, fa) -> int:
    v = fa[b]
    if b == max(blk[v]):
        ans = min(blk[v])
    else:
        ans = b + 1
    return ans

# 获得前驱
def get_lst_arc_number(a, blk, fa) -> int:
    v = fa[a]
    if a == min(blk[v]):
        return max(blk[v])
    else:
        return a - 1

def get_a(a, i, j, m, n, blk, fa):
    if i != n:
        return (a + j*m, i)
    else:
        return (get_nxt_arc_number(a, blk, fa) + j*m, 0)
    
def get_b(b, i, j, m, n, blk, fa):
    return get_a(b, j, i, m, n, blk, fa)

# 获取交叉点矩阵
def get_crossing_matrix_for_item(item, blk, fa, m, n):
    b, a, bp, ap = item
    assert bp == get_nxt_arc_number(b, blk, fa)
    assert ap in [get_lst_arc_number(a, blk, fa), get_nxt_arc_number(b, blk, fa)]
    arr = []
    for i in range(n):
        for j in range(n):
            if ap == get_lst_arc_number(a, blk, fa): # 减小方向 [b, a+1, b+1, a]
                arr.append([
                    get_b( b,   i,   j, m, n, blk, fa), 
                    get_a(ap, i+1,   j, m, n, blk, fa), 
                    get_b( b,   i, j+1, m, n, blk, fa), 
                    get_a(ap,   i,   j, m, n, blk, fa)
                ])
            else: # 增大方向 [b, a, b+1, a+1]
                arr.append([
                    get_b(b,   i,   j, m, n, blk, fa), 
                    get_a(a,   i,   j, m, n, blk, fa), 
                    get_b(b,   i, j+1, m, n, blk, fa), 
                    get_a(a, i+1,   j, m, n, blk, fa)
                ])
    return arr

# 合并两个连通块
# 直接在 dic 上进行修改
def merge_dic_term(dic, x, y):
    if x == y:
        return
    merged_list = dic[x] + dic[y]
    dic[x] = []
    dic[y] = []
    dic[min(x, y)] = sorted(merged_list)

def find(fa, x): # 路径压缩并查集
    if fa[x] == x:
        return x
    else:
        root  = find(fa, fa[x])
        fa[x] = root
        return root

# 合并连通块
def merge(fa: dict, a, b):
    a = find(fa, a)
    b = find(fa, b)
    fa[max(a, b)] = fa[min(a, b)]

# 获得所有联通分支以及并查集
def get_componets(pd_code):
    fa  = {}
    blk = {}
    for item in pd_code:
        for v in item:
            fa[v]  = v
            blk[v] = []
    for item in pd_code:
        a, b, c, d = item
        merge(fa, a, c)
        merge(fa, d, b)
    for v in fa: # 拍扁并查集
        find(fa, v)
    for v in fa:
        blk[fa[v]].append(v)
    for v in blk:
        blk[v] = sorted(blk[v])
    return blk, fa

# 对所有 arc 进行重新编号
def renumbering(arr) -> list:
    all_id= []
    for item in arr:
        for term in item:
            if term not in all_id:
                all_id.append(term)
    all_id  = sorted(all_id)
    get_new_idx = {
        old_id: new_id + 1
        for new_id, old_id in enumerate(all_id)
    }
    new_pd_code = []
    for old_item in arr:
        new_item = []
        for old_term in old_item:
            new_item.append(get_new_idx[old_term])
        new_pd_code.append(new_item)
    return new_pd_code

# 计算扭结的
def pd_code_n_cabling(pd_code: list, n: int):
    assert n >= 1
    arc_index_checker(pd_code)
    pd_code = de_r1(pd_code)
    m       = len(pd_code) * 2       # 记录弧线总段数
    blk, fa = get_componets(pd_code) # 记录连通块以及并查集
    arr = []
    for item in pd_code:
        arr += get_crossing_matrix_for_item(item, blk, fa, m, n)
    return renumbering(arr)

if __name__ == "__main__":
    print(pd_code_n_cabling([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]], 2))